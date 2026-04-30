# WoCo

`WoCo` is a research-oriented skill for agents that need specialized support on German works council law (`BetrVG`) and closely overlapping topics such as employee data protection, discrimination, working time, health and safety, election questions, and selected labor-court case law.

It is built to be statute-grounded first, then interpretation-aware second.

## Important Warning

This project can make mistakes.

It can miss controlling facts, newer case law, sector-specific rules, collective-agreement constraints, or procedural details that change the legal outcome.

It does **not** replace a German-qualified lawyer.

Use it as:

- a research accelerator
- a drafting helper
- a citation helper
- an issue-spotting tool

Do **not** use it as the only basis for:

- litigation decisions
- election challenges and deadline-sensitive procedural steps
- injunction strategies
- restructuring actions with high legal exposure
- sensitive surveillance or health-data programs

## Why This Skill Is Structured This Way

The core design choice is to keep the agent instructions small and move the legal corpus into versioned references.

That gives a few benefits:

- the agent can load only the relevant legal material instead of dragging the entire corpus into every answer
- the legal sources are inspectable and refreshable
- statute text, workflow guidance, and case-law notes stay separate
- the skill can cite exact `§` and `Art.` references instead of relying on vague memory

The current structure is:

- [`SKILL.md`](./SKILL.md): the operating instructions for the skill
- [`agents/openai.yaml`](./agents/openai.yaml): UI-facing metadata for agent launchers
- [`references/generated/`](./references/generated): versioned local statute snapshots
- [`references/topic-map.md`](./references/topic-map.md): issue-to-authority routing
- [`references/privacy-workflows.md`](./references/privacy-workflows.md): privacy-heavy authority bundles
- [`references/case-law-notes.md`](./references/case-law-notes.md): curated BAG digest
- [`scripts/update_sources.py`](./scripts/update_sources.py): source refresher
- [`scripts/privacy_authorities.py`](./scripts/privacy_authorities.py): focused privacy extractor

## What Is Versioned And Why

This repo versions:

- `SKILL.md`
- agent metadata
- generated Markdown statute snapshots in `references/generated/`
- hand-written workflow and case-law notes
- helper scripts

This repo does **not** version raw fetched source files in `references/raw/`.

Reason:

- the generated Markdown is easy to inspect in git
- the raw downloads are reproducible and bulky
- keeping raw fetches out of git makes the repo lighter while preserving refreshability

## Legal Sources

Primary statutory sources are fetched from official sources:

- `gesetze-im-internet.de` for German federal statutes and regulations
- the Publications Office of the European Union for the official German GDPR text

Case-law notes currently point to official BAG decision pages.

This project intentionally prefers:

1. official statutory text
2. official court decisions
3. only then practical interpretation

## How To Use It

Typical use cases:

- “Does a works council likely have co-determination rights over this monitoring tool?”
- “What are the first-pass authorities for employee-data processing in a works council context?”
- “Which `BetrVG` and `WO` sections matter for this election issue?”
- “Give me a cautious summary of the legal basis and the facts that could change the answer.”

Good prompting pattern:

1. ask the agent to identify the legal bucket
2. ask for exact statute references
3. ask it to separate binding law from interpretation
4. ask it to list what facts could change the outcome
5. ask it to state clearly that the output is informational, not legal advice

Example:

```text
Use WoCo to assess whether a works council likely has co-determination rights over a new monitoring tool. Cite the relevant BetrVG, BDSG, and GDPR provisions, separate law from interpretation, and include a note that this does not replace a lawyer.
```

## Privacy-Heavy Workflows

For privacy-heavy questions, use the helper:

```bash
python3 scripts/privacy_authorities.py --list-topics
python3 scripts/privacy_authorities.py --topic monitoring
python3 scripts/privacy_authorities.py --topic ai-profiling
```

This prints a focused first-pass bundle of relevant provisions extracted from the local statute snapshots.

## Refreshing Legal Sources

Refresh the versioned statute bundle with:

```bash
python3 scripts/update_sources.py
```

That updates:

- `references/generated/*.md`
- `references/raw/*` locally

If you refresh sources and want the updated legal text tracked in git, commit the generated Markdown files.

## Installing In Codex

Codex in this environment loads local skills from `~/.codex/skills/`.

The recommended setup is:

1. keep the repo in a normal development folder such as `~/Development/german-works-council-law`
2. symlink it into the Codex skills directory

Example:

```bash
ln -s ~/Development/german-works-council-law ~/.codex/skills/german-works-council-law
```

If the link already exists, replace or update it as needed.

Codex will then be able to use the skill as `$german-works-council-law`.

## Installing In OpenCode

In this environment, OpenCode appears to use a global rules file at `~/.opencode_rules`, not a Codex-style skills folder.

That means the clean approach is:

1. keep this repo in `~/Development`
2. append or adapt an instruction snippet into `~/.opencode_rules`
3. point the instructions at this repo’s files so the agent can use them as a local legal knowledge base

A starter snippet is provided at [`opencode_rules.woco.md`](./opencode_rules.woco.md).

Suggested install flow:

```bash
cat ./opencode_rules.woco.md >> ~/.opencode_rules
```

Then adjust the absolute path in that snippet if your repo lives somewhere else.

Important note:

- this is a pragmatic local integration pattern based on the OpenCode setup present on this machine
- it is not a claim about every OpenCode installation everywhere

## Publishing This To GitHub

Yes, this is a good candidate for a standalone GitHub repo.

Recommended publishing posture:

- publish as a dedicated `WoCo` skill repo
- keep the legal-warning language prominent
- keep generated Markdown sources versioned
- keep raw downloads ignored
- avoid marketing it as “legal advice”
- describe it as an informational agent skill or legal-research helper

Good repo positioning:

- “German works council law skill for agents”
- “Statute-grounded and citation-oriented”
- “Informational only, not a substitute for a lawyer”

## Suggested GitHub Description

```text
WoCo: a statute-grounded German works council law skill for agents. Informational only and not a substitute for a lawyer.
```

## Maintenance Guidance

- refresh the source snapshots when needed
- extend case-law notes carefully and with official citations
- keep the disclaimer language intact
- avoid turning high-level notes into overconfident legal conclusions
- prefer adding narrow helpers over bloating `SKILL.md`

## Current Limitations

- the case-law layer is curated, not comprehensive
- local generated texts may lag if not refreshed
- some legal questions depend heavily on facts outside the statutes
- labor-court interpretation can matter more than the text alone
- collective agreements and company-specific arrangements can change the practical answer

## Repo Status

This repo is intended to be usable as:

- a local Codex skill
- a local OpenCode rules-backed knowledge module
- a GitHub-hosted WoCo agent-skill project
