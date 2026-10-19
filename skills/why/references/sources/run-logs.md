# Run Logs & Failures

## What this source contains

Run logs hold what the program reported while it ran: the failures that motivated defensive code and the output behind a number, as opposed to what a summary or hand-back says about the run.

- **Training and eval logs.** The program's own output: stdout and stderr files (including the program's lines in the scheduler's job output files), log files the code writes, framework warnings. Loss values, learning-rate schedules, resolved configs, and dataset sizes are often printed here.
- **Crash traces.** Tracebacks, CUDA and out-of-memory errors, NaN or Inf detections, assertion failures, and the last lines before a job died.
- **Task folder run records.** Each `lab/<date>-<task>/` folder holds what an earlier task needed to rerun its work: commands, configs, setup records, run outputs, and its hand-back. A `decisions.tsv` there, if show-me-your-work kept one, records why each choice was made.
- **Saved outputs.** Predictions, per-example scores, and generated text, from which a reported number was computed.

This investigator owns the `lab/` task folders and the program's log output wherever it lives.

## How to search it

Use the shell: list, read, and search files. Read only.

1. **Locate the logs.** Start from the task folders under `lab/`, the log directories the code writes to, and the job output files the anchor names. List them with their dates and sizes before reading.

   ```bash
   ls -lt lab/
   rg -l --glob '*.{log,out,err,txt}' '<symbol_or_run_name>' <log_dirs>
   ```

2. **Search for the failure text.** Search for the error string, exception class, or condition the target guards against, and for the generic failure signs.

   ```bash
   rg -n -C3 '<error_string_or_exception>' <log_dirs>
   rg -n -i 'traceback|out of memory|\bnan\b|\binf\b|diverg|warning' <log_file>
   ```

   **Strongly prefer runs dated around the change** (the runs just before and just after the target was added or changed).

3. **Compare before and after.** For defensive code, check whether the failure appears in runs before the change and stops after. Note the commit each run recorded, if its log prints one.

4. **Trace a number to its run.** For "where did this number come from" or "why does our number differ", find the run whose log or saved output contains the number. Then record what that run's log says it used: command, resolved config, commit, data version, number of examples evaluated, and any warnings. Check that the number in the hand-back matches the number in the log or the saved outputs.

## What good evidence looks like here

- A traceback or NaN loss in runs dated before a guard was added, absent from runs after
- A log line printing the effective setting (resolved config, effective batch size, dtype, number of examples) that differs from the intended one
- A warning in our eval log (inputs truncated, examples skipped, a fallback to a default) that bears on a gap with the paper
- A task folder whose recorded command and config produced the number in question
- A `decisions.tsv` row stating why a setting was chosen

## Common pitfalls

- **The report is not the record.** A hand-back, README, or summary that states a number is a claim. Trace it to the log or saved outputs that produced it.
- **Which run?** Several runs often share a name, directory, or log path, and a resumed or requeued run may append to or overwrite an earlier log. Match by job ID, timestamps, and the recorded commit, not by file name alone.
- **Wiped logs.** Node-local logs may disappear when an allocation is released. A missing log is a gap, not a clean run.
- **Silent fallbacks.** Code that catches an error and continues may log one warning instead of crashing. Search warnings, not only errors.
- **Truncated output.** A job killed by the scheduler may end mid-line with no traceback. Read the last lines and hand the job ID to the cluster investigator as a lead.
- **Correlation is not causation.** A crash before a commit and none after is suggestive, not definitive. Other changes may have landed in the same window, and later runs may simply have used different settings.

## What to return

For each relevant log or record:
- File path, and the job ID, run ID, or task folder it belongs to
- The run's time range, and the commit and config it recorded, if any
- The verbatim lines that bear on the question, with line numbers (excerpt, not summary)
- The search patterns you ran and the files they covered
- Temporal correlation with the target's change date
- Relevance + strength: direct / circumstantial / weak

Sources: SOURCES.md entries `slurm-docs`, `reclaim`.
