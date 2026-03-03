# Memory

<!--
  EXAMPLE of what MEMORY.md looks like in practice.
  Real file: ~/.claude/projects/<hash>/memory/MEMORY.md
  Keep under 200 lines. Brief entries: what happened, why it matters.
-->

## Project Conventions
- 2025-01-10: Use bun over npm — agreed with team for speed
- 2025-01-12: API follows JSON:API spec — backend contract
- 2025-01-15: Tests: `bun test` — no separate config needed

## Environment
- 2025-01-10: Python tools always in venv (`local/.venv`) — system Python breaks macOS
- 2025-01-11: Node 20 LTS via .nvmrc

## Topic Files
- `memory/debugging.md` — build issues, deployment gotchas
- `memory/patterns.md` — component architecture decisions
