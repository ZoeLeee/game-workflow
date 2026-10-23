# Godot — Breaking Changes

Last verified: 2026-10-17

Changes between Godot versions, focused on post-LLM-cutoff changes (4.4+).

## 4.6 → 4.7 (Jun 2026 — POST-CUTOFF, HIGH RISK)

Sourced from the official migration guide
(`https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.7.html`).

> The guide's own summary: "For most games and apps made with 4.6 it should be
> relatively safe to migrate to 4.7." The **Changed defaults** table below is the
> part that bites silently — defaults are not errors, so nothing reports them.

### API breaking changes

| Subsystem | Change | Details |
|-----------|--------|---------|
| GUI (RichTextLabel) | Enum `ImageUpdateMask.UPDATE_WIDTH_IN_PERCENT` renamed to `UPDATE_WIDTH_UNIT` | **Not GDScript-compatible** — the one rename that breaks existing `.gd` code |
| GUI (RichTextLabel) | `add_image` / `update_image`: `width_in_percent` / `height_in_percent` renamed to `width_unit` / `height_unit`, type `bool` → `RichTextLabel.ImageUnit` | Source-compatible for C#, not for C# binaries |
| GUI (RichTextLabel) | `add_image` / `update_image`: `width` / `height` parameter type `int` → `float` | |
| GUI (Control) | Property `accessibility_live` type changed `DisplayServer.AccessibilityLiveMode` → `AccessibilityServer.AccessibilityLiveMode` | |
| Audio | `AudioEffectSpectrumAnalyzer.tap_back_pos` property **removed** | GDScript-incompatible |
| Rendering | `ImageTexture.get_format()` and `PortableCompressedTexture2D.get_format()` moved to base class `Texture2D` | Source-compatible |
| Core | `Object.is_class` parameter type `String` → `StringName` | |
| Core | `OptimizedTranslation.generate` return type `void` → `bool` | |
| Core | `ZIPPacker.start_file` adds optional `permissions` and `modified_time` | |
| Physics 2D | `PhysicsServer2D.body_set_shape_as_one_way_collision` adds optional `direction`; the GDExtension virtual `_body_set_shape_as_one_way_collision` adds a required `direction` | GDExtension-incompatible |
| 2D / 3D | `CPUParticles2D/3D` and `GPUParticles2D/3D` `request_particles_process` add optional `process_time_residual` | |
| Rendering (server) | `RenderingServer.particles_request_process_time` renames `time` → `process_time`, adds optional `process_time_residual`; `viewport_set_size` adds optional `view_count` | |
| Text | `Font.find_variation` adds optional `palette_index` and `custom_colors` | |
| Text / Tree | `TreeItem.select` adds optional `set_as_cursor` | |
| Animation | `AnimationNodeBlendSpace1D/2D.add_blend_point` adds optional `name`; `Animation.length` type metadata `float` → `double` | |
| Editor | Constants `IMPORT_ANIMATION`, `IMPORT_DISCARD_MESHES_AND_MATERIALS`, `IMPORT_FAIL_ON_MISSING_DEPENDENCIES`, `IMPORT_FORCE_DISABLE_MESH_COMPRESSION`, `IMPORT_GENERATE_TANGENT_ARRAYS`, `IMPORT_SCENE`, `IMPORT_USE_NAMED_SKIN_BINDS` moved into enum `ImportFlags` on `EditorSceneFormatImporter` | |
| Editor | `EditorVCSInterface._commit` adds an `amend` parameter | GDExtension-incompatible |
| XR | `OpenXRExtensionWrapper._on_register_metadata` adds a required `interaction_profile_metadata`; `OpenXRSpatialAnchorCapability.create_new_anchor` adds optional `next` | |

### Behavior changes

