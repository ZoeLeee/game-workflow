# Godot Engine — Version Reference

| Field | Value |
|-------|-------|
| **Engine Version** | Godot 4.7.0 |
| **Installed at pin time** | 4.7.0 — `/mnt/d/softwares/Godot_v4.7-stable_win64.exe/godot47.exe --version` returned `4.7.stable.official.5b4e0cb0f` (probed 2026-10-17) |
| **Release Date** | 4.7 stable: 2026-06-18 (latest 4.7 maintenance, 4.7.2: 2026-08-18) |
| **Project Pinned** | 2026-10-17 |
| **Last Docs Verified** | 2026-10-17 |
| **LLM Knowledge Cutoff** | May 2025 |

## Knowledge Gap Warning

The LLM's training data likely covers Godot up to ~4.3. Versions 4.4 through 4.7
introduced significant changes that the model does NOT know about.
Always cross-reference this directory before suggesting Godot API calls.

4.7 is a **HIGH RISK** pin: it postdates the training cutoff by more than a year
and by four feature releases.

## Installed-Version Gap Warning

The warning above is one-directional — it covers the **model** knowing less than
this pin. The reverse gap is real and `/setup-engine` §3 creates it deliberately
("pin the newer one and upgrade later"): this reference can sit **ahead of the
installed editor**, and an agent citing it correctly then emits APIs that do not
compile locally. **Check `Installed at pin time` above before trusting a
version-qualified claim.**

At this pin the two agree: `project.yaml` pins `engine.version: "4.7.0"` and the
probed editor reports `4.7.stable`. The latest maintenance release, **4.7.2**,
exists upstream and is backward-compatible with 4.7.0; upgrading to it is
optional and would require re-running `/setup-engine` to restamp this table.

## Post-Cutoff Version Timeline

| Version | Release | Risk Level | Key Theme |
|---------|---------|------------|-----------|
| 4.5 | Sep 2025 | HIGH | Accessibility (AccessKit), variadic args, @abstract, shader baker, SMAA |
| 4.6 | Jan 2026 | HIGH | Jolt default, glow rework, D3D12 default on Windows, IK restored |
| 4.7 | Jun 2026 | HIGH | HDR output, AreaLight3D, Asset Store, Control offset transforms, Android XR |

## Known Issue for This Project

The project renders its greybox battlefield with `Node2D._draw()`. In 4.7,
`CanvasItem` no longer adds the antialiasing feather when drawing lines
(GH-105122), so **lines render thinner than they did in 4.6** — line widths on
this project were written against 4.6-era assumptions. See
`breaking-changes.md` § 4.6 → 4.7.

## Before the Cutoff

- Official docs: https://docs.godotengine.org/en/stable/
- 4.6→4.7 migration guide: https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.7.html
- 4.7 release page: https://godotengine.org/releases/4.7/
- 4.7 changelog: https://raw.githubusercontent.com/godotengine/godot/4.7-stable/CHANGELOG.md
- Godot downloads (current stable): https://godotengine.org/download/
