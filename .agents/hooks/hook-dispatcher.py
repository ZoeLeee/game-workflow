#!/usr/bin/env python3
"""Antigravity PreToolUse Hook Dispatcher
Enforces project security deny rules and delegates to project validation hooks.
Receives JSON on stdin, outputs decision JSON on stdout.
"""

import sys
import json
import re
import subprocess
import os

DENY_COMMAND_PATTERNS = [
    re.compile(r'\brm\s+.*-(?:[a-zA-Z]*r[a-zA-Z]*f|[a-zA-Z]*f[a-zA-Z]*r)\b', re.IGNORECASE),
    re.compile(r'\brm\s+.*(?:--recursive\s+--force|--force\s+--recursive)\b', re.IGNORECASE),
    re.compile(r'\bgit\s+(?:[^\n]*\s+)?push\b.*(?:\s+-f\b|\s+--force\b|\s+\+[a-zA-Z0-9_/-]+)', re.IGNORECASE),
    re.compile(r'\bgit\s+(?:[^\n]*\s+)?reset\s+--hard\b', re.IGNORECASE),
    re.compile(r'\bgit\s+(?:[^\n]*\s+)?clean\s+.*-(?:[a-zA-Z]*f)\b', re.IGNORECASE),
    re.compile(r'\bsudo\b', re.IGNORECASE),
    re.compile(r'\bchmod\s+777\b', re.IGNORECASE),
]

DENY_FILE_PATTERNS = [
    re.compile(r'(?:^|/)\.env(?:$|\..*)'),
    re.compile(r'\.(?:uasset|umap)$', re.IGNORECASE),
]

def respond(decision: str, reason: str = ""):
    output = {"decision": decision}
    if reason:
        output["reason"] = reason
    json.dump(output, sys.stdout)
    sys.stdout.flush()
    sys.exit(0)

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            respond("allow")
        data = json.loads(raw_input)
    except Exception:
        respond("allow")

    tool_call = data.get("toolCall", {})
    tool_name = tool_call.get("name", "")
    args = tool_call.get("args", {})

    # 1. run_command safety & validation
    if tool_name == "run_command":
        cmd = args.get("CommandLine", "")

        # Deny dangerous commands
        for pat in DENY_COMMAND_PATTERNS:
            if pat.search(cmd):
                respond("deny", f"Security Policy: Blocked dangerous command execution matching rule: {pat.pattern}")

        # Delegate git commit checks
        if "git commit" in cmd and os.path.exists(".claude/hooks/validate-commit.sh"):
            claude_payload = json.dumps({
                "tool_name": "Bash",
                "tool_input": {"command": cmd}
            })
            res = subprocess.run(
                ["bash", ".claude/hooks/validate-commit.sh"],
                input=claude_payload,
                text=True,
                capture_output=True
            )
            if res.returncode != 0:
                reason = res.stderr.strip() or res.stdout.strip() or "Git commit validation failed."
                respond("deny", reason)

        # Delegate git push checks
        if "git push" in cmd and os.path.exists(".claude/hooks/validate-push.sh"):
            claude_payload = json.dumps({
                "tool_name": "Bash",
                "tool_input": {"command": cmd}
            })
            res = subprocess.run(
                ["bash", ".claude/hooks/validate-push.sh"],
                input=claude_payload,
                text=True,
                capture_output=True
            )
            if res.returncode != 0:
                reason = res.stderr.strip() or res.stdout.strip() or "Git push validation failed."
                respond("deny", reason)

    # 2. File edit & write safety & validation
    elif tool_name in ("write_to_file", "replace_file_content", "multi_replace_file_content"):
        target_file = args.get("TargetFile", "")
        for pat in DENY_FILE_PATTERNS:
            if pat.search(target_file):
                respond("deny", f"Security Policy: Modifying protected file ({target_file}) is blocked.")

        if os.path.exists(".claude/hooks/validate-write.sh"):
            claude_payload = json.dumps({
                "tool_name": "Write" if tool_name == "write_to_file" else "Edit",
                "tool_input": {
                    "file_path": target_file,
                    "content": args.get("CodeContent", "")
                }
            })
            res = subprocess.run(
                ["bash", ".claude/hooks/validate-write.sh"],
                input=claude_payload,
                text=True,
                capture_output=True
            )
            if res.returncode != 0:
                reason = res.stderr.strip() or res.stdout.strip() or f"Write validation failed for {target_file}."
                respond("deny", reason)

    # 3. File read safety
    elif tool_name == "view_file":
        abs_path = args.get("AbsolutePath", "")
        if re.search(r'(?:^|/)\.env(?:$|\..*)', abs_path):
            respond("deny", "Security Policy: Reading .env files is blocked.")

    respond("allow")

if __name__ == "__main__":
    main()
