# labstack on Claude Code

How labstack's neutral wording maps to Claude Code. Skills never name these tools; this file does.

## Install

```
/plugin marketplace add tosunlab/labstack
/plugin install labstack@labstack
```

Skills are namespaced by the plugin: `/labstack:lab-mode`, `/labstack:setup-labstack`.

## Files next to a skill

When Claude Code loads a skill it shows the skill's base directory. Resolve relative paths in the skill against it: `playbooks/literature.md` is inside the lab-mode skill directory, `../principle-answer-first/SKILL.md` is a sibling skill, and this file is `../../docs/harness/claude-code.md` from any skill.

## Verbs

| labstack says | Claude Code |
|---|---|
| ask the supervisor | `AskUserQuestion` for a few multiple-choice questions, each option with a short description and the recommendation marked. For a long numbered batch ("all recommended except 3"), write it as a plain message and end the turn. |
| keep a todo list | `TaskCreate` and `TaskUpdate` (on older versions or models without them, `TodoWrite`). |
| spawn a subagent | `Agent` tool. Use the general-purpose agent unless a more specific one fits. Give it a self-contained brief: it does not see the conversation. |
| run a role on its model | Pass the per-invocation `model` parameter on the `Agent` call. Claude Code accepts aliases (`opus`, `sonnet`, `haiku`) and full model IDs. If the role resolves to the session model, omit the parameter. |
| run a long job detached | `Bash` with `run_in_background: true`, writing to a log file, then poll the log. |
| search the web, fetch a page | `WebSearch`, `WebFetch`. `WebFetch` returns a model summary of long pages, not the full text; for a paper or a long page, fetch the raw file with `curl` in `Bash` and read it. |

## Role models

`setup-labstack` writes `~/.config/labstack/models.yml`. lab-mode reads the `claude-code:` section. Values are anything the `Agent` tool's `model` parameter accepts. A missing file or role means the session model.

## Hard limits

Things a skill states in prose but that must hold every time (read-only raw data, no writes to the scorer) are better enforced with permission rules or hooks in the project's Claude Code settings. labstack does not install them; set them per project if you want them enforced.
