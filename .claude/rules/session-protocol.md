---
globs:
  - "local/**"
---

<!--
  This rule loads when working with local/ files (session notes, cached data).
  It tells Claude how to maintain session continuity.
-->

# Session Protocol

## Session Notes

Claude maintains session notes in `local/session-notes/YYYY-MM-DD.md`:
- **Start of session** — create or open today's file
- **During work** — log completed tasks, decisions, key findings
- **Before ending** — fill in "Next steps" section

### Template

```markdown
# Session Notes - YYYY-MM-DD

## Completed Tasks
### [task name]
- what was done, key decisions

## Commits
- `hash` - description

## Notes
- important observations

## Next Steps
- what to do next
```

## Handover

The PreCompact hook (`.claude/hooks/pre-compact-handover.py`) automatically generates
`local/session-notes/HANDOVER-latest.md` when Claude Code compresses context.
This file is read at the start of the next session (see CLAUDE.md).
