# Chapter 9: Migrations and Sunsetting of Platforms

## Core Idea
Migrations are inevitable (end-of-life timelines have compressed from a decade to 1-2 years for cloud products) and are a platform team's biggest opportunity to prove its value — by engineering for transparent, automated migrations first, coordinating carefully second, and reserving mandates and sunsetting for when nothing else works.

## Frameworks Introduced
- **Migration antipattern quartet**: context-free deadlines (imposed with no discussion of what teams must defer), unclear requirements (users can't tell if a notice even applies to them), untested migrations (gaps/broken features discovered only after users start), and "clipboard-carrying scolds" (chasing/shaming users via wall-of-shame dashboards). These are options of last resort, not the default approach — reach for them only after exhausting engineering and communication investment.
- **Engineering-first migration strategy**: (1) tackle migrations early, before scale makes "scrappy get 'er done" energy break down; (2) use abstractions that minimize glue and limit variation (fewer versions in flight = less testing surface, per Ch 1); (3) architect for transparent migrations — combine judicious APIs with container packaging, autoscaling, canary/blue-green deployment, and advanced health monitoring so the platform team can migrate customers with minimal-to-no visible impact, backed by up-front agreements (chaos-testing/stability expectations, customer-maintained acceptance tests, defined maintenance windows); (4) track usage metadata (who uses what, which parts, who owns it) and centralize ownership metadata to fight "organizational drift" (unowned cron jobs/pipelines) before it blocks migrations; (5) automate instead of defaulting to clipboards/project managers — map dependency trees and build workflow tooling before asking for PM headcount.
- **Scope/limit/prioritize planned changes**: scope backward from hard deadlines within a 12-month horizon (dates further out are usually more negotiable than they appear — the industry often produces a shared solution before the date arrives); limit coupling of in-flight customer work (bundle only when it genuinely reduces total customer effort, not to sneak in unrelated platform-team wishlist items); track and deconflict overlapping migrations in bottom-up planning (Ch 7) so customers — and your own team's ability to isolate root causes — aren't hit by simultaneous unrelated changes.
- **Sunsetting criteria (true removal without a replacement)**: reserve for cases where (a) there are very few users (often from over-expanding to satisfy a noisy minority's custom configuration), (b) the cost of supporting the offering is disproportionately high relative to adoption, or (c) the team needs to redirect focus elsewhere and communicates where freed capacity is going. Sunsetting should hit only the deep long tail (e.g. ~0.1% of use cases) — if it would affect a meaningful slice of critical use, find a migration path to another offering instead of true sunsetting.

## Key Concepts
- **Migration (this chapter's definition)**: any mandatory platform change requiring some customer work to adopt — a spectrum from physical data-center moves to backward-breaking API upgrades to near-in-place upgrades needing acceptance testing.
- **Monorepos and migrations**: monorepo visibility into code-level dependencies mainly helps in-house library changes, not platform migrations broadly — platform services still need multi-version support because client redeployment isn't on your schedule, and thick clients depending on external OSS/vendor code create coupling monorepos don't remove.
- **On-ramps and off-ramps**: for migrations that can't be automated end-to-end, provide tooling/documentation for partial migration (testing before full cutover) and clear paths off the old system — validated via dogfooding with other platform teams as alpha testers, then advanced customers as early adopters.
- **The final 20% (long tail)**: the hardest, highest-risk, most customized applications are typically what's left after the bulk of a migration completes; plan explicitly for (a) how long you'll keep running the old system and how not to demoralize whoever staffs it, (b) unexpected dependency surprises (e.g. legacy hardware needing replacement mid-migration), and (c) who ultimately owns finishing laggard migrations (platform team vs. application team, negotiated per your org's culture).
- **Mandates as a scarce resource**: top-down CTO/executive mandates work but compete with every other initiative (cost-cutting, compliance, business expansion) for organizational attention — save mandate requests for essential work, ideally aligned with other mandatory efforts (security, compliance, major product initiatives) rather than issued in isolation.
- **Sunsetting coordination options**: give the system back to the consuming team (with a negotiated support-transition period, possibly moving 1-2 engineers permanently); identify off-ramps (migration docs, peer customers who've already migrated, DIY guidance, alternative tools); and always talk directly to remaining users rather than just sending a notice, negotiating a realistic timeline (quarters to years depending on criticality).

## Mental Models
- Treat "the deadline is more than 12 months out" as a signal to invest in engineering (easing future migration) rather than heavy coordination — industry-wide deadlines often slip or get solved collectively before they bite.
- When a team requests project-manager headcount for a migration, first ask "what have you automated to avoid needing this?" — often dependency mapping and workflow tooling can replace much of what a PM would coordinate manually.
- Recognize that resistance to sunsetting often comes from the team that built the failing feature, not just from customers — staff attached to a technology's success may need to leave before a sunset can actually complete.
- Distinguish sunsetting (no replacement offered) from a normal migration (moving people to an equivalent) — sunsetting is a narrower, harder conversation reserved for genuinely low-value, high-cost, or distracting offerings.

## Anti-patterns
- **Context-free deadlines**: imposing migration dates without discussing what else teams must defer.
- **Unclear migration requirements**: notices that assume users already know if they're affected.
- **Shipping untested migrations**: forcing users into a new offering with gaps, broken features, or missing docs.
- **Clipboard-carrying enforcement / wall-of-shame dashboards**: adds stress without fixing the underlying process gaps; a last resort, not a default.
- **Coupling unrelated changes into one deadline-driven migration** to offload platform-team wishlist items onto customers who have no choice but to comply.
- **Overusing top-down mandates**: creates a culture where application engineers feel they exist only to serve platform-team projects.
- **Refusing to sunset genuinely low-value/high-cost offerings** out of empathy fatigue or sunk-cost attachment from the building team.

## Worked Example
A base platform team owning standard Linux distributions faced a painful, dragged-out OS upgrade (customers found the verification work too tedious, requiring constant nagging) and, fearing a repeat, asked for headcount to hire project managers for the next version. Camille pushed back: "I will allow hiring of project managers only when you've proven to me that we have done everything we can to automate the work... Show me that we've hit the wall, and we can hire. Until then, be creative." The team responded by mapping the upgrade's dependency tree, building a system that detected when a set of dependencies was validated and automatically released the next step of work, and creating observability/tracking tooling designed around what would make the job easy for the customers doing the upgrade. The result: a significant improvement over prior migrations, though some human project management was still needed near the end — illustrating that automation-first doesn't always eliminate coordination entirely, but it should be exhausted before assuming project managers are the answer.

## Key Takeaways
1. Reach for engineering solutions (abstractions, transparent multi-version deployment, dependency/ownership tracking, automation) before communication/coordination processes, and before mandates/clipboards.
2. Scope migration urgency realistically — dates more than 12 months out usually have more give than they appear to, and industry-wide solutions often emerge before then.
3. Limit and prioritize overlapping migrations deliberately; don't bundle unrelated changes just because customers are already forced to move.
4. Automate to avoid clipboard-carrying enforcement — prove automation is exhausted before hiring project managers.
5. Plan explicitly for the final 20% (long tail): staffing morale on the legacy system, unexpected dependency surprises, and ownership negotiation.
6. Use top-down mandates sparingly, ideally bundled with other mandatory business initiatives, reserved for essential or final-push cases.
7. Reserve true sunsetting for genuinely low-adoption, high-cost, or distracting offerings — and expect resistance from the feature's own builders as much as from its customers.

## Connects To
- **Ch 1**: revisits "glue" and the value of encapsulation in reducing migration surface area.
- **Ch 2**: ownership metadata registries recur as a migration-planning prerequisite.
- **Ch 6**: chaos testing, canary/blue-green deployment, and guardrails are reused directly for transparent migrations.
- **Ch 7**: bottom-up roadmap planning is where overlapping-migration deconfliction and mandate estimation happen.
- **Ch 8**: migration cost estimation (Step 2 of the rearchitecture framework) is the direct application of this chapter's practices.
