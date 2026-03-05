# Claude Code Memory Template

A ready-to-use system that makes Claude Code remember your project across sessions — rules, preferences, decisions, and context.

## The problem

Every new Claude Code session starts from zero. Claude doesn't remember what you decided yesterday, what bugs you fixed, or how your project is structured. You end up repeating yourself, correcting the same mistakes, and losing time.

## What this template gives you

| What | How it helps |
|------|-------------|
| **Modular rules** | Claude loads only relevant instructions — not everything at once |
| **Persistent memory** | Decisions, bug fixes, and gotchas survive across sessions |
| **Session handover** | When Claude runs out of context mid-conversation, it saves a handover file so the next session picks up where you left off |
| **Skills** | Reusable "modes" that make Claude an expert at specific tasks (code review, copywriting, deployment...) |
| **Anti-hallucination** | Built-in rules that stop Claude from making up facts, stats, or URLs |

## How it's organized

```
your-project/
├── CLAUDE.md                    # Project rules (always loaded, keep it short)
├── .claude/
│   ├── rules/                   # Detailed rules — loaded only when relevant
│   │   ├── architecture.md      #   → loads when editing src/ files
│   │   ├── workflow.md          #   → loads when editing docs/ or scripts/
│   │   └── session-protocol.md  #   → loads when editing local/ files
│   ├── skills/                  # Specialized modes for specific tasks
│   │   └── example-skill/       #   → copy and adapt for your needs
│   │       ├── SKILL.md         #     instructions for this skill
│   │       ├── LEARNED.md       #     patterns Claude discovers over time
│   │       └── references/      #     supporting docs
│   ├── hooks/
│   │   └── pre-compact-handover.py  # Auto-saves context before it's lost
│   └── settings.json            # Hook configuration
├── local/                       # Your working notes (gitignored)
│   ├── backlog.md               #   task tracking between sessions
│   └── session-notes/           #   daily notes + auto-generated handovers
├── .claudeignore                # What Claude skips at startup
└── .gitignore                   # Keeps local/ and .env out of git
```

The key idea: **CLAUDE.md stays short** (under 100 lines). Detailed instructions go into `rules/` files that load automatically based on what files you're editing.

## Quick start

**1. Copy the template into your project:**

```bash
cp -r claude-memory-template/.claude your-project/.claude
cp -r claude-memory-template/local your-project/local
cp claude-memory-template/CLAUDE.md your-project/CLAUDE.md
cp claude-memory-template/.claudeignore your-project/.claudeignore
cat claude-memory-template/.gitignore >> your-project/.gitignore
```

**2. Rename template files:**

```bash
mv your-project/local/backlog-TEMPLATE.md your-project/local/backlog.md
mv your-project/local/session-notes/TEMPLATE.md your-project/local/session-notes/README.md
```

**3. Edit `CLAUDE.md`** — replace the placeholder comments with your project's conventions.

**4. Edit `.claude/rules/`** — adapt the example rules to your tech stack. Each rule file has a `globs:` header that controls when it loads.

**5. Start a Claude Code session.** Everything works automatically from here.

That's it. The memory system, handover hook, and rules loading are all pre-configured.

## How each piece works

### Rules (load only when needed)

Instead of cramming everything into CLAUDE.md, put detailed instructions in `.claude/rules/`. Each file has a header that tells Claude when to load it:

```yaml
---
globs:
  - "src/**"
---
# Architecture rules here...
```

This file loads only when Claude edits something in `src/`. Your styling guide, component conventions, API patterns — all loaded contextually, not always.

### Memory (persists across sessions)

Claude Code has a built-in memory system at `~/.claude/projects/`. You don't need to create it — Claude manages it automatically.

This template teaches Claude **how** to use memory well:
- Write entries immediately when discovering something useful (don't wait)
- Use the format: `2026-03-05: what happened — why it matters`
- Organize into topic files (`tools/docker.md`, `domain/auth.md`)
- Keep the index (`MEMORY.md`) short — one line per topic file

> The `memory/` folder in this repo contains **examples only**. It shows what Claude creates on its own — it's not part of your project files.

### Skills (specialized modes)

Skills give Claude domain expertise for specific tasks. Each skill has:
- **SKILL.md** — instructions loaded when the skill is invoked
- **LEARNED.md** — patterns Claude discovers during real usage (gets better over time)
- **references/** — supporting documentation loaded on demand

The template includes an annotated `example-skill/` to copy and adapt.

### Session handover (automatic)

When Claude Code runs out of context and compresses the conversation, the pre-configured hook:
1. Reads the full conversation
2. Generates a structured handover document
3. Saves it to `local/session-notes/HANDOVER-latest.md`

Next session, Claude reads the handover and continues where it left off. No manual work needed.

### .claudeignore (control what loads)

Works like `.gitignore` — tells Claude Code what to skip when starting a session. Useful for large directories (build output, node_modules, big data files) that would waste context.

Note: `.claudeignore` only affects auto-loading at startup. Claude's search tools (Glob, Grep) can still find files in ignored directories when needed.

## Design principles

1. **Context is expensive.** Every line Claude reads costs tokens. Load only what's relevant.
2. **Modular beats monolithic.** 50 lines in CLAUDE.md + 3 focused rules > 200 lines in one file.
3. **Rules over memory.** Rules are structured and always apply. Memory is for discoveries and edge cases.
4. **No work lost.** The handover hook means context compression doesn't erase progress.
5. **Human-in-the-loop.** Claude never auto-publishes, auto-approves, or auto-deploys without your OK.
6. **No hallucinations.** Claude cites sources, admits when it doesn't know, and verifies before claiming.

## Requirements

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3 (for the handover hook)
