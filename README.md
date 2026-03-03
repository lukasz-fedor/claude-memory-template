# Claude Code Memory Template

A starter template for organizing Claude Code's memory system: modular rules, persistent memory, session continuity, and automatic handover.

## Why this exists

Claude Code loads `CLAUDE.md` into every conversation. As your project grows, this file bloats — and Claude wastes context on instructions irrelevant to the current task.

This template solves that with **three layers**:

| Layer | What it does | When it loads |
|-------|-------------|---------------|
| `CLAUDE.md` | Core project identity and conventions | Every session |
| `.claude/rules/` | Domain-specific rules with glob patterns | Only when editing matching files |
| `MEMORY.md` | Persistent knowledge across sessions | Every session (auto-managed by Claude Code) |

## How it works

### 1. CLAUDE.md — lean and focused

Keep it under 100 lines. Only project-wide conventions that apply to every task. Move everything else to rules.

**Key sections included in the template:**
- Session Continuity — handover reading at session start
- Work Conventions — placeholder rules, human-in-the-loop
- Anti-Hallucination Protocol — prevents fabricated facts, stats, URLs
- Git Workflow — conventional commits
- Productivity Tips — "update CLAUDE.md" habit, subagents, plan mode

### 2. Rules with glob patterns

Files in `.claude/rules/` have frontmatter that controls when they load:

```yaml
---
globs:
  - "src/**"
---
```

This rule loads only when Claude edits files in `src/`. Architecture docs, styling gotchas, component conventions — all loaded contextually instead of always.

**Included examples:**
- `architecture.md` (glob: `src/**`) — tech stack, components, styling
- `workflow.md` (glob: `docs/**`, `scripts/**`) — documentation and tooling
- `session-protocol.md` (glob: `local/**`) — session notes format

### 3. Persistent memory

Claude Code auto-manages `MEMORY.md` at:
```
~/.claude/projects/<project-hash>/memory/MEMORY.md
```

This file is **not stored in your repo** — Claude Code creates and manages it automatically. You don't need to set it up.

**Best practices for MEMORY.md:**
- Keep it under 200 lines (content beyond line 200 gets truncated)
- For detailed topics, create separate files (`debugging.md`, `patterns.md`) in the same directory
- Reference topic files from MEMORY.md with a simple index

**Example structure:**
```markdown
# Memory

## Project Conventions
- Key conventions Claude should always remember
- User preferences for workflow and communication

## Topic Files
- `memory/debugging.md` — recurring issues and solutions
- `memory/patterns.md` — architectural patterns and decisions
```

**What to save:** Stable patterns, architectural decisions, user preferences, recurring solutions.
**What NOT to save:** Session-specific context, unverified conclusions, anything that duplicates CLAUDE.md.

### 4. Session continuity

The **PreCompact hook** solves Claude Code's biggest limitation: context loss.

When Claude Code runs out of context and compresses the conversation, the hook:
1. Reads the full conversation transcript
2. Generates a structured HANDOVER document via `claude -p` (tools disabled, single turn)
3. Saves it to `local/session-notes/HANDOVER-latest.md`

Next session, Claude reads the handover and picks up where it left off.

**Setup:** The hook is configured in `.claude/settings.json` and runs automatically.

### 5. .claudeignore

Controls what Claude Code auto-loads at session start. Does **not** block search tools (Glob, Grep) — those can still scan ignored directories unless you pass the `path` parameter explicitly.

## Quick start

1. Copy this template into your project root
2. Edit `CLAUDE.md` — replace placeholders with your project info
3. Edit `.claude/rules/` — adapt rules to your tech stack
4. Verify `.claude/settings.json` has the PreCompact hook
5. Create `local/session-notes/` directory (it's gitignored)
6. Start a Claude Code session — the system works automatically

```bash
# Copy template files
cp -r claude-memory-template/.claude your-project/.claude
cp claude-memory-template/CLAUDE.md your-project/CLAUDE.md
cp claude-memory-template/.claudeignore your-project/.claudeignore
cat claude-memory-template/.gitignore >> your-project/.gitignore

# Create local directories
mkdir -p your-project/local/session-notes
```

## File structure

```
your-project/
├── CLAUDE.md                          # Core instructions (always loaded)
├── .claudeignore                      # Auto-load exclusions
├── .gitignore                         # Includes local/ and .env
├── .claude/
│   ├── settings.json                  # Hook configuration
│   ├── rules/
│   │   ├── architecture.md            # Loads for src/** edits
│   │   ├── workflow.md                # Loads for docs/**, scripts/**
│   │   └── session-protocol.md        # Loads for local/** edits
│   └── hooks/
│       └── pre-compact-handover.py    # Auto-generates handover on compact
├── local/                             # Gitignored — local working data
│   └── session-notes/
│       ├── HANDOVER-latest.md         # Auto-generated by hook
│       └── 2025-01-15.md              # Daily session notes
└── memory/                            # Example structure (see memory/README.md)
    ├── README.md                      # How Claude Code memory works
    ├── example-memory.md              # Example MEMORY.md format
    └── example-topic.md               # Example topic file format
```

## Design principles

1. **Context is finite.** Every line Claude reads costs tokens. Load only what's relevant.
2. **Rules over memory.** Rules are structured and scoped. Memory is freeform. Prefer rules for stable conventions.
3. **Session continuity matters.** The handover hook means no work is lost when context compresses.
4. **Modular beats monolithic.** A 200-line CLAUDE.md with everything is worse than 50 lines + 3 focused rules.
5. **Human-in-the-loop.** Never auto-publish, auto-approve, or auto-save without explicit OK.
6. **Anti-hallucination by default.** Claude should cite sources, admit ignorance, and verify links.

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3 (for the handover hook)
