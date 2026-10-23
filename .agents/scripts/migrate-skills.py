#!/usr/bin/env python3
"""Batch migrate Claude skills to Antigravity skills.
Copies all skill directories from .claude/skills/ to .agents/skills/
and adapts SKILL.md frontmatter and interpolation macros.
"""

import os
import shutil
import re

SRC_DIR = ".claude/skills"
DST_DIR = ".agents/skills"

def adapt_skill_content(content: str) -> str:
    # 1. Parse YAML frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not fm_match:
        return content

    fm_text, body = fm_match.group(1), fm_match.group(2)
    name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    desc_match = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)

    name = name_match.group(1).strip().strip('"\'') if name_match else "unknown-skill"
    desc = desc_match.group(1).strip().strip('"\'') if desc_match else ""

    new_fm = f"---\nname: {name}\ndescription: >-\n  {desc}\n---"

    # 2. Convert dynamic shell inclusions `!`bash ...`` to instructional blockquotes
    def replace_bash_macro(match):
        cmd = match.group(1).replace("${CLAUDE_SKILL_DIR}/../../hooks/", ".claude/hooks/")
        return f"\n> **Config Resolution**: If needed, resolve project config by running:\n> `bash {cmd}`\n"

    body = re.sub(r'!`bash\s+"?\${CLAUDE_SKILL_DIR}/([^`]+)"?`', replace_bash_macro, body)
    body = re.sub(r'!`bash\s+([^`]+)`', r'\n> **Config**: `\1`\n', body)

    # 3. Adapt AskUserQuestion references to ask_question
    body = body.replace("AskUserQuestion", "ask_question")

    return f"{new_fm}\n{body}"

def main():
    if not os.path.exists(SRC_DIR):
        print(f"Source directory {SRC_DIR} not found.")
        return

    os.makedirs(DST_DIR, exist_ok=True)
    skills = [d for d in os.listdir(SRC_DIR) if os.path.isdir(os.path.join(SRC_DIR, d))]
    print(f"Discovered {len(skills)} skills in {SRC_DIR}.")

    migrated = 0
    for skill_name in sorted(skills):
        src_skill = os.path.join(SRC_DIR, skill_name)
        dst_skill = os.path.join(DST_DIR, skill_name)

        # Copy directory structure (except existing customized ones if any)
        if not os.path.exists(dst_skill):
            shutil.copytree(src_skill, dst_skill)
        else:
            # Sync any missing files
            for root, dirs, files in os.walk(src_skill):
                rel_path = os.path.relpath(root, src_skill)
                target_root = os.path.join(dst_skill, rel_path)
                os.makedirs(target_root, exist_ok=True)
                for f in files:
                    s_file = os.path.join(root, f)
                    d_file = os.path.join(target_root, f)
                    if not os.path.exists(d_file):
                        shutil.copy2(s_file, d_file)

        skill_md_path = os.path.join(dst_skill, "SKILL.md")
        if os.path.exists(skill_md_path):
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            adapted = adapt_skill_content(content)
            with open(skill_md_path, "w", encoding="utf-8") as f:
                f.write(adapted)

        migrated += 1

    print(f"Successfully migrated {migrated} skills to {DST_DIR}.")

if __name__ == "__main__":
    main()
