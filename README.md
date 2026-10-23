# Game Studio Agent Workflow (`game-workflow`)

A comprehensive, production-grade agentic game development workflow system supporting both **Google Antigravity** and **Claude Code**.

Designed for indie game developers and studios to orchestrate AI agents across all disciplines: Game Design, Gameplay Programming, Shaders, Narrative, Level Design, QA Testing, and Release Management.

---

## 🌟 Key Features

- **74 Production Skills**: Complete coverage of the game development lifecycle:
  - Concept & Brainstorming (`/brainstorm`, `/prototype`)
  - Systems & Level Design (`/map-systems`, `/design-system`, `/design-review`)
  - Engineering & Architecture (`/create-architecture`, `/architecture-decision`, `/dev-story`)
  - QA, Testing & Balancing (`/gate-check`, `/balance-check`, `/smoke-check`, `/qa-plan`)
  - Polish, Launch & Ops (`/perf-profile`, `/patch-notes`, `/release-checklist`, `/hotfix`)
- **14 Domain-Specific Rules**: Strict coding and architectural standards for Godot, Unity, and Unreal (Data-driven gameplay, decoupled UI, memory bounds, shader standards, unit test conventions).
- **Safety & Lifecycle Hooks**:
  - Intercepts destructive shell operations (`rm -rf`, `git push -f`, `git reset --hard`, `sudo`).
  - Enforces Conventional Commits with story tracing.
  - Validates binary file integrity and asset registries before and after tool execution.
- **Dual Engine Compatibility**:
  - **Google Antigravity**: Native `.agents/` structure, `AGENTS.md`, progressive disclosure skills, `hooks.json`.
  - **Claude Code**: Legacy support for `.claude/` structure, `CLAUDE.md`, `settings.json`.

---

## 📁 Repository Structure

```text
game-workflow/
├── AGENTS.md                  # Antigravity master configuration and rules
├── CLAUDE.md                  # Claude Code master configuration
├── project.yaml               # Standard machine-readable game configuration template
├── install.sh                 # One-click workflow installer script
├── .agents/                   # Antigravity customizations
│   ├── hooks.json             # Lifecycle hooks configuration
│   ├── hooks/                 # Security dispatcher & post-tool validators
│   ├── rules/                 # 14 domain-specific rule markdown files
│   ├── scripts/               # Helper and migration scripts
│   └── skills/                # 74 Antigravity skills (YAML frontmatter + progressive load)
├── .claude/                   # Claude Code legacy workspace
│   ├── agents/                # 49 specialized agent personas
│   ├── docs/                  # Architectural guidelines & coordination rules
│   ├── hooks/                 # Shell validation hooks
│   ├── rules/                 # Markdown rules for Claude Code
│   ├── scripts/               # CLI helpers & status scripts
│   └── skills/                # 74 Claude Code skills
├── docs/                      # General documentation & engine references
│   ├── COLLABORATIVE-DESIGN-PRINCIPLE.md
│   └── engine-reference/      # Version-pinned engine documentation (e.g. Godot 4.7.0)
└── templates/                 # Subdirectory rule templates (src/, design/, docs/, studio-tests/)
```

---

## 🚀 Quick Start & Installation

### Install into an existing game project

You can install this workflow into any game repository using the provided `install.sh`:

```bash
# 1. Clone or navigate to this workflow repository
cd ~/projects/game-workflow

# 2. Install into your game project (copies all Antigravity & Claude workflows)
./install.sh ~/projects/my-game

# 3. (Optional) Install only for Antigravity:
./install.sh ~/projects/my-game --mode antigravity

# 4. (Optional) Link as symlinks to keep in sync with upstream workflow changes:
./install.sh ~/projects/my-game --method symlink
```

---

## 🛠️ Usage with Google Antigravity

When you open a project with this workflow in Antigravity:
1. **Hierarchical Rules**: Antigravity automatically discovers `AGENTS.md` at root and in subdirectories (`design/AGENTS.md`, `src/AGENTS.md`, etc.), enforcing coding rules as you navigate.
2. **Progressive Skills**: All 74 skills in `.agents/skills/` are registered. Only metadata is loaded initially; full runbooks are read on-demand when invoked or needed.
3. **Safety Protection**: `.agents/hooks.json` automatically intercepts shell and file modification tools to ensure project safety.

---

## 📜 Collaboration Protocol

This workflow enforces **User-driven collaboration, not autonomous execution**:
Every major task follows: **Question -> Options -> Decision -> Draft -> Approval**.
