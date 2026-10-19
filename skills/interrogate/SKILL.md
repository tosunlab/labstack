---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"stress test this result\", \"find blind spots\", or \"tear this apart\". Multiple LLM reviewers challenge code changes, results, analyses, or drafts from independent angles. Run only when the user asks for it."
---

# Interrogate

Spawn one reviewer per configured model to adversarially review code changes, a result, an analysis, or a draft. The adversarial signal comes from model diversity, not assigned personas. The deliverable is a synthesized verdict. Do NOT auto-apply changes.

## Step 1, Scope

Identify what to review from context:

- If the user points at specific files, a diff, a result, or a draft, use that.
- If on a feature branch, run `git diff main...HEAD` (or the appropriate base branch) for the full changeset.
- If the user's message references recent work, gather the relevant files.

Package the diff or file contents with any surrounding context files the reviewers need to understand the code. For a result, an analysis, or a draft, include the records behind it (run outputs, logs, configs, and the code that produced the numbers), so reviewers check the claims against them, not only against the prose.

## Step 2, Intent

Before spawning reviewers, state the intent in one clear paragraph from the user's message, commit messages, the PR description if one exists, and the artifact. For a result, an analysis, or a draft, the intent is what it claims or is meant to show; leave out any judgment of whether it succeeds. If you're unsure about the intent, ask the user before proceeding.

## Step 3, Spawn Reviewers

Spawn all reviewers at once as read-only subagents. Use the `panel` model from the labstack model config (lab-mode, Roles), one reviewer per entry, labeled Reviewer A, B, and so on to match the entry count. A missing config or role means the session model. If a configured model is unavailable, use the session model and say so. With fewer than two panel entries, run two reviewers on the session model, and state in the output that they share one model family, so their agreement is weaker evidence.

Read `references/reviewer-prompt.md` and fill in the same template for every reviewer with the stated intent, the artifact, and the lenses that fit it: the rubric from `references/rubric.md` for code, including the code behind a result; the code-quality lens from `references/code-quality-review.md` only for code meant to be kept (a library, a released replication package), not for throwaway analysis scripts; and the research lens from `references/research-review.md` for a result, an analysis, or a draft. Match each subagent's effort to the job where your harness lets you set it.

## Step 4, Synthesize

As results come back, build a unified picture. Parse every reviewer's findings. Merge findings that describe the same issue differently, and note which models raised each one. Findings two or more models raised independently are the highest signal. Read a lone model's finding, but weight it accordingly. Note disagreements. If one model flags something and another explicitly says the opposite, that is context for the verdict.

## Step 5, Lead Judgment

You are the lead reviewer, a pragmatic senior researcher, not a neutral aggregator. Read `references/lead-judgment.md` for the full framework. Put every finding in one of four buckets, with the model(s) that raised it and a one-line rationale.

- **Act on**. Real issues affecting correctness, security, or maintainability given the actual goals. They would change the verdict or block the claim.
- **Consider**. Legitimate, but you're not sure they outweigh the cost of addressing them now. Worth the user's attention.
- **Noted**. Technically valid but not actionable. Context-dependent, premature optimization, or low-impact at this stage.
- **Dismissed**. Wrong, nitpicky, or missing context, with a brief reason.

## Output Format

### Intent
> [The stated intent paragraph from Step 2]

### Reviewers
- Reviewer [label]: [model name], [N findings] (one bullet per reviewer)
- [If all reviewers share one model family: say so, and that their agreement is weaker evidence.]

### Act On
[Each: description, which models raised it, why it matters.]

### Consider
[Each: description, which models raised it, the tradeoff.]

### Noted
[Brief list.]

### Dismissed
[Each with a brief rationale.]

### Agreement Map
[Where models agreed and diverged, and what that pattern tells us.]

Sources: SOURCES.md entries `llm-self-preference`, `ai-reviewers-expert-audit`, `mlr-bench`.

Adapted from pstack's `interrogate` skill (https://github.com/cursor/plugins/tree/main/pstack, version 0.15.28), Copyright (c) 2026 Lauren Tan, MIT License: see `LICENSES/pstack.txt`. Changes for labstack are listed in `docs/pstack-port.md`.
