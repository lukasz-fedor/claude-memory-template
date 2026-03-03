# Memory Directory

This directory shows the **recommended structure** for Claude Code's persistent memory.

## How Claude Code memory works

Claude Code stores `MEMORY.md` at:
```
~/.claude/projects/<project-hash>/memory/MEMORY.md
```

That path is auto-managed — you don't create it manually. But you CAN create **topic files** in the same directory to keep MEMORY.md lean and contextual.

## Recommended structure

```
~/.claude/projects/<hash>/memory/
├── MEMORY.md          ← Index + key conventions (always loaded, max 200 lines)
├── debugging.md       ← Recurring issues and solutions
├── patterns.md        ← Architectural patterns and decisions
├── tools.md           ← CLI tools, configs, workarounds
└── migrations.md      ← Migration notes, data transformations
```

For larger projects, organize into subdirectories:
```
memory/
├── MEMORY.md
├── domain/
│   ├── auth.md
│   └── payments.md
└── tools/
    ├── docker.md
    └── ci.md
```

## Entry format

Keep entries brief and actionable — what happened, why it matters.

```markdown
## Deployment
- 2025-02-03: Preview deploys need env vars in Vercel project settings, not just .env
- 2025-02-10: Build fails on Node 18 — .nvmrc enforces 20, CI needs matching config
```

## What goes where

| File | Content | Example |
|------|---------|---------|
| `MEMORY.md` | Index + top conventions | "Always use bun instead of npm" |
| Topic files | Detailed notes by domain | "Tailwind v4: hidden lg:grid doesn't work..." |

## What to save vs. skip

**Save:** Stable patterns, user preferences, architectural decisions, recurring solutions, environment quirks.

**Skip:** Session-specific context, unverified conclusions, anything already in CLAUDE.md or rules.

## Maintenance

Say **"clean up memory"** to Claude and it will audit all memory files, remove outdated entries, consolidate related notes, rebuild the MEMORY.md index, and report what changed.

## Example files

The files in this directory (`example-memory.md`, `example-topic.md`) show the format.
Delete them after reviewing — Claude Code will create the real files at `~/.claude/projects/<hash>/memory/`.
