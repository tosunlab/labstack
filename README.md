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
