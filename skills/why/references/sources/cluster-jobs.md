# Cluster & Job Records

## What this source contains

The scheduler holds the record of what actually ran, as opposed to what the job script, the config, or the paper says should have run.

- **Accounting records.** One row per job and job step: submit, start, and end times, elapsed time, nodes, allocated resources (GPUs, CPUs, memory), peak memory, restarts, state, and exit code. On Slurm this is `sacct`, which keeps finished jobs. `squeue` shows pending, running, and completing jobs by default; other states can be selected with `--states`.
- **Job states.** How each job ended: completed, failed, cancelled, timed out, out of memory, preempted, node failure, requeued. A `TIMEOUT`, `OUT_OF_MEMORY`, or `PREEMPTED` state is often the forcing function behind a smaller batch, a checkpoint interval, or a resume path.
- **The submit line.** The full command a job was submitted with (`SubmitLine`) and the directory it ran in (`WorkDir`). Command-line options and input environment variables override the job script's `#SBATCH` lines, so the script alone may not show what ran.
- **The scheduler's lines in job output files.** By default `slurm-<jobid>.out`, or `slurm-<arrayjob>_<index>.out` for an array, in the job's working directory unless `--output` named another path. The scheduler's own messages there (time limit, out-of-memory kill, node failure) belong to this source. The program's output belongs to the run-logs investigator.
- **Environment files.** `lab/ENVIRONMENT.md` records the machine, scheduler, partitions, GPUs, storage, and software, each fact marked verified with a date or unverified. A job may also have written a module list or an environment export.

## How to search it

Use the scheduler's commands on the cluster, or a scheduler MCP if one is available. Read only: never submit, cancel, hold, requeue, or update a job.

1. **Start from known job IDs.** The task folder's run records, the tracker's run metadata, and log file names often carry them.

   ```bash
   sacct -j <jobid> --parsable2 \
     --format=JobID,JobName,Partition,Submit,Start,End,Elapsed,State,ExitCode,NodeList,AllocTRES,MaxRSS,Restarts,SubmitLine,WorkDir
   ```

   Add `-D` (`--duplicates`) to see every record of a requeued job. By default only the most recent record is shown.

2. **Search a time window when you have no IDs.** Without `--jobs` or `--state`, `sacct` searches only since midnight today, so set the window. Bracket the target's change date.

   ```bash
   sacct -S <start> -E <end> --name=<jobname> -X --parsable2 --format=JobID,JobName,Start,End,Elapsed,State,ExitCode,NodeList,AllocTRES
   ```

   `-X` shows one row per job instead of every step, but reports utilization such as `MaxRSS` as zero. Drop it for memory questions. For a non-root user `sacct` shows only your own jobs; pass `--user <name>` for a labmate's.

3. **Pending and running jobs.** `squeue -j <jobid>` or `squeue -u <user>`. A pending job's reason column says why it is waiting.

4. **The machine.** Read `lab/ENVIRONMENT.md` and compare it with the job's `Partition`, `NodeList`, and `AllocTRES`. A run on different hardware or a different partition than the run it is compared with is a finding.

5. **Scheduler MCPs and other schedulers.** A Slurm MCP (for example `slurm-mcp`, with job-status, job-log, and job-resource tools) covers the same reads; use none of its submit or cancel tools. For PBS, LSF, or a cloud job service, use its job list, status, and log commands. On Hugging Face Jobs: `hf jobs ps -a`, `hf jobs inspect <job_id>`, `hf jobs logs <job_id>`.

## What good evidence looks like here

- A job that ended `OUT_OF_MEMORY` or `TIMEOUT` shortly before the commit that lowered the batch size, raised the time limit, or added checkpointing
- Repeated `PREEMPTED` or `REQUEUED` records, or a nonzero `Restarts` count, before resume logic was added
- A `SubmitLine` whose command-line options differ from the job script or the config in the repo
- The run behind a number placed on a different GPU type, node count, or partition than the run it is compared with
- An environment-file entry, dated before the change, that records the constraint the code works around (a quota, a time limit, no internet on compute nodes)

## Common pitfalls

- **Default time window.** `sacct` with no `--jobs`, `--state`, or `--starttime` shows only today's jobs. An empty result there is not "no jobs".
- **Hidden jobs.** Another user's jobs need `--user`, and a site may hide other users' accounting entirely. A job missing from `sacct` that you know ran is a gap, not a null result.
- **`-X` zeros.** Allocation-only output reports utilization as zero. Read the steps before claiming a job used no memory.
- **Requeues collapse.** Without `-D`, a requeued job shows only its last record, and the submit time resets on requeue.
- **Site-local names.** Partitions, accounts, QoS, and GPU names are site-specific. Read them from the record, never from memory.
- **Correlation is not causation.** A failed job before a commit and clean jobs after is suggestive, not definitive. Other changes may have landed in the same window.

## What to return

For each relevant job:
- Job ID (with array index or step), job name, user
- Partition, nodes, allocated resources, and peak memory if read
- Submit, start, and end times, elapsed time, state, exit code, restarts
- The submit line or job-script options that bear on the question (verbatim)
- The exact command or MCP call you ran, with its time window
- Temporal correlation with the target's change date
- Relevance + strength: direct / circumstantial / weak

Sources: SOURCES.md entries `slurm-docs`, `slurm-mcp`, `hf-jobs`.
