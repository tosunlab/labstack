---
name: show-me-your-work
description: "Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away. Run only when the user asks for it."
---

# Show me your work

Keep one canonical log.

## The format

A single TSV file, one row per decision. Cells stay single-line. Evidence is a pointer, not prose.

Copy `references/decision-log-template.tsv` (the header row) to start a clean log. Columns:

- **ts.** ISO8601 timestamp.
- **phase.** The phase or workstream.
- **decision.** What was chosen or done, one line.
- **why.** The reason in plain words. If a principle drove it, say it plainly, not as a jargon tag.
- **evidence.** A link or path that proves it: commit SHA, job id, `file:line`, or an artifact, trace, or screenshot path. Never a paragraph.
- **result.** The outcome or predicate state: `tests green`, `reverted`, `within tolerance`, `INCONCLUSIVE`, `open`.

An example, plain-spoken so a reviewer reads it at a glance.

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, 6 cells of Table 2 and roughly 40 GPU-hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	targets	wrote down the paper's Table 2 numbers before running anything	so we can compare ours against the paper's and catch any gap	targets.tsv, paper v2 Table 2	saved 6 targets with the agreed tolerance
2026-05-24T11:15:00Z	baseline	ran the paper's baseline without changing its config	match the original exactly so any gap means something	commit 7c21e0a, job 4815162	72.0 vs 72.1 reported, within tolerance
2026-05-24T12:30:00Z	baseline	threw out a helper's eval numbers because its output files were empty	checked the real files instead of trusting its summary	runs/helper-eval/ (empty)	discarded, tightened the instructions for next time
```

## Logging a row

Write each entry the way you'd tell a teammate what you did. Plain words, concrete actions, no AI speak or abstract jargon (the **principle-answer-first** skill applies to log text too).

Use the helper `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`. It stamps `ts`, writes the header on first use, strips stray tabs/newlines, and prefixes any cell starting with `=`, `+`, `-`, or `@` with a single quote. A bare `printf` appending a row works too, but mind those same bytes if cells come from generated or user-supplied text.

Log decision points and checkpoints, not every action: a fork chosen, a unit completed with its verification result, a pivot or revert with its trigger, a blocker surfaced, a gate fixed. For loop runs, one row per iteration. Skip the trivial and self-evident.

A run is one agent conversation, including its later turns and any summary of it. A pickup, a replacement agent, or a new chat starts a new run. When a run adds to a log that already has rows, its first row has phase `start`, and so does its first row after another run's `start` row. So a run that comes back to a log in a later turn first reads the log's last rows to see whether another run wrote since. A `start` row names the `ts` range of the rows before it that this run did not write, and its evidence names this run, such as its agent id. Use phase `start` for nothing else.

## Where it lives

By default the log is a working artifact, not committed. Keep it at `lab/<date>-<task>/decisions.tsv`, in the task folder lab-mode defines, and leave it out of git.

Commit it only when the work is ambitious enough that a reviewer needs the trail to trust the result.

## Rules

- Append-only. A wrong call gets a new row that supersedes it. Never edit or delete history.
- Prefer evidence produced by committed scripts over hand-made one-offs (the **correct** skill).

## Audit the log against the transcript

At the end of the run, before handing back, check the log told the truth. Read this run's transcript in this harness's session transcripts (where they live: `docs/harness/<harness>.md`, Transcripts). Don't glob across other projects' transcripts. That reads unrelated private chats. Walk this run's rows against what actually happened. Each stretch of them begins at one of this run's `start` rows, or at the first row if this run created the log, and ends at the next `start` row of another run:

- Check that every row maps to a real decision or action.
- Check that each row's evidence resolves and shows what the row claims.
- A fork, pivot, or abandoned approach that shaped the work but isn't logged is a gap. Add it.

Correct the log, not the story. The audit never edits or removes a row, even an invented one. When a row records neither a real decision nor a real action, or its claim or evidence is wrong, add a row that supersedes it with what actually happened and a pointer that resolves. This audit does not check rows outside this run's stretches. If this run's own work shows one of them is wrong, supersede it like any wrong call.

## Cross-model review of the trail

Run this only when the user asks for it. When asked, spawn a subagent on a different model family from the one that did the work. Self-review is not a substitute. The subagent reads the audit trail and the run's transcript, then flags what the user should pay attention to. Not a redo of the work, a scan for what's suboptimal or risky. Use a `panel` model from the labstack model config (lab-mode, Roles) whose family differs from the one that did the work, else the `judgment` model. A missing config or role means the session model. If a configured model is unavailable, use the session model and say so. Match each subagent's effort to the job where your harness lets you set it.

- Decisions logged with weak or absent evidence.
- Verification steps skipped or claimed without proof in the transcript.
- Choices that look risky in hindsight (premature, scope-creeping, papering over a symptom).
- Gaps the user would otherwise miss on a casual skim.

When this review ran, the reply ends with an "Attention" section. Lead with the reviewer's model on its own line (`reviewed by <model>`), then list each flag pointing to specific rows or moments. "No flags" is a valid value. The model name is not. If the reviewer shares the working model's family, say so on that line; a same-family review is weaker evidence.

## Reviewing the trail

Read top to bottom, follow the evidence pointers, spot-check. GitHub renders a committed TSV as a table. `column -s$'\t' -t decisions.tsv` renders it in a terminal.

## Composing this skill

Other skills route their audit trail here instead of inventing one. Reference it by name and let it own the format. Don't restate the columns.

Sources: SOURCES.md entries `llm-self-preference`.

Adapted from pstack's `show-me-your-work` skill (https://github.com/cursor/plugins/tree/main/pstack, version 0.15.28), Copyright (c) 2026 Lauren Tan, MIT License: see `LICENSES/pstack.txt`.
