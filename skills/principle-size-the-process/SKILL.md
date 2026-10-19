---
name: principle-size-the-process
description: Apply when choosing how much workflow a request gets: subagents, state files, review passes, runs.
---

# Size the process to the request

Use the smallest workflow that answers the question. One agent by default. Add parallel agents only when the work splits into independent parts, such as one per paper or per benchmark. Add state files, logs, or review passes only when the task spans sessions or the supervisor asks.

- A single strong agent with a shell and files matched or beat elaborate multi-agent and search setups on ML engineering tasks at equal budget. Parallel agents cost many times the tokens and pay off only when the work really splits.
- Do what was asked and nothing more. Mention an extra in one line.
- How many runs to do is the supervisor's call. There is no default repeat count.

Sources: SOURCES.md entries `minimal-harness-mle`, `scaling-agent-systems`, `anthropic-multi-agent-research`, `claude-md-growth`.
