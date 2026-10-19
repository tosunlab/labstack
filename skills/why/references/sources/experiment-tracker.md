# Experiment Tracker

## What this source contains

The tracker holds the logged record of each run: the configuration it ran with and the metrics it produced, as opposed to what the config file in the repo says today.

- **Run config.** Hyperparameters and settings logged when the run started. Strong evidence of what a run used, where the code logged the values it actually applied.
- **Metric histories and summaries.** Per-step curves and final values. For "where did this number come from", the summary value of the run that produced it.
- **Run metadata.** Start time, state, tags, and the commit. W&B records the git commit for runs started inside a repo (and a diff unless code saving is off). MLflow tags runs with `mlflow.source.git.commit` when run from a git repo.
- **Sweeps and groups.** Sets of runs from a hyperparameter search. A sweep's results are often the reason a setting has its value.
- **System metrics.** GPU, CPU, and memory use per run (MLflow system metrics, trackio system metrics, W&B system metrics).
- **Artifacts.** Checkpoints, datasets, and predictions logged with versions.
- **Notes, reports, and logbooks.** Write-ups attached to runs: W&B Reports, MLflow run notes, trackio logbooks (which record the exact command, config files, exit code, and output of each run).

## How to search it

Use the tracker's MCP if one is available, otherwise its CLI, API, or local files. Always name the project (and the entity or workspace). Read only: no reports, tags, deletes, or syncs.

1. **Orient before querying.** Find the project and its keys first.

   ```
   W&B MCP: probe_project_tool (metric keys, config keys, tags)
   MLflow: mlflow experiments search
   trackio: trackio list projects --json; trackio list runs --project <p> --json
   TensorBoard: list the run directories under the log directory
   ```

2. **Start from known run IDs.** The task folder, the run's log, or the job output often names the run ID or URL. Read that run's config, summary, and metadata.

   ```
   W&B MCP: query_wandb_tool (without the MCP: the public API, wandb.Api(); for a local run directory: wandb leet inspect <run_directory_or_wandb_file> --summary --json)
   MLflow: mlflow runs describe --run-id <id>
   trackio: trackio get run --project <p> --run <r> --json
   ```

3. **Where a setting came from.** For "why is X set to N", find the run or sweep where N first appears and the runs that tried other values. A sweep whose best run used N, dated just before N was hard-coded, is circumstantial evidence the value came from it.

   ```
   W&B MCP: compare_runs_tool
   MLflow: mlflow experiments csv -x <experiment_id>
   trackio: trackio query project --project <p> --sql "SELECT ..."   (read-only SQL)
   ```

4. **Curves around a change.** For defensive settings (gradient clipping, a lower learning rate, warmup, a smaller batch), pull the metric history of runs before and after the change. Look for NaN or Inf, divergence, or spikes before it.

   ```
   W&B MCP: get_run_history_tool (reports non_finite_counts for NaN and Inf)
   trackio: trackio get metric --project <p> --run <r> --metric <m> --around <step> --window <n>
   ```

5. **Our run versus the paper.** For "why does our number differ", record verbatim every setting our run logged that a comparison needs (model and checkpoint, data version and split, learning rate and schedule, batch size, steps, precision, seeds, evaluation settings), and its final metrics. Leave the paper's side to the published-record investigator.

## What good evidence looks like here

- A sweep or comparison whose best run used the value the target now hard-codes, dated just before the change
- A run's logged config that differs from the repo's config at the run's commit (an override on the command line or in code)
- A metric history with NaN or divergence in runs before a defensive change and stable curves after
- A note, report, or logbook page by the author stating why a setting was chosen

## Common pitfalls

- **Bounded results.** Tools and APIs often return a page or a sample, not every run. The W&B MCP reports `has_more`, `sampled`, and `truncated`. Check them before calling a search exhaustive.
- **Wrong server or project.** A wrong instance, entity, or project can return empty results or an access or not-found error. A local W&B MCP without `WANDB_BASE_URL` set defaults to the public cloud, not a dedicated instance. An empty result from an unconfirmed project is a gap.
- **Unsynced and local runs.** Runs logged offline stay on local disk until synced, and TensorBoard and trackio keep data local by default. A run missing from the server may exist in a local directory.
- **Logged ≠ used.** A config value logged at start may have been overridden later in code. It is what the code reported, not proof of what ran. Pair it with the code at the run's commit.
- **Instrumented ≠ caused.** A metric's existence means someone cared enough to log it, not that the target exists *because* of it.
- **Resumed runs.** A resumed run joins history from several processes. W&B's automatic resume can attach the wrong run when several runs failed in the same directory.
- **Only what was logged.** TensorBoard shows hyperparameters only if the code logged them. A missing config is a gap, not a default.

## What to return

For each relevant finding:
- Tracker, project, and run IDs or URLs
- The exact query, tool call, or command you ran, and the step or time window
- The config values and metrics that bear on the question (exact values, not "about"), plus any coverage fields the tool reported
- The commit, start time, and state each run recorded
- Temporal correlation with the target's change date (e.g., "sweep finished 2026-03-02, value hard-coded in commit abc123 on 2026-03-04")
- Relevance + strength: direct / circumstantial / weak

Sources: SOURCES.md entries `wandb-agent-docs`, `wandb-mcp-server`, `mlflow-docs`, `tensorboard-docs`, `trackio`.
