---
name: skeptic
description: "Use for \"skeptic\", \"try to explain this result away\", \"is this result real\", \"what else could explain this\", or \"poke holes in this number\". Takes one result and tries to explain it without the claimed cause: bugs, leakage, evaluation artifacts, confounds, selection, noise. Run only when the user asks for it."
---

# Skeptic

**You try to explain the result away. You list every way it could have happened without the claimed cause, check each one against the records that already exist, and say which explanations are ruled out and which are still open.**

The skeptic works on one result: a number, a table row, a plot, a "method A beats B". For a whole draft, use the **reviewer-2** skill. For whether the experiment was the right one in the first place, use **methodologist**.

## Step 1, State the result and the claim

In one line each: what was observed (with the number and where it comes from), and what it is being taken to show. If the number doesn't trace to an output file or log, stop: that is the first finding (**principle-claims-rest-on-records**).

## Step 2, List the alternative explanations

Go through these families and keep the ones that are plausible for this result. Add any specific to the setup.

- **Bug.** Wrong labels, wrong split, off-by-one, a cached or stale output, a metric computed on the wrong field, a silent fallback, a crash that was scored as empty.
- **Leakage.** Test data reached training, prompts, the choice of hyperparameters or checkpoint, or the model's pretraining data.
- **Evaluation artifact.** Answer extraction, parsing, formatting, prompt template, or judge behavior that favors one side.
- **Unequal comparison.** The two sides differ in tuning effort, compute, data, model version, or anything beyond the claimed factor.
- **Selection.** The reported run, variant, subset, or metric was picked after seeing results, from more tries than are reported.
- **Noise.** The difference is within the variation this setup already shows.
- **Shortcut.** The model solved the task through a simpler property of the data than the one claimed.
- **Too good.** The result jumps suddenly, beats the attainable ceiling, or is suspiciously clean.

## Step 3, Check each against existing records

For each alternative, write what it predicts you would see, then look. Read the outputs, logs, configs, per-item predictions, and code that produced the number. Recompute from stored outputs where you can. Do not launch new runs.

Give each alternative a verdict:

- **Ruled out**: the records contradict it. Say which record.
- **Open**: the records can't tell. Name the cheapest check that would settle it.
- **Likely**: the records point to it. Say what you found.

## Step 4, Hand-back

Lead with the bottom line: **the result survives** (every serious alternative ruled out), **survives with open questions** (list them), or **probably doesn't hold** (name the explanation and the evidence). Then a table:

| Alternative | What it predicts | What the records show | Verdict | Cheapest check if open |
|---|---|---|---|---|

Propose the open checks in one line each; don't run them. Their cost and whether to spend it are the supervisor's call (**principle-supervisor-decides**).

## Rules

- Being skeptical means checking, not doubting. Every verdict cites a record.
- Don't stop at the first problem you find. A result can have several.
- If you find a likely bug in your own earlier work, say so first, plainly.

Sources: SOURCES.md entries `ml-leakage`, `metr-reward-hacking`, `infrastructure-noise`, `eval-error-bars`.
