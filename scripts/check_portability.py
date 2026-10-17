#!/usr/bin/env python3
"""Reject harness-specific text in shipped agent-facing files.

Skills, agents, and commands use neutral wording ("spawn a subagent",
"ask the user", "keep a todo list") and role names instead of models.
Per-harness mappings belong in docs/harness/, which this check never scans.

Usage: check_portability.py FILE...   (pre-commit passes staged paths)
"""

import re
import sys
from pathlib import Path, PurePosixPath

SCANNED_ROOTS = {"skills", "agents", "commands"}

_CC_TOOLS = r"Agent|Task|Bash|Read|Write|Edit|Glob|Grep|Skill|LS"

# (harness, what, pattern)
RULES = [
    ("claude-code", "tool name",
     r"\b(?:AskUserQuestion|TodoWrite|TodoRead|WebFetch|WebSearch|NotebookEdit|NotebookRead"
     r"|MultiEdit|ExitPlanMode|SlashCommand|BashOutput|KillShell)\b"),
    ("claude-code", "tool reference", rf"`(?:{_CC_TOOLS})`|\b(?:{_CC_TOOLS})\("),
    ("claude-code", "subagent field", r"\bsubagent_type\b|\brun_in_background\b|\bisolation:\s*\"?worktree"),
    ("claude-code", "config path/env", r"\$\{?CLAUDE_[A-Z_]+\}?|~/\.claude\b|(?<![\w.])\.claude/|\bCLAUDE\.md\b"),
    ("omp", "internal URI", r"\b(?:agent|skill|local|artifact|xd|proc|history|omp|memory|cfg|rule|mcp)://"),
    ("omp", "config path", r"~/\.omp\b|(?<![\w.])\.omp/|\b(?:APPEND_)?SYSTEM\.md\b|\bWATCHDOG\.yml\b"),
    ("omp", "tool reference", r"`(?:eval|todo|ask|task|ast_edit|ast_grep|web_search|wait|irc)`|\b(?:workpool|judge_batch)\("),
    ("cursor", "tool/field", r"\bAskQuestion\b|\bgeneralPurpose\b|\bcloud_base_branch\b|\breadonly:\s*true\b"),
    ("cursor", "config path", r"\.mdc\b|~/\.cursor\b|(?<![\w.])\.cursor/|\.cursor-plugin\b"),
    ("codex", "tool/path", r"\bapply_patch\b|\bupdate_plan\b|~/\.codex\b|(?<![\w.])\.codex/|\bcodex\s+exec\b|\$CODEX_HOME"),
    ("gemini", "config path", r"~/\.gemini\b|(?<![\w.])\.gemini/|\bGEMINI\.md\b"),
    ("any", "agent model name",
     r"(?i)\bclaude-(?:opus|sonnet|haiku|fable)\b|\b(?:opus|sonnet|haiku)\s*\d|\bgpt-\d|\bgrok-\d|\bgemini-\d"),
    ("any", "provider/model slug",
     r"(?<![/\w.])(?:anthropic|openai|openai-codex|cursor|xai|google|openrouter)/[\w.-]+"
     r"|:(?:xhigh|minimal)\b"),
]
COMPILED = [(harness, what, re.compile(pattern)) for harness, what, pattern in RULES]


def in_scope(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return bool(parts) and parts[0] in SCANNED_ROOTS


def scan(path: str) -> list[str]:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for harness, what, regex in COMPILED:
            for match in regex.finditer(line):
                findings.append(f"{path}:{lineno}: {harness} {what}: {match.group(0)!r}")
    return findings


def main(argv: list[str]) -> int:
    findings = [f for path in argv if in_scope(path) for f in scan(path)]
    if not findings:
        return 0
    print("\n".join(findings))
    print(
        "\nHarness-specific text in shipped files. Use neutral wording and role names;"
        "\nput per-harness mappings in docs/harness/.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
