---
name: why
description: "Use for 'why does X work this way', 'why we picked Y', 'why does our number differ from the paper', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and tools and queries each evidence category (source control, issue tracker, long-form docs, real-time chat, cluster and job records, run logs and failures, experiment tracker, published record) in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior."
---

# Why

Investigate the motivation and intent behind code or a result. The companion `how` skill answers what the code does and how it works. `why` answers what forces led to its shape.

Each spawn below names a role: use the `<role>` model from the labstack model config (lab-mode, Roles). A missing config or role means the session model. If a configured model is unavailable, use the session model and say so. Match each subagent's effort to the job where your harness lets you set it.

Give every subagent the session's tools, including MCP servers. **Do not use a read-only mode that strips MCP access.** It disables the MCP-backed investigators and the synthesizer's citation spot-checks. Investigators still shouldn't write anything.

## Operating Posture

Operate as a **careful, cautious, and precise investigator**. Be honest about what you know vs what you're inferring. Read `references/epistemics.md` for the full confidence framework and phrasing guide. The synthesizer must follow it.

## Step 1. Understand the Target and the Question

The **target** is usually a chunk of code, a config value, a result, a pattern, a feature, or a named design decision. The **question** is usually a design rationale, a tradeoff, a motivating edge case, an external constraint, dead code, a broad history sweep, or why our number differs from a paper's.

If the target is vague ("why do we do it this way?" with no clear referent), make your best guess from conversation context (open files, recent edits, cursor location, what was just discussed). State your interpretation briefly so the user can redirect if you're off, then proceed.

## Step 2. Establish the Code Anchor

Before spawning investigators, build the seed context inline: file paths and line ranges, key symbols (functions, classes, constants), the last few commits touching the target, PR numbers from merge commits (pattern `(#1234)` in the subject line), and any linked ticket IDs. Run `git blame -L <start>,<end> <file>` for last-touch commits, `git log --follow -p -- <file>` for full history with patches through renames, `git log --oneline -20 -- <file>` for recent commits with PR numbers visible, and `git log -1 --format=%B <commit>` to extract PR numbers. Then pull the PR bodies and discussion for any substantive commit: `gh pr view <number> --json title,body,author,createdAt,mergedAt,labels,closingIssuesReferences,comments,reviews`. This anchor goes to every investigator and to the synthesizer.

When the target is a result, the anchor also names the number and its records: our value with the task folder, job IDs, and tracker run IDs that produced it, and the published value with its paper version, table, and cell.

## Step 3. Spawn Parallel Investigators

**Default to the full parallel investigation.** The goal is a complete coverage map, not a minimal one. Document the null, don't skip the search.

### Discovery

Before spawning investigators, list the tools and MCP servers available in this session.

Map each available MCP to one evidence category:

1. Source control history
2. Issue / ticket tracker
3. Long-form documents
4. Real-time team chat
5. Cluster and job records
6. Run logs and failures
7. Experiment tracker
8. Published record

Source control is always available through git and `gh`. Four categories often need no MCP: cluster and job records through the scheduler's commands, run logs through the log files in the project and its `lab/` task folders, the experiment tracker through its CLI, API, or local files, and the published record through web access. Count a category as available when its source is reachable. For each MCP, classify using the MCP name, server instructions, tool names, and resource descriptors. If an MCP could fit more than one category, choose the one matching its primary evidence. Record ambiguous cases in the coverage map.

Spawn one investigator per category that has a matching MCP or other source, all at once so they run concurrently, each owning exactly one tool or MCP. Don't ask one agent to cover multiple MCPs. Role: `worker`.

Each investigator's prompt is `references/investigator-prompt.md` filled in, plus:
- the category playbook `references/sources/<source>.md` for the selected MCP or source, adapted from the examples in `references/source-playbook.md`
- `references/sources/incident-postmortem.md` **if the target code looks defensive** (null checks, NaN guards, retry or requeue logic, checkpoint resume, timeout handling, rate limiting, feature flags, egress guards, OOM handlers)
- the code anchor and the user's original question

### Investigator roster, one per available evidence category

Each category below is uniquely positioned to surface one shape of "why", shown after "Best at". Use it to know what to expect back, to name a gap when a category returns empty, and, only in the rare provably-irrelevant case, to justify a skip.

