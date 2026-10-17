# labstack

A skill stack for researchers who work with coding agents.

You set the task; the agent does it with rigor and hands it back. `lab-mode` takes a scoped request such as "find the latest benchmarks for X, implement them, and run them" or "find me the papers on Y". It picks the playbook that fits, selects what matters most, verifies the result, and returns control to you. labstack is not an autonomous research pipeline.

**Status:** in development. No skills are released yet.

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
