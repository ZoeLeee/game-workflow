#!/usr/bin/env python3
"""Antigravity PostToolUse Hook Dispatcher
Executes post-tool validators (e.g. asset validation) and outputs empty JSON {}.
"""

import sys
import json
import subprocess
import os

def main():
    try:
        raw_input = sys.stdin.read()
        if raw_input.strip():
            data = json.loads(raw_input)
            tool_call = data.get("toolCall", {})
            args = tool_call.get("args", {})
            target_file = args.get("TargetFile", "")

            # If an asset was modified, trigger validate-assets.sh
            if target_file and target_file.startswith("assets/") and os.path.exists(".claude/hooks/validate-assets.sh"):
                subprocess.run(
                    ["bash", ".claude/hooks/validate-assets.sh"],
                    text=True,
                    capture_output=True
                )
    except Exception:
        pass

    # Antigravity PostToolUse contract expects an empty JSON object
    json.dump({}, sys.stdout)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
