# Antigravity Game Studios -- Game Studio Agent Architecture

Indie game development managed through coordinated Antigravity specialized agents and workflows.
Each agent owns a specific domain, enforcing separation of concerns and quality.

## Technology Stack

- **Engine**: Godot 4.7.0 (Source of truth: `project.yaml`)
- **Language**: GDScript
- **Version Control**: Git with trunk-based development
- **Build System**: SCons (engine), Godot Export Templates
- **Asset Pipeline**: Godot Import System + custom resource pipeline

> **Note**: Engine-specialist configurations exist for Godot, Unity, and Unreal. Always verify against `project.yaml`.

---

## Collaboration Protocol

**User-driven collaboration, not autonomous execution.**
Every task follows: **Question -> Options -> Decision -> Draft -> Approval**

- Agents MUST ask "May I write this to [filepath]?" before using `write_to_file` or `replace_file_content` (exempt: `active.md` appends, agent memory, or subagent files at designated paths; see [agent-memory.md](file:///.agents/rules/agent-memory.md)).
- Agents MUST show drafts or summaries before requesting approval.
- Multi-file changes require explicit approval for the full changeset.
- No git commits without explicit user instruction.
- A skipped or dismissed question is not an answer: act on nothing, re-ask in plain text and wait.
- Started outside this file's folder? Warn first: hooks, deny rules and collaborative modes apply when Antigravity starts here.

See `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md` for full protocol and examples.

---

## Project Structure

```text
/
├── AGENTS.md                    # Antigravity master configuration and rules
├── CLAUDE.md                    # Claude Code legacy configuration
├── project.yaml                 # Machine-readable project config — engine, modes, stage (source of truth)
├── .agents/                     # Antigravity customizations (skills, rules, hooks, plugins)
├── .claude/                     # Claude Code legacy workspace
├── <code root>/                 # Game source code (engine-specific: 'src/' for Godot, 'Assets/' for Unity, 'Source/' for Unreal)
├── assets/                      # Game assets (art, audio, vfx, shaders, data)
├── design/                      # Game design documents (gdd, narrative, levels, balance)
├── docs/                        # Technical documentation (architecture, api, postmortems)
│   └── engine-reference/        # Curated engine API snapshots (version-pinned)
├── tests/                       # Game test suites (unit, integration, performance, playtest)
├── tools/                       # Build and pipeline tools (ci, build, asset-pipeline)
├── prototypes/                  # Throwaway prototypes (outside the code root)
├── production/                  # Production management (sprints, milestones, releases)
│   ├── session-state/           # Ephemeral session state (active.md — gitignored)
│   └── session-logs/            # Session audit trail (gitignored)
└── studio-tests/                # QA for the skills/agents themselves
```

### The code root is engine-specific
- **Godot**: Code root is `src/`; tests under `tests/unit/`, `tests/integration/`.
- **Unity**: Code root is `Assets/`; tests under `Assets/Tests/EditMode/`, `Assets/Tests/PlayMode/`.
- **Unreal**: Code root is `Source/<Module>/`; tests under `Source/<Module>/Private/Tests/`.

---

## Engine Version Reference

Refer to [docs/engine-reference/godot/VERSION.md](file:///docs/engine-reference/godot/VERSION.md) for pinned engine details (Godot 4.7.0).
Always cross-reference before suggesting Godot API calls, particularly regarding post-4.3 changes.

---

## Technical Preferences

- `project.yaml` at the repo root is the primary config store — engine, specialists, naming, platform, performance, modes.
- `.claude/docs/technical-preferences.md` is the **legacy fallback**, read on demand when a key is absent from `project.yaml`.

---

## Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared parent. If no shared parent, escalate to `creative-director` for design conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files outside its designated directories without explicit delegation.
6. **Read Design Docs by Section**: Use section headings with targeted searches (`grep_search` or slice views in `view_file`) rather than whole-file reads over 40 KB.
7. **Nothing Goes Upstream**: Never file, open or comment on an issue or pull request in an engine, plugin or vendor repository, even when asked. Write a draft and the user submits it.

---

## Coding & Design Standards

- All game code must include doc comments on public APIs.
- Architecture decisions are recorded as ADRs in `docs/architecture/` per `modes.workflow`.
- Gameplay values must be data-driven (external config), never hardcoded.
- All public methods must be unit-testable (dependency injection over singletons).
- Commit messages: Use Conventional Commits format (`feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`).
- **Verification-driven development**: Write tests first when adding gameplay systems. For UI changes, verify visually. Compare expected output to actual output before marking work complete.
- Launch & Observation: Every story that changes something player-observable is verified before it closes.
- GDD standards: Follow the 8 sections (Overview, Player Fantasy, Detailed Rules, Formulas, Edge Cases, Dependencies, Tuning Knobs, Acceptance Criteria).

---

## Context Management

- **`production/session-state/active.md` is the session checkpoint.** The file is the memory, not the conversation. Read it first after any reset or major task resumption.
- **Helpers in scripts emit observations, never verdicts.** A script that scores or judges will eventually contradict a mode or override it cannot see.
