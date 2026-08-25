#!/usr/bin/env python3
"""Extração mecânica de metadados (título/autor/editora/idioma) + sha256 de EPUB/PDF.

Zero LLM, zero dependência externa (só stdlib) — pra não pagar token de modelo
por trabalho que é parsing puro. Agnóstico de pasta (aceita arquivo ou diretório
passado na hora) e de layout interno do EPUB (lê META-INF/container.xml pra achar
o OPF em vez de assumir OEBPS/content.opf).

Uso:
  extract_metadata.py <arquivo.epub|arquivo.pdf>      -> 1 objeto JSON
  extract_metadata.py <diretório>                      -> 1 objeto JSON por linha (JSONL)
"""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

NS_CONTAINER = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
NS_OPF = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}

SUPORTADOS = {".epub", ".pdf"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _vazio(formato: str) -> dict:
    return {"format": formato, "title": None, "authors": [], "publisher": None, "language": None}


def extract_epub(path: Path):
    import zipfile

    warnings = []
    result = _vazio("epub")
    with zipfile.ZipFile(path) as z:
        try:
            container = z.read("META-INF/container.xml")
        except KeyError:
            warnings.append("META-INF/container.xml ausente — EPUB fora do padrão OCF")
            return result, warnings

        root = ET.fromstring(container)
        rootfile = root.find(".//c:rootfile", NS_CONTAINER)
        opf_path = rootfile.attrib.get("full-path") if rootfile is not None else None
        if not opf_path:
            warnings.append("container.xml sem <rootfile full-path> utilizável")
            return result, warnings

        try:
            opf_data = z.read(opf_path)
        except KeyError:
            warnings.append(f"OPF declarado ({opf_path}) não existe dentro do EPUB")
            return result, warnings

        opf_root = ET.fromstring(opf_data)
        metadata = opf_root.find(".//opf:metadata", NS_OPF)
        if metadata is None:
            metadata = opf_root.find(".//metadata")  # alguns produtores omitem o namespace
        if metadata is None:
            warnings.append("elemento <metadata> não encontrado no OPF")
            return result, warnings

        title_el = metadata.find("dc:title", NS_OPF)
        if title_el is not None and title_el.text:
            result["title"] = title_el.text.strip()

        result["authors"] = [
            c.text.strip() for c in metadata.findall("dc:creator", NS_OPF) if c.text and c.text.strip()
        ]

        pub_el = metadata.find("dc:publisher", NS_OPF)
        if pub_el is not None and pub_el.text:
            result["publisher"] = pub_el.text.strip()

        lang_el = metadata.find("dc:language", NS_OPF)
        if lang_el is not None and lang_el.text:
            result["language"] = lang_el.text.strip()

    if not result["publisher"]:
        warnings.append("dc:publisher ausente no OPF — confirmar na ficha catalográfica/prefácio")
    if not result["authors"]:
        warnings.append("dc:creator ausente no OPF — confirmar manualmente")
    _flag_watermark(result, warnings)
    return result, warnings


_WATERMARK_TITLE_RE = re.compile(r"\(for [^)]+\)\s*$", re.IGNORECASE)
_WATERMARK_AUTHOR_TOKENS = {"author names here", "author name here", "unknown"}


def _flag_watermark(result: dict, warnings: list) -> None:
    """Alguns distribuidores (ex.: WeLib.org) reescrevem dc:title/dc:creator com
    watermark de destinatário ("(for Fulano)") ou placeholder genérico — visto em
    2 dos 7 livros já convertidos aqui. Isso não é ausência de dado (que os checks
    acima já cobrem), é dado presente e ERRADO — vale alerta próprio."""
    if result["title"] and _WATERMARK_TITLE_RE.search(result["title"]):
        warnings.append(
            f"título parece conter watermark de distribuidor ({result['title']!r}) — "
            "conferir capa/ficha catalográfica antes de usar no front-matter"
        )
    if any(a.strip().lower() in _WATERMARK_AUTHOR_TOKENS for a in result["authors"]):
        warnings.append(
            "autor é um placeholder genérico do produtor do EPUB — conferir capa/ficha "
            "catalográfica antes de usar no front-matter"
        )


_PDF_INFO_RE = re.compile(rb"/(Title|Author)\s*\(((?:[^()\\]|\\.)*)\)")


def _pdf_literal_to_bytes(raw: bytes) -> bytes:
    """Resolve os escapes de string literal do PDF (spec 7.3.4.2): \\ddd octal,
    \\n \\r \\t \\b \\f, \\( \\) \\\\, quebra de linha escapada, e escape
    desconhecido (ignora a barra, mantém o caractere seguinte)."""
    out = bytearray()
    i, n = 0, len(raw)
    simples = {0x6E: 0x0A, 0x72: 0x0D, 0x74: 0x09, 0x62: 0x08, 0x66: 0x0C, 0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
    while i < n:
        c = raw[i]
        if c == 0x5C and i + 1 < n:
            nxt = raw[i + 1]
            if 0x30 <= nxt <= 0x37:  # \ddd octal, 1-3 dígitos
                j, digits = i + 1, []
                while j < n and len(digits) < 3 and 0x30 <= raw[j] <= 0x37:
                    digits.append(raw[j] - 0x30)
                    j += 1
                val = 0
                for d in digits:
                    val = val * 8 + d
                out.append(val & 0xFF)
                i = j
                continue
            if nxt in simples:
                out.append(simples[nxt])
                i += 2
                continue
            if nxt in (0x0A, 0x0D):  # quebra de linha escapada -> continuação, descarta
                i += 2
                if nxt == 0x0D and i < n and raw[i] == 0x0A:
                    i += 1
                continue
            out.append(nxt)  # escape desconhecido: descarta a barra, mantém o caractere
            i += 2
            continue
        out.append(c)
        i += 1
    return bytes(out)


def _decode_pdf_literal(raw: bytes) -> str:
    b = _pdf_literal_to_bytes(raw)
    if b.startswith(b"\xfe\xff"):  # strings literais do PDF podem trazer UTF-16BE com BOM
        return b.decode("utf-16-be", errors="replace").lstrip("﻿").strip()
    return b.decode("latin-1", errors="replace").strip()


def extract_pdf(path: Path):
    warnings = [
        "metadados de PDF são melhor-esforço (regex sobre /Info) — em PDF escaneado/OCR "
        "quase sempre vêm vazios; confirme manualmente na ficha catalográfica do texto extraído"
    ]
    result = _vazio("pdf")
    with open(path, "rb") as f:
        blob = f.read()

    found = {}
    for m in _PDF_INFO_RE.finditer(blob):
        key = m.group(1).decode("ascii")
        found.setdefault(key, _decode_pdf_literal(m.group(2)))

    if found.get("Title"):
        result["title"] = found["Title"]
    if found.get("Author"):
        result["authors"] = [a.strip() for a in re.split(r",| and | e ", found["Author"]) if a.strip()]
    if not result["title"] and not result["authors"]:
        warnings.append("nenhum /Title ou /Author encontrado no /Info dict — PDF provavelmente sem metadados embutidos")
    return result, warnings


def processar(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".epub":
        data, warnings = extract_epub(path)
    elif suffix == ".pdf":
        data, warnings = extract_pdf(path)
    else:
        data, warnings = _vazio(suffix.lstrip(".") or "desconhecido"), [
            "formato sem extrator automático — preencher front-matter manualmente lendo o arquivo"
        ]
    data["source_path"] = str(path)
    try:
        data["sha256"] = sha256_file(path)
    except OSError as e:
        data["sha256"] = None
        warnings.append(f"falha ao calcular sha256: {e}")
    data["warnings"] = warnings
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("caminho", help="arquivo .epub/.pdf, ou diretório contendo vários")
    args = ap.parse_args()

    alvo = Path(args.caminho)
    if not alvo.exists():
        print(json.dumps({"error": f"caminho não encontrado: {alvo}"}), file=sys.stderr)
        sys.exit(1)

    if alvo.is_dir():
        arquivos = sorted(p for p in alvo.iterdir() if p.is_file() and p.suffix.lower() in SUPORTADOS)
        if not arquivos:
            print(json.dumps({"error": f"nenhum .epub/.pdf em {alvo}"}), file=sys.stderr)
            sys.exit(1)
        for p in arquivos:
            print(json.dumps(processar(p), ensure_ascii=False))
    else:
        print(json.dumps(processar(alvo), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
