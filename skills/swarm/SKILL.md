---
name: swarm
description: "Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration. Run only when the user asks for it."
---

# Swarm

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices (papers, benchmarks, configs, or commits), race N workers on identical briefs, or mix both. A race duplicates spend, so race only when the supervisor asked for one. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
4. Pick the worker model. Use the `worker` model from the labstack model config (lab-mode, Roles). A missing config or role means the session model. If a configured model is unavailable, use the session model and say so. For a model race, name each arm's model up front. Match each subagent's effort to the job where your harness lets you set it.
5. Give each worker its own writable output (`lab/<date>-<task>/worker-<n>/`) when it writes. When workers verify or measure, each brief names the exact inputs (commit SHAs, data version, paper version). A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Spawn all N workers at once on the step 4 model.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the exact inputs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with the table, issue one-liners, gaps or dropouts, and the race rule when used.

Adapted from pstack's `swarm` skill (https://github.com/cursor/plugins/tree/main/pstack, version 0.15.28), Copyright (c) 2026 Lauren Tan, MIT License: see `LICENSES/pstack.txt`. Changes for labstack are listed in `docs/pstack-port.md`.