1. **Source control** (git history, `gh` for PRs, code comments, tests). Always spawn, the only guaranteed source. Best at *implementation-time rationale captured during review*.
2. **Issue / ticket tracker** (e.g. Linear, Jira, GitHub Issues, Plane, Shortcut MCP). Best at *the product or business forcing function*. Strongest when the why is external to engineering.
3. **Long-form documents** (e.g. Notion, Confluence, Google Docs, Coda MCP; lab notebooks and design notes). Best at *long-form design rationale*, written out before it becomes code.
4. **Real-time team chat** (e.g. Slack, Discord, Microsoft Teams, Mattermost MCP). Best at *real-time deliberation that never reached a doc*. Especially important when the source control, ticket, and doc paper trail is thin.
5. **Cluster and job records** (e.g. Slurm's `sacct` and `squeue`, PBS, LSF, a cloud job service, or a scheduler MCP; environment files such as `lab/ENVIRONMENT.md`). Best at *what a job actually ran on and how it ended*. Strongest when the target reacts to the machine (time limits, memory caps, preemption, checkpoint and resume) or when a result may depend on where it ran.
6. **Run logs and failures** (training and eval logs, crash traces, job output files, the run records in `lab/` task folders). Best at *the specific crashes, divergences, and warnings that motivated defensive or corrective code or settings*. Strongest for NaN guards, gradient clipping, lowered learning rates or batch sizes, retries, and other defenses, and for tracing a number to the run that produced it.
7. **Experiment tracker** (e.g. W&B, MLflow, TensorBoard, Aim, trackio, a results database). Best at *the logged configs and metrics that shaped a setting or a number*. Strongest for settings chosen from a sweep, metric-driven changes, and "where did this number come from" questions.
8. **Published record** (the paper and its versions, appendices, released code and configs, OpenReview discussion, errata, and the authors' issues). Best at *the authors' stated rationale for a method's design and the setting behind a reported number*. Strongest when the target implements or reproduces a paper, and for "why does our number differ from the paper?"

### When to skip an investigator

Only with an **explicit, written justification** that goes in the final Sources Consulted. Two valid reasons:

- **No MCP or other access is available for that category** in this environment. Flag it as a gap, not a choice: "Real-time team chat skipped. No matching MCP available, so the conversational record was not searchable."
- **The source is provably irrelevant**, not just "probably irrelevant." A high bar: "Run logs and failures skipped. Target is a build script that no training or eval run executes."

If your scope assessment suggests a single-commit trivial target where the PR description already contains the complete answer, you may answer inline **only after** confirming all eight available category searches would be redundant. Say so explicitly. This should be rare.

## Step 4. Synthesize

Spawn one synthesizer. Role: `judgment`. It gets:
1. The investigator findings, including any null results and any categories skipped with justification
2. The code anchor
3. The user's original question
4. The epistemics framework from `references/epistemics.md`
5. The synthesizer prompt template from `references/synthesizer-prompt.md`

## Step 5. Present

Present the synthesizer's output to the user. You may lightly edit for clarity or add context from the conversation, but **do not rewrite the confidence language**.

## Output Format

The structure is the one in `references/synthesizer-prompt.md`: The Question, The Code in Question, What We Found, What We Can Reasonably Infer, Competing Hypotheses, What We Don't Know, Sources Consulted, Confidence Summary. Adapt as needed, but keep the confidence separation intact, and keep Sources Consulted as one line per investigator, including the ones that returned nothing or were skipped, with the reason.

After Sources Consulted, if the user's `why` question is a precursor to changing this code or its settings, convert the lineage findings into a Preserve / Change / Avoid / Risk constraint set for planning the change.

## Common Failure Modes to Avoid

- **Recency bias**. Assuming the most recent commit is authoritative. The current shape is often the accretion of many earlier decisions. Trace back.

Sources: SOURCES.md entries `slurm-docs`, `slurm-mcp`, `hf-jobs`, `wandb-agent-docs`, `wandb-mcp-server`, `mlflow-docs`, `tensorboard-docs`, `trackio`, `arxiv-versions`, `openreview-docs`, `openreview-mcp`, `reclaim`, `sacrebleu-clarity`, `olmes`.

Adapted from pstack's `why` skill (https://github.com/cursor/plugins/tree/main/pstack, version 0.15.28), Copyright (c) 2026 Lauren Tan, MIT License: see `LICENSES/pstack.txt`. Changes for labstack are listed in `docs/pstack-port.md`.