| Subsystem | Change | Details |
|-----------|--------|---------|
| **2D** | `CanvasItem` no longer adds the antialiasing feather when drawing lines | GH-105122. Lines appear **thinner** than intended. Projects relying on the old behavior must draw a greater `line_width`. **Affects this project's `_draw()` greybox.** |
| **Input** | Mouse and keyboard device IDs changed from `0` to `InputEvent.DEVICE_ID_MOUSE` / `InputEvent.DEVICE_ID_KEYBOARD` | GH-116274. Some joypads use `0` as their ID. Compare `InputEvent.device` against the new constants instead of the literal `0`. |
| **GDScript** | Setting an element of a packed array no longer calls the setter for the whole packed-array property | GH-113228 |
| **GDScript** | Methods inheriting from a method with a typed return now inherit the return type, requiring an explicit `return` in the override | GH-115763. Add `return null` at the end of the method to fix the error. |
| Rendering (shader) | The `LinearToSRGB` visual shader node no longer clamps to `[0.0, 1.0]` under the Mobile or Forward+ renderer | GH-113956. **This project pins Forward+.** |
| Audio | Default `area_mask` for `AudioStreamPlayer` changed `1` → `0` (disabled) | GH-107679. Projects using `audio_bus_override` on `Area2D`/`Area3D` with the default mask must reset it to layer 1. |
| Physics 3D (Jolt) | `WorldBoundaryShape3D.plane.d` sign convention flipped | GH-118948. Flip the sign yourself to match 4.6. 3D only. |
| Physics 3D (Jolt) | `SoftBody3D` no longer defaults its mass to `0`; `linear_stiffness` applied differently | GH-116041. Every `SoftBody3D` needs re-tuning. 3D only. |
| Physics 3D (Jolt) | `Area3D` now reports overlaps with `SoftBody3D` | GH-114198. 3D only. |

### Changed defaults

Newly created projects get these; existing projects keep their stored values.

| Subsystem | Property / Parameter | Old Default | New Default |
|-----------|----------------------|-------------|-------------|
| **ProjectSettings** | `display/window/stretch/mode` | `disabled` | `canvas_items` |
| **ProjectSettings** | `display/window/stretch/aspect` | `keep` | `expand` |
| ProjectSettings | `rendering/reflections/sky_reflections/roughness_layers` | 7 | 8 |
| Import | `ResourceImporterDynamicFont.hinting` | 1 | 3 |
| GUI | `RichTextLabel.add_image` / `update_image` parameter `width_in_percent` | `false` | `0` |
| GUI | `RichTextLabel.add_image` / `update_image` parameter `height_in_percent` | `false` | `0` |
| Animation | `LookAtModifier3D.relative` | `true` | `false` |

> The two `ProjectSettings` stretch rows matter most for a pixel-art project:
> `canvas_items` + `expand` is a different scaling model from `disabled` + `keep`,
> and pixel art is exactly what the difference is visible on. Not project-relevant
> here (no `project.godot` settings beyond the scaffold), but check it when the
> first scene and its stretch configuration are authored.

## 4.5 → 4.6 (Jan 2026 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Physics | Jolt is now the DEFAULT 3D physics engine | New projects use Jolt automatically. Existing projects keep their setting. Some HingeJoint3D properties (like `damp`) only work with GodotPhysics. |
| Rendering | Glow processes BEFORE tonemapping | Was after tonemapping. Scenes with glow will look different. Adjust intensity/blend in WorldEnvironment. |
| Rendering | D3D12 default on Windows | Was Vulkan. For better driver compatibility. |
| Rendering | AgX tonemapper new controls | White point and contrast parameters added. |
| Core | Quaternion initializes to identity | Was zero. Unlikely to affect most code but technically breaking. |
| UI | Dual-focus system | Mouse/touch focus now separate from keyboard/gamepad focus. Visual feedback differs by input method. |
| Animation | IK system fully restored | CCDIK, FABRIK, Jacobian IK, Spline IK, TwoBoneIK via SkeletonModifier3D nodes. |
| Editor | New "Modern" theme default | Grayscale replaces blue-tint. Restore: Editor Settings → Interface → Theme → Style: Classic |
| Editor | "Select Mode" keybind changed | New "Select Mode" (v key) prevents accidental transforms. Old mode renamed "Transform Mode" (q key). |
| 2D | TileMapLayer scene tile rotation | Scene tiles can now be rotated like atlas tiles. |
| Localization | CSV plural form support | No longer requires Gettext for plurals. Context columns added. |
| C# | Automatic string extraction | Translation strings auto-extracted from C# code. |
| Plugins | New EditorDock class | Specialized container for plugin docks with layout control. |

