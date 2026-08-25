# Capítulo 1: Introdução e instalação

## Core Idea
O livro é um bloco de notas de referência — não um tutorial passo a passo — com exemplos prontos para classificação e regressão sobre dados estruturados usando o ecossistema Python (pandas, scikit-learn e dezenas de bibliotecas satélite), deliberadamente fora do escopo de deep learning.

## Key Concepts
- **Dados estruturados** é o foco do livro; deep learning é citado como melhor opção para dados não estruturados (imagem, áudio, texto livre), mas fica fora do escopo.
- **Instalação JIT ("just in time")**: não instalar todas as dezenas de bibliotecas citadas de uma vez — instalar cada uma só quando o exemplo específico for usado, para evitar conflitos de versão.
- **pip vs. conda**: duas vias de instalação de pacotes Python, cada uma com seu próprio isolamento de ambiente (`venv` para pip, `conda create --name` para conda) e seu próprio arquivo de dependências (`requirements.txt` vs. `environment.yml`).
- Nem todas as bibliotecas citadas estão disponíveis via conda; é seguro usar `pip` dentro de um ambiente conda ativo, sem precisar criar outro ambiente virtual.

## Anti-patterns
- **Instalar todas as bibliotecas do livro de uma vez**: gera conflitos de versão desnecessários; instalar sob demanda.
- **Misturar instalação global e de ambiente virtual**: sempre ativar o ambiente (`venv`/`conda`) antes de instalar, para isolar versões por projeto.

## Code Examples
```python
# criação e ativação de ambiente virtual (pip)
$ python -m venv env
$ source env/bin/activate       # Linux/Mac
C:> env\Scripts\activate.bat    # Windows
(env) $ pip install pandas
(env) $ pip freeze > requirements.txt
(other_env) $ pip install -r requirements.txt

# criação e ativação de ambiente (conda)
$ conda create --name env python=3.6
$ conda activate env
(env) $ conda install pandas
(env) $ conda env export > environment.yml
(other_env) $ conda create -f environment.yml
```
- **O que demonstra**: os dois fluxos completos e paralelos (pip/venv vs. conda) para criar ambiente isolado, instalar pacote e exportar/reproduzir dependências.

## Key Takeaways
1. O livro assume familiaridade prévia com Python e, idealmente, com pandas.
2. Instale bibliotecas sob demanda ("JIT"), não todas de uma vez.
3. `venv`+pip e `conda` são caminhos paralelos e intercambiáveis — pip funciona dentro de um ambiente conda quando um pacote não está no repositório do Anaconda.

## Connects To
- **Ch 3**: primeiro exemplo completo de classificação, onde as bibliotecas instaladas aqui (pandas, sklearn, Yellowbrick) entram em uso.
