# Example Skill

<!--
  SKILL.md is the main instruction file for a skill.
  It's loaded into context when the user invokes this skill.

  Think of skills as specialized "modes" for Claude Code — each skill
  gives Claude domain expertise, workflows, and guardrails for a specific task.

  Real-world examples: code-review, research, copywriting, deployment, SEO audit.
-->

## Before You Start

<!--
  List files Claude should read before starting work.
  These give Claude the context it needs to do the job well.
  Reference files stay in references/ — they're loaded on demand, not always.
-->

**Read required context:**
```
references/guidelines.md    # Domain-specific guidelines
```

**Read learned patterns:**
```
LEARNED.md                  # What worked (and didn't) in previous sessions
```

---

## Workflow

<!--
  Step-by-step process Claude follows when this skill is invoked.
  Be specific — Claude follows these literally.
-->

1. Read the required context files listed above
2. Understand the user's request
3. Follow the rules below
4. Verify output against the checklist

---

## Rules

<!--
  Guardrails and conventions for this skill.
  These prevent common mistakes and keep output consistent.
  Write them as clear imperatives — "Do X", "Never Y", "Always Z".
-->

- Always verify facts before including them in output
- Use project terminology consistently (see references/)
- Ask the user when requirements are ambiguous — don't guess
- Keep output focused and actionable

---

## Self-Learning

<!--
  Skills improve over time. LEARNED.md captures what Claude discovers
  during real usage — patterns that work, gotchas, user preferences.

  Claude updates LEARNED.md proactively after solving non-trivial problems.
  This is what makes skills get better with each session.
-->

Read `LEARNED.md` before starting. Update it when you discover:
- Patterns that work well for this skill
- Common mistakes or gotchas
- User preferences learned during use

**Consolidation (target ~50 lines):**
Before adding a new entry, check file length. If approaching 50 lines:
1. Merge duplicate/overlapping entries
2. Remove entries that haven't been reinforced
3. Keep only entries that would change behavior
