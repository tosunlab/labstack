# labstack

A skill stack for researchers who work with coding agents.

You set the task; the agent does it and hands it back. `lab-mode` takes a scoped request such as "find the latest benchmarks for X, implement them, and run them", "find me the papers on Y", or "reproduce Table 2 of paper Z". It routes the request to a playbook, works on its own, asks you only when a choice changes what the result means or costs, and leads its hand-back with the answer. labstack is not an autonomous research pipeline.

**Status:** early. lab-mode with three playbooks (literature, benchmarks, reproduction) and six principles.

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

Then start a task with `lab-mode`. Every role runs on your session model; run `setup-labstack` to pick models per role. Harness notes: [docs/harness](./docs/harness).

## Design

External sources behind the skills are in [SOURCES.md](./SOURCES.md).

## Next steps

In order:

1. **Use it on real requests.** Run lab-mode on two or three real literature, benchmark, and reproduction tasks, then fix what the hand-backs and questions get wrong. Nothing else changes before this.
2. **Test lab-mode itself.** Trial cases with a planted decision point (a stated requirement a code default contradicts, sources that disagree) and a tempting action the request does not allow (a launch script, a file that must not change). Grade from file changes and the tool trace; a question is scored on whether it was needed. On real use, log the supervisor's minutes spent reading and correcting each hand-back.
3. **Remaining playbooks**, drafted from the same source base:
   - running experiments and judging results;
   - writing and claims;
   - review, when review is the task;
   - theory and proofs;
   - ideation and choosing problems;
   - debugging;
   - figures and slides.
4. **Research versions of pstack's general skills**: `how`, `why`, `interrogate` (as the review skill, run only when the supervisor asks), `reflect`, `correct`, `recall`, and the rest.
5. **More harnesses**: Codex and others, each as one adapter doc in `docs/harness/`.

## What's missing

Areas where the external evidence behind the skills is thin, so the skills say little or rely on the owner's judgment:

- **Benchmarks outside LLM evaluation.** Finding and choosing benchmarks is well covered for LLMs; vision, RL, systems, and science benchmarks are not.
- **Cost estimates for API runs.** Estimating token and API spend reliably, with retries and queues, before asking for a budget.
- **Retired hosted models.** What a reproduction does when the paper's hosted model no longer exists. Any substitute is a deviation that needs consent; the playbook has no further guidance.
- **Gated data and credentials.** Requesting access through the supervisor.
- **Literature completeness.** How to estimate recall for a scoped search, and when a search is deep enough.
- **Internal figures.** Which table or plot to hand back after a benchmark or reproduction run.
- **Non-ML fields.** Wet lab, field studies, qualitative data.
- **Evidence that it helps.** No source measures supervisor time saved or rework avoided; step 2 above is how labstack would find out.
- **Hard limits.** Skills state rules in prose (raw data read-only, the agent never edits its scorer). Enforcing them with harness permissions or hooks is left to each project.

## Contributing

Install the local hooks once per clone:

```bash
pipx install pre-commit   # or: uv tool install pre-commit
pre-commit install
```

The hooks run on every commit:

- **privacy**: no personal absolute paths, local working material, or archives.
- **portability**: shipped skills, agents, and commands contain no harness-specific tool names, config paths, or model names.
- **secrets**: gitleaks and private-key detection.
- **hygiene**: file size, whitespace, line endings, YAML and JSON syntax.

Run every hook against the whole tree with `pre-commit run --all-files`.
