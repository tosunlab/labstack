---
name: figure-it-out
description: "Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions. Use for /figure-it-out or 'figure it out'."
---

# Figure it out

When the task matches no playbook, design one. The deliverable before any code is the workflow itself: a sequence of phases that scales rigor to the task, runs the scientific method, and leaves a decision trail a human can audit after stepping away.

## Start

Open a todolist whose first item is to read the Principles section of the **lab-mode** skill. Then add the phases below as todos.

## Phase A: Frame

Ground first, then commit. Don't start the run until you can state:

- The definition of done as a falsifiable predicate (the **principle-settle-done-first** principle skill).
- Scope, quantified: rough units and effort, plus the blockers grounding surfaced.
- The rigor level, matched to the request (the **principle-size-the-process** principle skill). One-way doors and high blast radius get more. Reversible low-stakes steps get less. Rigor is gates and artifacts, not "try harder". Propose in one line any check the supervisor did not ask for.

Present the framing and tradeoffs before committing to a long run. Reversible work proceeds (the **principle-supervisor-decides** principle skill, which lists the points where you ask), but a multi-hour run earns one checkpoint.

## Phase B: Design the workflow

Decompose into atomic, independently-landable units. Sequence riskiest-unknown-first. Scaffold and verification come before results (the **principle-size-the-process** principle skill).

- Settle the done criterion before the work (the **principle-settle-done-first** principle skill), with the baseline captured from the pre-change state, so the check reads as "old value vs new value". A baseline measurement that costs compute is part of the plan the supervisor approves.
- For one-way-door design decisions, propose the **arena** skill in one line; it runs only when the supervisor asks. Skip it for mechanical work whose shape is already concrete. A second arena over a settled design is over-engineering (the **principle-size-the-process** principle skill).
- Decide what fans out. Parallelize only across seams, and give each worker its own output folder (`lab/<date>-<task>/worker-<n>/`) and, for code edits, its own worktree or branch; never let two write the same file. Don't over-fan. Match each subagent's effort to the job where your harness lets you set it.
- Write the designed phase list down. That list is what the human reviews.

Then execute the design. Add its steps to the todolist as concrete items between the Phase C and Phase D entries. Run each under the Phase C loop discipline, and weave the Phase D log through them, a row as each step lands, rather than saving the whole trail for the end.

## Phase C: Run the loop

Each unit is an experiment. State the hypothesis, make the smallest change, measure against the predicate on the real artifact, keep it if it advanced, revert it if it didn't. Verify each unit before starting the next instead of batching checks at the end. The loop stays inside the one scoped task; a change of direction goes to the supervisor.

- Verify by inspecting the artifact, never a self-report. When something passes too easily, suspect the observation method before the system.
- Check delegated work against its artifacts, not the worker's report; a separate judge runs only when the supervisor asks for one. If a worker games the gate, reset and harden the contract. If your implementation of the gate is wrong, fix it in its own change rather than routing around it, and tell the supervisor. Changing the agreed done criterion or deviating from an original protocol goes to the supervisor before use.
- A verdict is VERIFIED, NOT VERIFIED, or INCONCLUSIVE. Inconclusive is not a pass. Don't hide a negative.

## Phase D: Keep the audit trail

Log the run via the **show-me-your-work** skill. The trail goes in the task folder, `lab/<date>-<task>/`, so the supervisor can read it next to the results. The trail plus the results and the diff is what lets the human come back and trust the work.

## Phase E: Verify and hand back

Check the whole against the Phase A predicate on the real artifact, not just the harness. Offer, in one line, to encode any recurring correction as a gate, a lint rule, a check, or a script (the **correct** skill).

**Reply:** the playbook you designed, the rigor level and why, the decision-trail path, what's verified against the predicate, and what's still open.

Adapted from pstack's `figure-it-out` skill (https://github.com/cursor/plugins/tree/main/pstack, version 0.15.28), Copyright (c) 2026 Lauren Tan, MIT License: see `LICENSES/pstack.txt`. Changes for labstack are listed in `docs/pstack-port.md`.
