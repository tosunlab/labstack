# Source playbooks

The why skill spawns one investigator per available evidence category, each reading a single source-specific playbook below. The playbooks are concrete examples for common MCPs and tools. Adapt them for a different MCP or tool in the same category.

| Category | Playbook | Example MCP or tool it documents |
|---|---|---|
| Source control history | [`code-archaeology.md`](./sources/code-archaeology.md) | git, `gh` |
| Issue / ticket tracker | [`linear.md`](./sources/linear.md) | Linear (adapt for Jira, GitHub Issues, Plane, Shortcut) |
| Long-form documents | [`notion.md`](./sources/notion.md) | Notion (adapt for Confluence, Google Docs, Coda) |
| Real-time team chat | [`slack.md`](./sources/slack.md) | Slack (adapt for Discord, Microsoft Teams, Mattermost) |
| Cluster and job records | [`cluster-jobs.md`](./sources/cluster-jobs.md) | Slurm's `sacct` and `squeue` (adapt for PBS, LSF, a cloud job service, or a scheduler MCP) |
| Run logs and failures | [`run-logs.md`](./sources/run-logs.md) | Log files and `lab/` task folders (adapt for any log location) |
| Experiment tracker | [`experiment-tracker.md`](./sources/experiment-tracker.md) | W&B MCP and API, MLflow, trackio, TensorBoard (adapt for Aim or a results database) |
| Published record | [`published-record.md`](./sources/published-record.md) | arXiv, the released repository, OpenReview (adapt for other venues and preprint servers) |

Cross-cutting:

- [`incident-postmortem.md`](./sources/incident-postmortem.md). Add this if the target code looks defensive (null checks, NaN guard, retry or requeue, checkpoint resume, timeout, rate limit, feature flag, egress guard, OOM handler).
