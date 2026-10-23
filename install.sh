#!/usr/bin/env bash
# Game Workflow Installer
# Install Antigravity and/or Claude Code game studio workflow into a target game project.
#
# Usage:
#   ./install.sh <target-project-dir> [options]
#
# Options:
#   --mode <antigravity|claude|both>   Workflow system to install (default: both)
#   --method <copy|symlink>            Install method: copy files or symlink (default: copy)
#   --help                             Show this help message

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR=""
MODE="both"
METHOD="copy"

print_usage() {
  echo "Usage: $0 <target-project-dir> [options]"
  echo ""
  echo "Options:"
  echo "  --mode <antigravity|claude|both>   (default: both)"
  echo "  --method <copy|symlink>            (default: copy)"
  echo "  --help                             Show this help message"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)
      MODE="$2"
      shift 2
      ;;
    --method)
      METHOD="$2"
      shift 2
      ;;
    --help)
      print_usage
      ;;
    -*)
      echo "Unknown option: $1"
      print_usage
      ;;
    *)
      if [[ -z "$TARGET_DIR" ]]; then
        TARGET_DIR="$1"
        shift
      else
        echo "Unexpected argument: $1"
        print_usage
      fi
      ;;
  esac
done

if [[ -z "$TARGET_DIR" ]]; then
  echo "Error: Target project directory is required."
  print_usage
fi

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "Target directory '$TARGET_DIR' does not exist. Creating it..."
  mkdir -p "$TARGET_DIR"
fi

TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"
echo "Installing game-workflow into: $TARGET_DIR (mode: $MODE, method: $METHOD)"

sync_path() {
  local src="$1"
  local dest="$2"

  if [[ "$METHOD" == "symlink" ]]; then
    ln -sfn "$src" "$dest"
    echo "  [link] $dest -> $src"
  else
    if [[ -d "$src" ]]; then
      mkdir -p "$dest"
      cp -r "$src"/* "$dest"/
    else
      cp "$src" "$dest"
    fi
    echo "  [copy] $dest"
  fi
}

# 1. Base project configuration
if [[ ! -f "$TARGET_DIR/project.yaml" ]]; then
  cp "$SCRIPT_DIR/project.yaml" "$TARGET_DIR/project.yaml"
  echo "  [init] project.yaml created"
fi

# 2. Antigravity workflow
if [[ "$MODE" == "antigravity" || "$MODE" == "both" ]]; then
  echo "Installing Antigravity workflow (.agents/ & AGENTS.md)..."
  sync_path "$SCRIPT_DIR/.agents" "$TARGET_DIR/.agents"
  sync_path "$SCRIPT_DIR/AGENTS.md" "$TARGET_DIR/AGENTS.md"
fi

# 3. Claude Code workflow
if [[ "$MODE" == "claude" || "$MODE" == "both" ]]; then
  echo "Installing Claude Code workflow (.claude/ & CLAUDE.md)..."
  sync_path "$SCRIPT_DIR/.claude" "$TARGET_DIR/.claude"
  sync_path "$SCRIPT_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
fi

# 4. Engine reference docs
mkdir -p "$TARGET_DIR/docs"
if [[ -d "$SCRIPT_DIR/docs/engine-reference" ]]; then
  sync_path "$SCRIPT_DIR/docs/engine-reference" "$TARGET_DIR/docs/engine-reference"
fi

# 5. Templates for subdirectories
if [[ -d "$SCRIPT_DIR/templates/rules" ]]; then
  for dir in design src docs studio-tests; do
    if [[ -d "$TARGET_DIR/$dir" ]]; then
      if [[ "$MODE" == "claude" || "$MODE" == "both" ]]; then
        [[ -f "$SCRIPT_DIR/templates/rules/$dir/CLAUDE.md" ]] && cp "$SCRIPT_DIR/templates/rules/$dir/CLAUDE.md" "$TARGET_DIR/$dir/"
      fi
      if [[ "$MODE" == "antigravity" || "$MODE" == "both" ]]; then
        [[ -f "$TARGET_DIR/$dir/CLAUDE.md" ]] && ln -sf CLAUDE.md "$TARGET_DIR/$dir/AGENTS.md"
      fi
    fi
  done
fi

echo "Game workflow successfully installed!"
