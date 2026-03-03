#!/usr/bin/env python3
"""
PreCompact Hook: Auto-generate HANDOVER when Claude Code compresses context.

When Claude Code runs out of context window, it triggers "compact" — summarizing
the conversation to free up space. This hook runs BEFORE that happens, capturing
the full conversation into a structured handover document.

The next session reads HANDOVER-latest.md (see CLAUDE.md) and picks up seamlessly.

How it works:
1. Reads transcript_path from stdin JSON (provided by Claude Code)
2. Parses the JSONL transcript file to extract conversation text
3. Sends parsed text to `claude -p` (with tools disabled) to generate handover
4. Saves to local/session-notes/HANDOVER-latest.md

Key design: --tools "" disables all tools so the model generates text directly
in one turn (--max-turns 1), avoiding agentic loops that cause timeouts.

Setup: See .claude/settings.json for hook configuration.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Project root (parent of .claude directory)
PROJECT_ROOT = Path(__file__).parent.parent.parent
HANDOVER_PATH = PROJECT_ROOT / "local" / "session-notes" / "HANDOVER-latest.md"

HANDOVER_PROMPT = """You are generating a HANDOVER document for the next Claude session.
This document should allow a fresh Claude instance to continue the work seamlessly.
Write in the same language the user was using.

Analyze the conversation transcript and create a structured handover with:

## Current Task
What was being worked on? Be specific about the exact task and progress.

## Progress Made
- What was completed?
- What decisions were made and why?

## In Progress (if any)
- What was started but not finished?
- Exactly where did we leave off? (file names, line numbers if relevant)

## Key Context
- Important decisions or preferences expressed by the user
- Any constraints or requirements mentioned
- Relevant file paths

## Next Steps
What should be done next to continue this work?

## Open Questions (if any)
Anything that was unclear or needs user input?

Be concise but complete. Focus on information needed to continue the work.
"""


def read_transcript(transcript_path: str, max_chars: int = 80000) -> str:
    """Read JSONL transcript file, extract conversation text, truncate to last max_chars."""
    try:
        path = Path(transcript_path)
        if not path.exists():
            return f"[Transcript file not found: {transcript_path}]"

        lines = []
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                raw_line = raw_line.strip()
                if not raw_line:
                    continue
                try:
                    entry = json.loads(raw_line)
                except json.JSONDecodeError:
                    continue

                msg = entry.get("message")
                if not msg:
                    continue

                role = msg.get("role", "unknown")
                content = msg.get("content", "")

                if isinstance(content, str):
                    if content.strip():
                        lines.append(f"[{role}]: {content}")
                elif isinstance(content, list):
                    parts = []
                    for block in content:
                        if isinstance(block, dict):
                            btype = block.get("type", "")
                            if btype == "text":
                                text = block.get("text", "")
                                if text.strip():
                                    parts.append(text)
                            elif btype == "tool_use":
                                name = block.get("name", "unknown")
                                parts.append(f"[Tool: {name}]")
                            elif btype == "tool_result":
                                result_content = str(block.get("content", ""))
                                parts.append(f"[Tool result: {result_content[:200]}]")
                    if parts:
                        lines.append(f"[{role}]: {' '.join(parts)}")

        full_text = "\n".join(lines)

        if len(full_text) > max_chars:
            full_text = "...[truncated earlier conversation]...\n" + full_text[-max_chars:]

        return full_text

    except Exception as e:
        return f"[Error reading transcript: {str(e)}]"


def generate_handover(transcript: str) -> str:
    """Use claude -p with tools disabled for fast, single-turn generation."""
    try:
        input_text = f"{HANDOVER_PROMPT}\n\n---\n\nCONVERSATION TRANSCRIPT:\n\n{transcript}"

        result = subprocess.run(
            ["claude", "-p", "--max-turns", "1", "--tools", "", "--output-format", "text"],
            input=input_text,
            capture_output=True,
            text=True,
            timeout=120,
            cwd="/tmp"  # Prevents loading project MCP tools
        )

        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        elif result.stderr:
            return f"Error generating handover: {result.stderr}"
        else:
            return "Error: Empty response from claude"

    except subprocess.TimeoutExpired:
        return "Error: Handover generation timed out"
    except FileNotFoundError:
        return "Error: claude CLI not found"
    except Exception as e:
        return f"Error generating handover: {str(e)}"


def save_handover(content: str, trigger: str = "unknown") -> None:
    """Save handover to file."""
    HANDOVER_PATH.parent.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"""# HANDOVER - Session Context
**Generated:** {timestamp}
**Trigger:** {trigger}
**Purpose:** Continue work in next session

---

"""

    full_content = header + content
    HANDOVER_PATH.write_text(full_content, encoding="utf-8")


def main():
    """Parse stdin JSON -> read transcript_path -> generate -> save."""
    try:
        stdin_data = sys.stdin.read()

        if not stdin_data.strip():
            print("HOOK: No input data received, skipping handover generation")
            return

        try:
            hook_input = json.loads(stdin_data)
        except json.JSONDecodeError:
            print("HOOK: Invalid JSON input, skipping")
            return

        transcript_path = hook_input.get("transcript_path", "")
        trigger = hook_input.get("trigger", "unknown")

        if not transcript_path:
            print("HOOK: No transcript_path in input, skipping")
            return

        print(f"HOOK: Reading transcript from {transcript_path}")
        transcript = read_transcript(transcript_path)

        if not transcript or transcript.startswith("[Error") or transcript.startswith("[Transcript"):
            print(f"HOOK: Problem reading transcript: {transcript[:200]}")
            save_handover(f"Error reading transcript: {transcript}", trigger)
            return

        print(f"HOOK: Transcript extracted: {len(transcript)} chars")
        print("HOOK: Generating handover (tools disabled, single turn)...")

        handover_content = generate_handover(transcript)
        save_handover(handover_content, trigger)
        print(f"HOOK: Handover saved to {HANDOVER_PATH.relative_to(PROJECT_ROOT)}")

    except Exception as e:
        print(f"HOOK ERROR: {str(e)}")


if __name__ == "__main__":
    main()
