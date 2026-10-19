# labstack

labstack is an add-on for AI coding agents (Claude Code and omp) that makes the agent work like a good research assistant to a PI.

You give it a scoped research task, the way you would to a student or RA:

- "Find me the papers on contamination detection for LLM benchmarks."
- "Find the latest benchmarks for long-context retrieval, implement them, and run them on these two models. We have 2 A100s this week."
- "Reproduce Table 2 of this paper."

The agent does the work on its own, stops to ask you only when a choice is really yours, and hands back a short answer you can check.

labstack does not run research on its own. It does not pick topics, run overnight loops, or write papers end to end. You set each task; it does that task and returns.

## Why

Coding agents can search, read papers, write code, and run experiments. Left to themselves, they make the mistakes that waste a supervisor's time:

- **They invent things.** Citations that don't exist, numbers nobody computed, "tests pass" when nothing ran.
- **They quietly change the task.** When a paper's code won't run, they swap in a smaller model, fewer samples, or their own fix, and still call it a reproduction.
- **They grade their own work.** They report success from their own summary, and some will edit the scorer to make a number go up.
- **They ask badly.** Either a question at every step, or no question when one was needed (which benchmark counts, how much compute to spend).
- **They bury the answer** under logs and caveats.

labstack gives the agent a short set of rules and step-by-step playbooks that prevent these. They were built from about 2,300 external sources (papers, guides, skill collections, lab practices), listed in [SOURCES.md](./SOURCES.md).

## How it works

You start a task with **lab-mode**. It matches your request to a playbook and follows it.

| You ask | Playbook | What you get back |
|---|---|---|
| "Find me the papers on Y", "what's new on Y since March?" | Literature | The answer first, then the papers grouped by role (closest work, foundations, surveys) with one line each on why they matter, the 3-5 to read first, and what was searched. Every reference is looked up, never written from memory. |
| "Find the latest benchmarks for X and run them" | Benchmarks | A shortlist of the benchmarks the field uses now, each with its state (saturated? contaminated? maintained?). You pick. Then a results table: our score, the published score for the same setup, cost, and a few example items. |
| "Reproduce Table 2 of paper Z" | Reproduction | A table per target number: the paper's value, ours, the gap, and a verdict (matched, near, not reproduced). Any change from the original setup is listed, and none is made without your OK. |

Anything else runs under the same rules without a playbook.

### What you decide, and what the agent decides

The agent decides routine things itself: how to search, how to write the code, how to debug its own mistakes. It asks you only when a choice changes what the result means or what it costs:

- **Selection.** Which papers, benchmarks, or baselines count.
- **Yardstick.** The metric and what counts as success, set before results exist.
- **Spending.** Compute or money beyond the budget you gave. A budget in your request ("2 A100s this week") already approves runs inside it.
- **Deviations.** Any change from the plan or from the original paper's setup.
- **Claims.** What gets written under your name.

Questions come together in one message, numbered, each with a sentence of context and a recommended option. You can answer "all recommended except 2".

Example of a question it sends:

> **3. Qwen2.5-7B above 32K tokens.** The model natively handles 32K; its model card says to enable YaRN scaling for longer inputs. (a) Native up to 32K, YaRN only above, as the card says. **Recommended.** (b) YaRN everywhere: one config, but short-context scores may drop. (c) Stop Qwen at 32K: cheapest, but its 128K claim goes untested.

### The rules behind it

Six short principles, each its own skill:

1. **Settle what "done" means before results exist.**
2. **The agent does the work and judges it; the supervisor decides what changes meaning or cost.**
3. **No silent substitution.** If something won't run or match, say so; "not reproduced" is an acceptable answer.
4. **Claims rest on records.** Every number and citation traces to a log, a file, or a looked-up reference. The agent never grades itself.
5. **Answer first, in the supervisor's terms,** in about one screen.
6. **Keep the process as small as the request.** One agent by default; no extra runs or checks you didn't ask for. The agent proposes extras in one line.

## Install

Claude Code:

```
/plugin marketplace add tosunlab/labstack
/plugin install labstack@labstack
```

omp:

```
/marketplace add tosunlab/labstack
/marketplace install labstack@labstack
```

Then give the agent a task and say "lab mode", or call the skill directly (`/labstack:lab-mode` in Claude Code, `/skill:lab-mode` in omp).

By default every part of the work runs on your current model. To use different models for different roles (for example, a strong model for judgment and a cheaper one for code), run `setup-labstack` once.

## What's inside

```
skills/
  lab-mode/              entry point: rules for asking, autonomy, hand-back
    playbooks/           literature.md, benchmarks.md, reproduction.md
  principle-*/           the six principles
  setup-labstack/        pick a model per role (optional)
docs/harness/            how the skills map onto Claude Code and omp
SOURCES.md               the external sources the skills cite
```

## Status

Early. lab-mode, three playbooks, and the six principles are written and have been tried on test requests in both harnesses. They have not yet been used on real research tasks.

### Next steps

Each step is a GitHub issue with sub-issues for the pieces of work.

1. **Use it on real requests** ([#1](https://github.com/tosunlab/labstack/issues/1)). Two or three real literature, benchmark, and reproduction tasks, then fix what goes wrong. Nothing else changes before this.
2. **Test lab-mode itself** ([#6](https://github.com/tosunlab/labstack/issues/6)). Trial tasks with traps: a decision that should go to the supervisor, or a tempting action the request doesn't allow. Check what the agent actually did, and whether its questions were needed. On real tasks, track how much of the supervisor's time each hand-back takes to read and correct.
3. **More playbooks** ([#12](https://github.com/tosunlab/labstack/issues/12)): running experiments and judging results, writing, review (only when asked for), proofs, ideation, debugging, figures and slides.
4. **Research versions of general agent skills** ([#20](https://github.com/tosunlab/labstack/issues/20)) adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack): explaining how something works, finding why something happened, an independent review run only when the supervisor asks for one, and others.
5. **More harnesses** ([#33](https://github.com/tosunlab/labstack/issues/33)), such as Codex.

### What's missing

These are areas where the sources say little, so the playbooks say little ([#36](https://github.com/tosunlab/labstack/issues/36)):

- **Benchmarks outside LLM evaluation.** Vision, RL, systems, and science benchmarks.
- **Cost estimates for API runs.** Predicting token and API spend before asking for a budget.
- **Retired models.** Reproducing a paper whose hosted model no longer exists.
- **Gated data and logins.** Getting access to restricted datasets or models through the supervisor.
- **Search completeness.** How to tell when a literature search is complete enough.
- **Figures for the supervisor.** Which table or plot to hand back after a run.
- **Fields outside ML.** Wet lab, field studies, qualitative research.
- **Proof that it saves time.** No source measures this yet; step 2 is how we'll find out.
- **Enforced rules.** Rules such as "never edit the raw data" or "never edit the scorer" are written instructions. Making the harness block them (permissions, hooks) is up to each project.

## Contributing

Install the local hooks once per clone:

```bash
pipx install pre-commit   # or: uv tool install pre-commit
pre-commit install
```

The hooks run on every commit:

- **privacy**: no personal absolute paths, local working material, or archives.
- **portability**: shipped skills contain no harness-specific tool names, config paths, or model names.
- **secrets**: gitleaks and private-key detection.
- **hygiene**: file size, whitespace, line endings, YAML and JSON syntax.

Run every hook against the whole tree with `pre-commit run --all-files`.
