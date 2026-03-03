# My Project

<!--
  CLAUDE.md is your project's main instruction file for Claude Code.
  It's always loaded into context. Keep it under 100 lines.
  Move domain-specific details to .claude/rules/ files with glob patterns.
-->

## Session Continuity

<!--
  This block tells Claude to read handover notes at the start of each session.
  The PreCompact hook (see .claude/hooks/) auto-generates HANDOVER-latest.md
  whenever context is compressed, so the next session can pick up seamlessly.
-->
At the start of a session, read:
- `local/session-notes/HANDOVER-latest.md`
- `local/session-notes/` (latest date file)
Summarize context and ask the user whether to continue.
For quick questions — skip and work directly.

## Work Conventions

<!-- Add your project-specific rules here. Examples below. -->
- Always ask before generating content that doesn't exist in source files
- Use placeholders ("TODO: content needed") for missing content — never invent
- Check `local/` for cached data before fetching from external sources
- Before making changes: outline **what** → **where** → **what it affects**, wait for OK

## Anti-Hallucination Protocol

<!--
  Prevents Claude from fabricating facts or guessing.
  Adapt the language to your project (PL/EN).
  Add project-specific rules (e.g., link verification) if Claude generates public content.
-->
- Run `date` command before answering date-related questions
- Numbers/statistics → show source: `(source: filename.md:42)`
- When unsure → say "I don't have information about..." — NEVER guess

## Git Workflow

```
<type>(<scope>): <description>
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `chore`

### Steps
1. Before work: `git pull origin main`
2. Make changes
3. Stage files: `git add <files>` (avoid `git add .`)
4. Commit: `git commit -m "type(scope): description"`
5. Push: `git push origin main`

## Safety

<!-- Files and directories that should never be committed -->
- `.env`, `.mcp.json`, and `local/` are in `.gitignore` — never commit to repo
- Human-in-the-loop: never auto-publish or auto-approve without explicit OK

## Memory Management

<!--
  Claude Code auto-manages MEMORY.md at ~/.claude/projects/<hash>/memory/
  These rules tell Claude HOW to use it. See memory/README.md for structure.
-->
Proactively save useful discoveries to memory — architectural decisions, bug fixes, gotchas, environment quirks. Write them as they happen, not at session end.

**Entry format:** brief and actionable. Include what happened and why it matters.

**When user says "clean up memory":**
1. Audit all memory files for outdated or duplicate entries
2. Consolidate related notes, split overgrown files
3. Rebuild the MEMORY.md index
4. Report what changed

## Productivity Tips

<!--
  Claude Code workflow patterns that improve session quality.
  Source: Claude Code team best practices + @bcherny (creator of Claude Code).
-->
- **"Update CLAUDE.md" habit:** After correcting Claude, say "Add this to CLAUDE.md so you don't repeat this mistake" — Claude is good at writing rules for itself
- **Subagents for complex tasks:** Add "use subagents" to request for more compute with clean main context
- **Plan mode:** For complex tasks, start in plan mode. When something goes wrong → go back to plan mode and re-plan
- **Prompting patterns:** "Prove to me this works" (before publishing), "Grill me on these changes" (content review)
- **Continue previous session:** Use `claude --continue` (or `-c`) to resume the last session with full context

## Modular Rules

<!--
  Detailed instructions live in .claude/rules/ — loaded automatically
  by glob pattern when you edit matching files. This keeps CLAUDE.md lean.
  See .claude/rules/ for examples.
-->
Architecture, workflow, and session protocol are in `.claude/rules/` — loaded automatically by glob when editing matching files.
