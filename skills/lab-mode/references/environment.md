# Know the compute environment

Before the first run or cost estimate, find out where you are and what you have. Look it up; do not assume it. Agents that guess invent scheduler flags, run heavy work on login nodes, fill quota-limited home directories, and size cost estimates for hardware that is not there.

## 1. Read what is already known

If the project has an environment file (`lab/ENVIRONMENT.md`), read it first. Trust facts marked verified and recent; recheck anything unverified, old, or contradicted by what you see.

## 2. Check, don't guess

- **Where you are.** Hostname, OS, container or VM, and whether this is a login node or a compute node.
- **Scheduler.** Whether there is one (Slurm, PBS, LSF, a cloud job service, or none). For Slurm: partitions, accounts, QoS, time limits, and GPU types and counts per partition (`sinfo`, `sacctmgr`, `scontrol show partition`).
- **Hardware.** GPU model, count, and memory; CPU; RAM. On a cluster, the compute nodes, not the login node.
- **Storage.** Home, scratch, and project paths; quotas and free space; what is wiped and when.
- **Software.** Module system, Python and package manager, CUDA driver and toolkit, and the versions of the tools the task needs. Check `--help` and versions instead of trusting memory.
- **Network and access.** Internet on compute nodes, gated models or datasets, credentials already present (check that they exist; never print them).
- **Cost.** On rented or cloud compute: the price per hour and what keeps billing when idle.

## 3. Record it

Write what you found to `lab/ENVIRONMENT.md` in the supervisor's project: one line per fact, each marked verified with the date or unverified. Later tasks reuse it.

## 4. Ask only what you can't find

Batch these with the task's other questions: which account or partition to charge, which machine to use when there are several, whether shared resources may be used.

## Rules

- No heavy work on a login node. Use the scheduler.
- Validate a job script with the scheduler's dry run (for Slurm, `sbatch --test-only`) before submitting.
- Set time limits explicitly from your estimate; platform defaults kill long jobs.
- Write results and checkpoints to persistent storage, never only to the node or VM that will be wiped.
- Base every cost estimate on the hardware you found.

Sources: SOURCES.md entries `nersc-ai-coding-tools`, `hpc-skills`, `slurm-mcp`, `aalto-hpc-agents`, `usc-carc-agents`, `hf-jobs`, `modal-checkpointing`.
