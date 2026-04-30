---
name: german-works-council-law
description: Use this skill for German works council, Betriebsrat, BetrVG, co-determination, election rules, consultation rights, personnel measures, working time, health and safety, discrimination, and data-protection questions that overlap with German employment law. Use it when the answer should be grounded in the relevant statute text with section-level citations and clear separation between binding law, practical inference, and unresolved risk.
---

# WoCo: German Works Council Law

## Overview

Use this skill to answer German works council and overlapping employment-law questions in a statute-grounded way. The skill is designed to anchor answers in the official legal text first, then add practical interpretation with explicit caveats.

This skill is a research and drafting aid. It is prone to mistakes, may miss decisive case law or factual nuances, and does not replace advice from a German-qualified lawyer.

## When To Use

Use this skill for questions about:

- constitution, election, composition, and procedure of a works council
- co-determination, participation, consultation, and information rights
- working time, shift models, attendance, remote work, and workplace monitoring
- personnel measures, dismissals, transfers, hiring, and restructuring
- discrimination, complaints, and equal-treatment topics in a works-council context
- data protection questions involving the employer, works council, and employee data
- drafting or reviewing works-council-facing summaries, agendas, FAQs, and issue spotters

Do not use this skill as a substitute for German-qualified legal advice in litigation, injunction, deadline-critical election disputes, or matters that turn on current case law that is not bundled with the skill.

## Answer Workflow

1. Classify the question before answering.
   Common buckets are election, constitution/procedure, social co-determination, personnel measures, economic matters, data protection, discrimination, or health and safety.
2. Read the smallest relevant set of references.
   Start with `references/topic-map.md`, then open the matching files in `references/generated/`.
3. Ground the answer in primary law first.
   Cite exact sections such as `§ 87 Abs. 1 Nr. 2 BetrVG`, `§ 99 BetrVG`, `§ 79a BetrVG`, `§ 26 BDSG`, or the relevant `WO` provision.
4. Separate law from interpretation.
   Distinguish between:
   - binding statutory text
   - practical interpretation or likely application
   - open questions, factual gaps, or case-law dependency
5. Finish with pragmatic next steps.
   If useful, suggest what facts to confirm, which body should act, and what documents or timeline matter next.

## Output Rules

- Prefer the current German statutory text as the primary source.
- Use local references as the starting point, but for high-stakes or date-sensitive questions verify the current official text online before giving a confident answer.
- Do not invent holdings, deadlines, or procedural steps.
- State clearly that the answer is an informational assessment, not legal advice.
- If a point depends on case law, commentary, collective agreements, or company structure, say so explicitly.
- Avoid categorical answers when the result depends on facts such as establishment size, tariff coverage, election mode, presence of a central works council, or whether a measure is mandatory or voluntary.
- Quote sparingly; usually section citations plus paraphrase are better.

## Recommended Response Shape

Use this structure when helpful:

1. Short answer
2. Legal basis
3. Why it likely applies here
4. What facts could change the answer
5. Practical next step

## Risk And Escalation Rules

Escalate clearly when the question involves:

- election challenges, voidability, or strict procedural deadlines
- injunctions, labor-court litigation, or criminal exposure
- mass layoffs, transfer of business, or complex restructuring
- sensitive processing of employee data or surveillance
- unsettled issues that likely require case law or specialist commentary

In those cases, say that the skill can provide a statute-grounded issue map, but specialist German legal review is recommended before action.

## References

Open these files as needed:

- `references/topic-map.md`
- `references/index.md`
- `references/generated/betrvg.md`
- `references/generated/wo-betrvg.md`
- `references/generated/agg.md`
- `references/generated/arbzg.md`
- `references/generated/arbschg.md`
- `references/generated/bdsg.md`
- `references/generated/gdpr.md`
- `references/case-law-notes.md`

## Privacy Helper

For privacy-heavy questions, run:

```bash
python3 scripts/privacy_authorities.py --topic monitoring
```

Available topics are printed by:

```bash
python3 scripts/privacy_authorities.py --list-topics
```

Use the helper to narrow the first-pass statute set before reading the fuller source files.

## Updating Sources

Run:

```bash
python3 scripts/update_sources.py
```

This refreshes the local statute snapshots from official German sources under `gesetze-im-internet.de` and writes both cleaned Markdown and raw HTML copies. If a question is especially high stakes, refresh first and then verify the specific cited provisions online.
