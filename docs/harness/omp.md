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
| spawn a read-only subagent | The `task` agent with a brief that says to write nothing. (The bundled `scout` agent is read-only but runs on its own configured model, not the role's.) Subagents get the session's tools, MCP servers included. |
| spawn all of them at once | One `task` call with several items in `tasks[]`; they run in parallel. |
| run a role on its model | The `task` tool takes no per-spawn model. Set `cfg://task/agentModelOverrides` so the `task` agent maps to the role's model before spawning, and restore the previous value afterwards. This is a session-only setting change and needs the user's approval; do not save it. If the role resolves to the session model, skip this. For `panel`, set the override to one entry, spawn that subagent, then the next entry and the next subagent; spawned subagents keep running in parallel. |
| match each subagent's effort | Put the effort in the model selector (`provider/model:high`) when setting the override. |
| generate an image | Only if an image-generation tool or MCP server is connected. Plots come from code, never from image generation. |
| list the tools and MCP servers available in this session | Look at the tool definitions in this session, MCP tools included; `mcp://` resources are readable with `read`. Treat a source as available only if its tools or another reachable interface (a CLI, an API) are present. |
| run a long job detached | `bash` with `async: true` (or `timeout: 0` for long jobs), writing to a log file. |
| search the web, fetch a page | `web_search`; `read` on a URL. `read` truncates long pages; for a paper, fetch the raw file with `curl` in `bash`. |

## Transcripts

Each session's transcript is a JSONL file under `~/.omp/agent/sessions/<project>/`, named `<timestamp>_<session-id>.jsonl`, where `<project>` is the project's path relative to the home directory with every `/` turned into `-` (so `~/Chore/lab` becomes `-Chore-lab`). A folder with the same name holds that session's tool-output logs. Find the current session by modification time. Read only the current project's folder unless the user asks for another.

## Role models

`setup-labstack` writes `~/.config/labstack/models.yml`. lab-mode reads the `omp:` section. Values are omp model selectors (`provider/model`, optionally `:effort`). A missing file or role means the session model.

## Hard limits

Things a skill states in prose but that must hold every time (read-only raw data, no writes to the scorer) are better enforced with omp hooks or tool approval settings in the project. labstack does not install them; set them per project if you want them enforced.
