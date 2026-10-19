---
name: setup-labstack
description: Choose which model labstack uses for each role (judgment, worker, panel) in the current harness, and write the choice to the user's labstack config. Use for /setup-labstack, "configure labstack models", or changing labstack's model choices. Optional: without it every role runs on the session model.
---

# Setup labstack

Write the current harness's section of `~/.config/labstack/models.yml`. Without this file every role runs on the session model, which is a fine default.

## Roles

- **judgment**: planning, interpreting results, synthesizing, writing to the supervisor.
- **worker**: delegated implementation, runs, searching, and reading (explorers, investigators, parallel workers). A faster, cheaper model often fits.
- **panel**: a list; one subagent per entry, for independent reviewers (`interrogate`) and parallel attempts (`arena`). Entries from different model families catch more, because a model tends to favour its own family's work. With fewer than two entries, those skills run on the session model and say their reviewers share one family.

## Steps

1. **Harness.** Name the harness you are running in. Read `../../docs/harness/<harness>.md` from this file for how that harness picks a model per subagent and what a model value looks like there.
2. **Available models.** Find the models you can actually use for a subagent in this harness. If you cannot list them, ask the user to name them. Never write a model you have not confirmed is available.
3. **Current state.** If the file exists, read it. Keep every other harness's section unchanged.
4. **Ask.** One batch: for each role, the current value (or "session model") and the available options, with "session model" always offered. Recommend the session model for any role the user has no reason to change.
5. **Write.** Rewrite only this harness's section, one line per role. Omit a role to leave it on the session model. Shape:

   ```yaml
   <harness>:
     judgment: <model>
     worker: <model>
     panel: [<model>, <model>]
   ```

6. **Confirm.** Tell the user what was written and that it applies to new lab-mode tasks. Running this skill again updates it.

Sources: SOURCES.md entries `pstack`, `llm-self-preference`.
