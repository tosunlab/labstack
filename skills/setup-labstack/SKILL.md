---
name: setup-labstack
description: Choose which model labstack uses for each role (judgment, code delegate, review panel) in the current harness, and write the choice to the user's labstack config. Use for /setup-labstack, "configure labstack models", or changing labstack's model choices. Optional: without it every role runs on the session model.
---

# Setup labstack

Write the current harness's section of `~/.config/labstack/models.yml`. Without this file every role runs on the session model, which is a fine default.

## Roles

- **judgment**: planning, interpreting results, writing to the supervisor.
- **code delegate**: implementation and runs handed to subagents.
- **review panel**: independent review, only when the supervisor asks for one. A list; one reviewer runs per entry. A model family different from the one that did the work catches more.

## Steps

1. **Harness.** Name the harness you are running in. Read `../../docs/harness/<harness>.md` from this file for how that harness picks a model per subagent and what a model value looks like there.
2. **Available models.** Find the models you can actually use for a subagent in this harness. If you cannot list them, ask the user to name them. Never write a model you have not confirmed is available.
3. **Current state.** If the file exists, read it. Keep every other harness's section unchanged.
4. **Ask.** One batch: for each role, the current value (or "session model") and the available options, with "session model" always offered. Recommend the session model for any role the user has no reason to change.
5. **Write.** Rewrite only this harness's section, one line per role. Omit a role to leave it on the session model. Shape:

   ```yaml
   <harness>:
     judgment: <model>
     code delegate: <model>
     review panel: [<model>, <model>]
   ```

6. **Confirm.** Tell the user what was written and that it applies to new lab-mode tasks. Running this skill again updates it.

Sources: SOURCES.md entries `pstack`, `llm-self-preference`.
