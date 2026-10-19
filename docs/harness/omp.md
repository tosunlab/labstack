# labstack on omp

How labstack's neutral wording maps to omp. Skills never name these tools; this file does.

## Install

omp reads the same catalog as Claude Code (`.claude-plugin/marketplace.json`).

```
/marketplace add tosunlab/labstack
/marketplace install labstack@labstack
```

Skills load as `/skill:lab-mode`, `/skill:setup-labstack`.

## Files next to a skill

Read bundled files through the skill URI: `skill://lab-mode/playbooks/literature.md`, `skill://principle-answer-first`. Files outside `skills/` (such as this one) are under the installed plugin's root; `../../docs/harness/omp.md` from the skill directory.

## Verbs

| labstack says | omp |
|---|---|
| ask the supervisor | The `ask` tool: a batch of questions, 2-5 options each, with `recommended` set to the recommended option. For a long numbered batch ("all recommended except 3"), write it as a plain message and end the turn. |
| keep a todo list | The `todo` tool. Put the playbook's steps in as the first phase. |
| spawn a subagent | The `task` tool with the default `task` agent. Give each task a self-contained brief: subagents do not see the conversation. |
| run a role on its model | The `task` tool takes no per-spawn model. Set `cfg://task/agentModelOverrides` so the `task` agent maps to the role's model before spawning, and restore the previous value afterwards. This is a session-only setting change and needs the user's approval; do not save it. If the role resolves to the session model, skip this. |
| run a long job detached | `bash` with `async: true` (or `timeout: 0` for long jobs), writing to a log file. |
| search the web, fetch a page | `web_search`; `read` on a URL. `read` truncates long pages; for a paper, fetch the raw file with `curl` in `bash`. |

## Role models

`setup-labstack` writes `~/.config/labstack/models.yml`. lab-mode reads the `omp:` section. Values are omp model selectors (`provider/model`, optionally `:effort`). A missing file or role means the session model.