## 4.4 → 4.5 (Sep 2025 — POST-CUTOFF, HIGH RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| GDScript | Variadic arguments added | Functions can accept `...` arbitrary params — new language feature |
| GDScript | `@abstract` decorator | Abstract classes and methods now enforceable |
| GDScript | Script backtracing | Detailed call stacks available even in Release builds |
| Rendering | Stencil buffer support | New capability for advanced visual effects |
| Rendering | SMAA 1x antialiasing | New post-processing AA option |
| Rendering | Shader Baker | Pre-compiles shaders — reportedly 20x faster startup on some demos |
| Rendering | Bent normal maps, specular occlusion | New material features |
| Accessibility | Screen reader support | Control nodes work with accessibility tools via AccessKit |
| Editor | Live translation preview | Test GUI layouts in different languages in-editor |
| Physics | 3D interpolation rearchitected | Moved from RenderingServer to SceneTree. API unchanged but internals differ. |
| Animation | BoneConstraint3D | New: AimModifier3D, CopyTransformModifier3D, ConvertTransformModifier3D |
| Resources | `duplicate_deep()` added | New explicit method for deep duplication of nested resources |
| Navigation | Dedicated 2D navigation server | No longer a proxy to 3D navigation; smaller export for 2D games |
| UI | FoldableContainer node | New accordion-style container for collapsible UI sections |
| UI | Recursive Control behavior | Disable mouse/focus interactions across entire node hierarchies |
| Platform | visionOS export support | New platform target |
| Platform | SDL3 gamepad driver | Delegated gamepad handling to SDL library |
| Platform | Android 16KB page support | Required for Google Play targeting Android 15+ |

## 4.3 → 4.4 (Mar 2025 — BEFORE CUTOFF, VERIFY)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Core | `FileAccess.store_*` return `bool` | Was `void`. Methods: `store_8`, `store_16`, `store_32`, `store_64`, `store_buffer`, `store_csv_line`, `store_double`, `store_float`, `store_half`, `store_line`, `store_pascal_string`, `store_real`, `store_string`, `store_var` |
| Core | `OS.execute_with_pipe` | Added optional `blocking` parameter |
| Core | `RegEx.compile/create_from_string` | Added optional `show_error` parameter |
| Rendering | `RenderingDevice.draw_list_begin` | Many parameters removed; `breadcrumb` parameter added |
| Rendering | `Shader.set_default_texture_parameter()` / `get_default_texture_parameter()` | Parameter/return type changed from `Texture2D` to `Texture`; the shading language did not change |
| Particles | `.restart()` method | Added optional `keep_seed` parameter (CPU/GPU 2D/3D) |
| GUI | `RichTextLabel.push_meta` | Added optional `tooltip` parameter |
| GUI | `GraphEdit.connect_node` | Added optional `keep_alive` parameter |

## 4.2 → 4.3 (In Training Data — LOW RISK)

| Subsystem | Change | Details |
|-----------|--------|---------|
| Animation | `Skeleton3D.add_bone` returns `int32` | Was `void` |
| Animation | `bone_pose_updated` signal | Replaced by `skeleton_updated` |
| TileMap | `TileMapLayer` replaces `TileMap` | One node per layer instead of multi-layer single node |
| Navigation | `NavigationRegion2D` | Removed `avoidance_layers`, `constrain_avoidance` properties |
| Editor | `EditorSceneFormatImporterFBX` | Renamed to `EditorSceneFormatImporterFBX2GLTF` |
| Animation | AnimationMixer base class | AnimationPlayer and AnimationTree now extend AnimationMixer |

## Sources

- Official docs: https://docs.godotengine.org/en/stable/
- 4.6→4.7 migration: https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.7.html
- 4.5→4.6 migration: https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.6.html
- 4.4→4.5 migration: https://docs.godotengine.org/en/stable/tutorials/migrating/upgrading_to_godot_4.5.html
- Changelog: https://github.com/godotengine/godot/blob/master/CHANGELOG.md
- Release notes: https://godotengine.org/releases/4.7/ (4.6: https://godotengine.org/releases/4.6/)
- Releases and dates: https://github.com/godotengine/godot/releases
