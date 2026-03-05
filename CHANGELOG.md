# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/).

## [1.1.0] - 2026-03-05

### Added
- `.claude/skills/example-skill/` — annotated skill template with SKILL.md, LEARNED.md, and references/
- Skills section in README explaining skill structure and self-learning

## [1.0.0] - 2026-03-03

### Added
- `CLAUDE.md` — annotated template with session continuity, work conventions, anti-hallucination protocol, memory management, and productivity tips
- `.claude/rules/` — three example rules with glob-scoped loading (architecture, workflow, session protocol)
- `.claude/hooks/pre-compact-handover.py` — PreCompact hook that auto-generates HANDOVER document when Claude Code compresses context
- `.claude/settings.json` — hook configuration for PreCompact
- `.claudeignore` — commented patterns with explanation of Glob/Grep limitations
- `local/session-notes/TEMPLATE.md` — session notes template for daily tracking
- `local/backlog-TEMPLATE.md` — backlog template for task tracking between sessions
- `memory/` — example files showing Claude Code's persistent memory structure (MEMORY.md, topic files)
- `README.md` — system philosophy, quick start guide, design principles
- MIT License
