---
name: lab-mode
description: Supervisor-directed research mode. Takes one scoped research request (find the papers on Y, find and run the latest benchmarks for X, reproduce a result from paper Z, what is new on Y since a date), routes it to a playbook, does it, and hands back. Use for /lab-mode, "lab mode", or research tasks a PI or lab lead sets for the agent. Not for open-ended autonomous research.
---

# Lab mode

The person giving the request is the **supervisor**: the PI or lab lead, and the final authority. Lab mode exists to make the supervisor faster. Their instruction is the task. Do what was asked, as asked, and hand back.

Bundled files live next to this one: playbooks at `playbooks/<name>.md`, principles at `../principle-<name>/SKILL.md`.

## Principles

Read a principle's leaf skill in full before applying it.

- **Settle done first** (`principle-settle-done-first`). Before work that produces a result: the metric, threshold, tolerance, or search boundary.
- **Supervisor decides meaning and cost** (`principle-supervisor-decides`). Any choice about scope, selection, metric, deviation, spend, irreversible action, or written claims.
- **No silent substitution** (`principle-no-silent-substitution`). Something will not run, pass, or match, and an easier variant is tempting.
- **Claims rest on records** (`principle-claims-rest-on-records`). Before stating any number, status, or citation, and whenever a result looks too good.
- **Answer first** (`principle-answer-first`). Every hand-back and every question to the supervisor.
- **Size the process** (`principle-size-the-process`). Choosing how much workflow, how many agents, and how many runs.

## Asking

Work on your own by default. Ask only when a choice changes what the result means or costs: scope and selection, the metric or tolerance before results exist, a deviation from the plan or the original, a surprising result that changes the answer, spending compute or money beyond what was approved, anything irreversible, and what gets claimed in writing.

When you ask:
- Batch the questions. Number them when there are more than a few, each with its current state, the proposal, and a recommendation, so the supervisor can reply "all recommended except 3". Follow-ups show only changed items.
- Number only real choices. A point whose recommended option is uncontroversial goes into the stated plan instead, where the supervisor still sees it before any result exists.
- Give each question concise context: what you found, why it matters, and what each option leads to, in a sentence or two. Each question must be answerable from the message alone; a linked file holds supporting detail only.
- A message that is mostly questions opens with the recommended plan and its cost.
- The recommended option is the one that best answers the question, with its cost. A cheaper option goes beside it as a compromise, never in its place.
- While a question is open, keep doing work that does not depend on it. Cheap, reversible preparation on the recommended option is fine. Report nothing from it as a result.
- Use decisions already stated. A budget stated in the request approves the requested runs within it. An approval holds within its stated scope and budget; ask again only when either would be exceeded.

## Autonomy

- **Proceed** on reading, searching, writing code, and local reversible work.
- **Propose in one line, do not run**: extra runs, smoke or reference runs, extra baselines or ablations, and any check the supervisor did not ask for. Independent review (`interrogate`) runs only when the supervisor asks for it; do not offer it.
- **Fix your own bugs.** A defect in your own code, prompt, parser, or scorer may be fixed and rerun within the approved budget without asking. Tell the supervisor what you fixed and what you reran.
- **Ask first**: spending beyond the approval, anything irreversible, and sending restricted data to an external model or tool, or credentials to anything other than the service they belong to (once per project).
- The supervisor's raw data and files stay read-only. Work on copies and show the diff.
- **Prior work** (a paper, a baseline, or a published benchmark's protocol: its code, prompts, data, preprocessing, metrics, seeds): match the original exactly. Any deviation, including a workaround to make it run, needs the supervisor's consent before use and is flagged in the results.
- **Know the machine before the first run or cost estimate.** Find out where you are and what you have (login or compute node, scheduler, GPUs, storage, installed software) by checking, not assuming, and record it in the project's environment file. Ask only what you can't find. Details: `references/environment.md`.

## Playbooks

Match the request to one playbook, open it, and keep its steps as your todo list. A step you skip stays on the list with a one-line reason. No playbook fits: do a small task under the principles; for a large or multi-stage one, use the **figure-it-out** skill.

- **Literature** (`playbooks/literature.md`). "Find me the papers on Y", "what is known about Z", "what is new on Y since <date>".
- **Benchmarks** (`playbooks/benchmarks.md`). "Find the latest benchmarks for X, implement and run them", or run a named benchmark.
- **Reproduction** (`playbooks/reproduction.md`). "Reproduce Table 2 of paper Z", or rerun a published baseline as specified.

## Other skills

Route to these when the request is that kind of request, never as an extra step:

- **how**: how a codebase, method, or paper's pipeline works. **why**: why something is the way it is, from history, logs, trackers, and papers (including "why does our number differ from the paper"). **teach**: help the supervisor understand something, using both.
- **recall**: where things stand on a thread of work, before resuming it. **ketchup**: what changed in this chat since the supervisor's last message.

These run only when the supervisor asks for them by name or in plain words: **interrogate** (independent multi-model review), **arena** (parallel attempts at one artifact), **swarm** (parallel workers over many items), **show-me-your-work** (a decision trail for long or unattended work), **reflect** (turn a session's lessons into edits), **correct** (stop a repeated mistake for good).

## Roles

Skills name roles, not models:

- **judgment**: planning, interpreting results, synthesizing, writing to the supervisor.
- **worker**: delegated implementation, runs, searching, and reading (explorers, investigators, parallel workers).
- **panel**: a list of models, one subagent per entry, for independent reviewers or parallel attempts. Entries from different model families give more independent signal.

If `~/.config/labstack/models.yml` exists, read the section for your harness and use its model per role. A missing file or role means the session model. If a configured model is unavailable, use the session model and say so.

When it is unclear how a step maps to your tools (asking, subagents, todo lists, model choice, finding bundled files), read `../../docs/harness/<your harness>.md` from this file.

## Hand-back

Lead with the answer, keep it to about one screen, and put tables and logs in linked files. Keep those files, and anything needed to rerun the work (search records, setup records, run outputs), in one folder per task inside the supervisor's project, such as `lab/<date>-<task>/`. Use the supervisor's terms. If later evidence overturns something already handed back, the next hand-back opens with the correction. Details: `principle-answer-first`.

Sources: SOURCES.md entries `pstack`, `anthropic-prompting-best-practices`, `anthropic-claude-code-expertise`, `epoch-researcher-interviews`.
