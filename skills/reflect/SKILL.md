---
name: reflect
description: Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on the project's notes or a proposed change to an existing skill. Use when the user says reflect. Run only when the user asks for it.
---

# Reflect

Mine the current conversation for durable learnings, then route them into edits to the project's notes or proposed skill edits.

Invoke when the user says "reflect" or "/reflect". Skip when the conversation is trivial, off-topic, or already covered by an existing skill the parent followed correctly. One-offs are not learnings.

## 1. Locate the active transcript

Before fanning out, find this conversation's transcript in this harness's session transcripts (where they live: `docs/harness/<harness>.md`, Transcripts). Do not glob across other projects' transcripts. That crosses workspace boundaries and reads private chats from unrelated projects.

List the ten most recently modified transcripts of this project, subagent transcripts included. For each candidate, read the first user message. Take the file whose first user message contains the conversation's opening user prompt. If none matches, pass a tight digest of the session instead.

## 2. Spawn three reviewers in parallel

Spawn all three at once. Give each the session's tools, including MCP servers; it still writes nothing. Reviewers need MCP access to look up the tickets, chat threads, and tracker runs the transcript references.

Each reviewer and the synthesizer name a role. Use the `<role>` model from the labstack model config (lab-mode, Roles). A missing config or role means the session model. If a configured model is unavailable, use the session model and say so. Match each subagent's effort to the job where your harness lets you set it.

| Lens | Role | Prompt template |
|---|---|---|
| Judgment | `judgment` | `references/judgment-reviewer.md` |
| Tooling | `worker` | `references/tooling-reviewer.md` |
| Divergent | `judgment` | `references/divergent-reviewer.md` |

Pass each template verbatim, substituting the transcript path or digest where marked. Reviewers return findings in their response body.

## 3. Synthesize

Spawn one subagent on the `judgment` model, with the session's tools, including MCP servers; it still writes nothing. It spot-verifies citations through MCP. Pass `references/synthesizer.md` verbatim, with each reviewer's full output inlined where marked. It returns an Accepted / Rejected / Backlog list.

## 4. Structural enforcement check

Move any Accepted item that a lint rule, script, metadata flag, or runtime check would enforce more reliably to Backlog. See the **correct** skill.

## 5. Apply

Present the synthesizer's full Accepted / Rejected / Backlog output and wait for explicit approval before applying any Accepted edit. The user picks the subset and may redirect routings. Skill changes affect every future agent in the org. Do not auto-apply.

List each Backlog item for the supervisor.

Follow each approved row's Routing exactly:

- `project notes: <file>` (the project's own instruction file or a note under `lab/`): the parent edits it directly.
- Existing-skill edit, `tune description: <skill path>`, or `new skill: <kebab-name>`: write the proposed change (the skill, the section, and the exact text) to `lab/<date>-reflect/` for the supervisor to send upstream. Installed plugin skills are not edited in place.

## 6. Summarize for the user

Short list, no preamble:

- Edits applied: `<file path>`. What changed, one line each.
- Skill changes proposed: `<skill path>` or `<kebab-name>` for a new skill (rare), with the file in `lab/<date>-reflect/`. One line each.
- Backlog for the supervisor: `<issue title>` (`<tags>`). One line each.
- Dropped: one line per rejected finding + reason from the synthesizer.

Adapted from pstack's `reflect` skill (https://github.com/cursor/plugins/tree/main/pstack, version 0.15.28), Copyright (c) 2026 Lauren Tan, MIT License: see `LICENSES/pstack.txt`. Changes for labstack are listed in `docs/pstack-port.md`.
