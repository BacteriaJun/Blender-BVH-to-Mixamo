# BVH Motion Retargeter v3.2.0

[![CI](https://github.com/BacteriaJun/BVH-Motion-Retargeter/actions/workflows/ci.yml/badge.svg)](https://github.com/BacteriaJun/BVH-Motion-Retargeter/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A Blender add-on for retargeting BVH motion capture data to Mixamo, Unreal Engine 5 humanoid, and VRM body rigs, with integrated FBX export presets for production-oriented animation workflows.

一个用于 Blender 的 BVH 动捕重定向插件。它可以将 BVH 动作转换并绑定到 Mixamo 标准骨骼、UE5 Humanoid 风格骨骼，以及 VRM 的 J_Bip 躯体骨骼，并提供内置 FBX 导出预设，减少手动导出配置错误。

---

## Overview | 项目简介

**BVH Motion Retargeter** is designed for practical motion-capture reuse in Blender. It provides a stable constraint-bake retargeting pipeline that imports BVH motion, applies a configurable source mapping, transfers the animation to a selected or generated target rig, bakes the result into keyframes, and optionally exports the result as a Mixamo-style or Unreal Engine 5-friendly FBX file.

本插件面向真实动捕工作流，重点解决 BVH 动作文件在不同人物骨骼体系之间复用的问题。插件以稳定的 **Constraint Bake** 约束烘焙流程为核心，支持 BVH 导入、骨骼映射、目标骨骼绑定、动画烘焙、曲线简化，以及 Mixamo / UE5 两套 FBX 导出预设。

v3.2.0 is a release-oriented version. It keeps the proven Mixamo-style constraint-bake workflow while adding target rig profiles, UE5 export support, VRM body-only mapping, built-in character template variants, and a more professional modular add-on structure.

v3.2.0 是面向发布的版本。它保留已验证稳定的 Mixamo 风格约束烘焙流程，并加入目标骨架配置、UE5 导出、VRM 躯体映射、内置人物模板颜色变体，以及更专业的模块化插件结构。

---

## Key Features | 核心特性

- **Stable Constraint Bake retargeting pipeline**  
  Uses Copy Location / Copy Rotation constraints and Blender NLA baking to transfer BVH animation into real keyframes.  
  使用 Copy Location / Copy Rotation 约束与 Blender NLA Bake，将 BVH 动作稳定烘焙为目标骨架关键帧。

- **Multiple target rig profiles**  
  Supports Mixamo Standard, Unreal Engine 5 Humanoid, and VRM Humanoid Body profiles.  
  支持 Mixamo 标准骨骼、UE5 Humanoid 风格骨骼，以及 VRM J_Bip 躯体骨骼。

- **Mixamo-compatible output**  
  Converts BVH motion to `mixamorig:*` bone naming and hierarchy for Mixamo-style characters.  
  可将 BVH 动作转换为 `mixamorig:*` 命名体系，适配 Mixamo 风格人物。

- **Unreal Engine 5 humanoid output**  
  Provides UE-style bone naming such as `root`, `pelvis`, `spine_01`, `upperarm_l`, `thigh_l`, and optional non-deforming helper bones.  
  支持 UE 风格骨骼命名，例如 `root`、`pelvis`、`spine_01`、`upperarm_l`、`thigh_l`，并可生成非变形辅助骨骼。

- **VRM body-only retargeting**  
  Retargets motion to VRM `J_Bip_*` body bones while ignoring `J_Sec_*` secondary hair, skirt, sleeve, and accessory bones.  
  支持将动作绑定到 VRM 的 `J_Bip_*` 躯体骨骼，并自动忽略 `J_Sec_*` 头发、裙摆、袖子、装饰等二级骨骼。

- **VRM leg and knee compensation controls**  
  Includes VRM thigh local-axis correction and independent left/right knee compensation to reduce seam twisting on compatible VRM models.  
  提供 VRM 大腿本地轴修正与左右膝盖独立补偿，用于减少部分 VRM 模型膝盖衔接处扭曲。

- **Bind to selected armature**  
  Retarget BVH motion to an existing selected Mixamo-compatible or VRM armature in the scene.  
  支持将 BVH 动作绑定到场景中已选中的 Mixamo 兼容骨架或 VRM 骨架。

- **Bind to character template**  
  Imports a built-in or custom character file and retargets BVH motion to the imported character.  
  支持导入内置或自定义人物模板，并将 BVH 动作直接绑定到该人物。

- **Built-in character template variants**  
  Includes multiple Mixamo-compatible template material variants: Default, White, Pink, Purple, Black, and Green.  
  内置多个 Mixamo 兼容人物模板颜色变体：默认、白色、粉色、紫色、黑色、绿色。

- **JSON-based source mapping**  
  Uses built-in or custom JSON mapping files to adapt BVH source bone names to the internal Mixamo-style intermediate rig.  
  使用内置或自定义 JSON 映射文件，将不同 BVH 来源骨骼名适配到内部 Mixamo 中间骨架。

- **Automatic BVH frame-rate matching**  
  Reads BVH `Frame Time` and optionally synchronizes the Blender scene FPS.  
  自动读取 BVH `Frame Time`，并可同步 Blender 场景帧率。

- **Integrated FBX export presets**  
  Provides Mixamo FBX, UE5 FBX, and Auto export presets directly inside the add-on panel.  
  插件内置 Mixamo FBX、UE5 FBX 与 Auto 自动导出预设，避免反复手动配置 Blender FBX 导出参数。

- **Optional curve simplification**  
  Can simplify redundant F-curves after baking for lighter animation data.  
  可在烘焙后简化冗余动画曲线，减小动画数据量。

---

## Requirements | 环境要求

- Blender 4.2 or later
- A BVH motion capture file
- For selected-armature binding: an existing compatible target armature in the scene
- For template binding: a built-in template or a custom `.fbx`, `.vrm`, `.glb`, or `.gltf` character file
- For VRM workflows: a VRM importer add-on may be required to import VRM files into Blender before binding

---

## Installation | 安装方法

1. Download the ZIP package from [GitHub Releases](https://github.com/BacteriaJun/BVH-Motion-Retargeter/releases/latest).
2. Open Blender.
3. Go to **Edit → Preferences → Add-ons** or **Extensions**.
4. Choose **Install...** or **Install from Disk**.
5. Select the ZIP package, for example:

   ```text
   bvh_motion_retargeter_v3.2.0_release.zip
   ```

6. Enable **BVH Motion Retargeter**.
7. Open the 3D Viewport.
8. Press `N` to open the sidebar.
9. Find the **BVH Retarget** tab.

安装后，插件面板位置为：

```text
3D Viewport → N Sidebar → BVH Retarget
```

---

## Panel Layout | 面板结构

The add-on panel is organized into six workflow sections:

插件面板按实际工作流分为六个区域：

```text
1. Source Motion
2. Source Mapping
3. Target Rig Profile
4. Binding Mode
5. Retarget Settings
6. FBX Export
```

### 1. Source Motion

Select the source BVH file and optionally match the Blender scene frame rate to the BVH frame time.

选择 BVH 源文件，并可选择是否自动匹配 BVH 帧率。

### 2. Source Mapping

Choose the built-in default mapping or a custom JSON mapping file.

选择内置默认映射或自定义 JSON 骨骼映射文件。

### 3. Target Rig Profile

Choose the final target rig profile:

选择最终目标骨架配置：

```text
Mixamo Standard
Unreal Engine 5 Humanoid
VRM Humanoid Body
```

### 4. Binding Mode

Choose how the target rig is created or selected:

选择目标骨架的创建或绑定方式：

```text
Create Target Armature
Bind to Selected Armature
Bind to Character Template
```

### 5. Retarget Settings

Configure the retargeting solver, root motion handling, and optional F-curve simplification.

配置重定向求解方式、Root Motion 处理和可选曲线简化。

### 6. FBX Export

Choose Mixamo, UE5, or Auto FBX export preset, set the output path, and export directly from the add-on.

选择 Mixamo、UE5 或 Auto 自动 FBX 导出预设，设置输出路径，并直接从插件导出。

---

## Target Rig Profiles | 目标骨架配置

### Mixamo Standard

The Mixamo profile uses standard `mixamorig:*` bone names. It is suitable for Mixamo-style characters and general humanoid animation workflows.

Mixamo 配置使用标准 `mixamorig:*` 骨骼命名，适合 Mixamo 风格人物和通用人形动画工作流。

Example target bones:

```text
mixamorig:Hips
mixamorig:Spine
mixamorig:Spine1
mixamorig:Spine2
mixamorig:Neck
mixamorig:Head
mixamorig:LeftArm
mixamorig:LeftForeArm
mixamorig:LeftHand
mixamorig:LeftUpLeg
mixamorig:LeftLeg
mixamorig:LeftFoot
```

### Unreal Engine 5 Humanoid

The UE5 profile converts the output to a UE-style humanoid hierarchy. It is designed as a UE-friendly skeleton profile, especially useful before importing into Unreal Engine or using UE5 IK Retargeter workflows.

UE5 配置会将输出转换为 UE 风格人形骨架，适合导入 Unreal Engine，或作为 UE5 IK Retargeter 工作流的中间骨架。

Example target bones:

```text
root
pelvis
spine_01
spine_02
spine_03
neck_01
head
clavicle_l
upperarm_l
lowerarm_l
hand_l
thigh_l
calf_l
foot_l
ball_l
```

Optional helper bones include Manny-style IK and lightweight twist helper bones. These are generated as non-deforming helper bones by default.

可选辅助骨骼包括 Manny 风格 IK 骨骼和轻量 twist 辅助骨骼，默认作为非变形骨骼生成。

### VRM Humanoid Body

The VRM profile targets VRM humanoid body bones using `J_Bip_*` naming. It intentionally ignores secondary physics and accessory bones such as `J_Sec_*` hair, skirt, sleeve, and decoration bones.

VRM 配置面向 `J_Bip_*` 命名的人形躯体骨骼，刻意忽略 `J_Sec_*` 头发、裙摆、袖子、装饰等二级骨骼。

Example target bones:

```text
J_Bip_C_Hips
J_Bip_C_Spine
J_Bip_C_Chest
J_Bip_C_UpperChest
J_Bip_C_Neck
J_Bip_C_Head
J_Bip_L_UpperArm
J_Bip_L_LowerArm
J_Bip_L_Hand
J_Bip_L_UpperLeg
J_Bip_L_LowerLeg
J_Bip_L_Foot
```

VRM leg-axis correction and independent knee compensation are provided for models whose thigh or knee seams twist after retargeting.

对于重定向后大腿或膝盖衔接处出现扭曲的 VRM 模型，插件提供腿部轴向修正与左右膝盖独立补偿参数。

---

## Binding Workflows | 绑定工作流

### Workflow 1: Create Target Armature | 创建目标骨架

Use this mode when you only need an animated target-format armature without binding to an existing character mesh.

适合只需要生成带动画的目标格式骨架，而不绑定到现有人物模型的情况。

1. Select a BVH file.
2. Choose a source mapping.
3. Choose a target rig profile.
4. Set **Binding Mode** to **Create Target Armature**.
5. Click **Create Target Armature**.
6. The add-on imports the BVH, maps the bones, creates the target armature, and bakes the animation.

### Workflow 2: Bind to Selected Armature | 绑定到已选骨架

Use this mode when a compatible character armature already exists in the scene.

适合场景中已经存在目标人物骨架的情况。

1. Import or prepare the target character in Blender.
2. Select the target armature.
3. Select the BVH file.
4. Choose the correct target rig profile.
5. Set **Binding Mode** to **Bind to Selected Armature**.
6. Click **Retarget to Selected Armature**.
7. The add-on transfers and bakes the BVH motion to the selected armature.

For VRM, first import the VRM character with a VRM importer, then select the VRM armature and use the **VRM Humanoid Body** profile.

对于 VRM，请先通过 VRM 导入插件将模型导入 Blender，再选中 VRM 骨架，并使用 **VRM Humanoid Body** 配置。

### Workflow 3: Bind to Character Template | 绑定到人物模板

Use this mode when you want the add-on to import a character template and apply the BVH motion automatically.

适合希望插件自动导入人物模板并直接生成带动画人物的情况。

1. Select a BVH file.
2. Choose a source mapping.
3. Choose a target rig profile.
4. Set **Binding Mode** to **Bind to Character Template**.
5. Choose a built-in template or a custom character file.
6. Click **Retarget to Character Template**.
7. The add-on imports the character, finds its armature, transfers the motion, and bakes the result.

Built-in character templates:

```text
Default Character
Default White
Default Pink
Default Purple
Default Black
Default Green
```

Custom template formats:

```text
.fbx
.vrm
.glb
.gltf
```

---

## FBX Export | FBX 导出

v3.2.0 includes integrated FBX export presets so that exported files can be generated directly from the add-on panel.

v3.2.0 内置 FBX 导出预设，可以直接在插件面板中导出，减少手动配置 Blender FBX 导出参数造成的错误。

### Export presets | 导出预设

```text
Auto
Mixamo FBX
UE5 FBX
```

### Auto

Automatically selects a suitable export preset from the selected target rig profile.

根据当前目标骨架配置自动选择合适的导出预设。

### Mixamo FBX

Use this when exporting Mixamo-style characters or general humanoid FBX files.

适合导出 Mixamo 风格人物或通用人形 FBX。

### UE5 FBX

Use this when exporting Unreal Engine 5-friendly humanoid skeletons.

适合导出 UE5 友好的人形骨架 FBX。

### Export options | 导出选项

- **FBX Output Path**: output `.fbx` file path
- **Auto Export After Convert**: automatically export after successful retargeting
- **Include Mesh**: include skinned meshes in the FBX export; disable for animation-only tests

---

## JSON Bone Mapping | JSON 骨骼映射

The source mapping system converts BVH source bone names into the internal Mixamo-style intermediate naming. This intermediate layer is then retargeted to Mixamo, UE5, or VRM target profiles.

源映射系统会先将 BVH 源骨骼名转换为内部 Mixamo 风格中间骨架，然后再映射到 Mixamo、UE5 或 VRM 目标骨架。

### Default mapping file | 默认映射文件

```text
presets/default_mixamo_mapping.json
```

### Custom mapping file | 自定义映射文件

Custom mappings should follow this structure:

自定义映射文件结构如下：

```json
{
  "name": "Custom BVH to Mixamo Mapping",
  "description": "Example source BVH bone names mapped to Mixamo intermediate bones.",
  "version": "1.0",
  "target": "mixamo",
  "mapping": {
    "Hips": "mixamorig:Hips",
    "Spine": "mixamorig:Spine",
    "Spine1": "mixamorig:Spine1",
    "Spine2": "mixamorig:Spine2",
    "Neck": "mixamorig:Neck",
    "Head": "mixamorig:Head",
    "LeftArm": "mixamorig:LeftArm",
    "LeftForeArm": "mixamorig:LeftForeArm",
    "LeftHand": "mixamorig:LeftHand",
    "RightArm": "mixamorig:RightArm",
    "RightForeArm": "mixamorig:RightForeArm",
    "RightHand": "mixamorig:RightHand",
    "LeftUpLeg": "mixamorig:LeftUpLeg",
    "LeftLeg": "mixamorig:LeftLeg",
    "LeftFoot": "mixamorig:LeftFoot",
    "RightUpLeg": "mixamorig:RightUpLeg",
    "RightLeg": "mixamorig:RightLeg",
    "RightFoot": "mixamorig:RightFoot"
  }
}
```

Notes:

- Source bone names must match the BVH file exactly.
- Target names in custom mapping files should use the Mixamo-style intermediate names.
- The target rig profile determines the final output naming.
- If no bones are matched, the operation is cancelled to avoid invalid processing.

---

## Package Structure | 插件结构

```text
bvh_to_mixamo/
  blender_manifest.toml
  __init__.py
  addon_info.py
  properties.py
  core/
    armature_utils.py
    bone_data.py
    bone_mapping.py
    bvh_parser.py
    export_profiles.py
    logger.py
    paths.py
    retarget_engine.py
    template_loader.py
    ue5_profile.py
    vrm_profile.py
  operators/
    convert.py
    export_fbx.py
    file_selectors.py
    import_bvh.py
    retarget.py
    template.py
  ui/
    panel.py
  presets/
    default_mixamo_mapping.json
    custom_mapping_example.json
    ue5_basic_mapping.json
    vrm_body_mapping.json
  templates/
    mixamo_default_character.fbx
    mixamo_default_white.fbx
    mixamo_default_pink.fbx
    mixamo_default_purple.fbx
    mixamo_default_black.fbx
    mixamo_default_green.fbx
docs/
  user-guide.md
scripts/
  build_release.py
  fetch_templates.py
tests/
  test_project.py
.github/workflows/
  ci.yml
```

### Architecture | 架构说明

```text
UI layer          → panel display and user controls
Operator layer    → Blender button actions and file selectors
Core layer        → BVH parsing, mapping, retargeting, export profiles
Resources layer   → installable presets and character templates
Project tooling   → top-level docs, tests, release builder, and CI
```

Large FBX templates are fetched from the immutable v3.2.0 release asset and verified with SHA-256 by `python scripts/fetch_templates.py`. Release ZIP files are then generated with `python scripts/build_release.py` and published as GitHub Release assets rather than committed to `main`.

---

## Technical Notes | 技术说明

### Retargeting solver

The current release uses a stable constraint-bake retargeting solver. It intentionally avoids experimental pose-delta retargeting in the public workflow because constraint baking has proven more predictable across Mixamo-style, UE-style, and VRM body targets.

当前版本使用稳定的约束烘焙重定向流程。公开版本中不暴露实验性的 Pose Delta 重定向，因为约束烘焙在 Mixamo、UE 风格和 VRM 躯体目标上更稳定、更可控。

### Root motion handling

Available root motion modes:

```text
Keep Source Motion
In-place Animation
Scale by Leg Length
```

UE5 profile also includes:

```text
No Root Motion
Root Bone Motion
Pelvis Only
```

### VRM body-only policy

VRM secondary bones are intentionally ignored:

```text
J_Sec_Hair*
J_Sec_Skirt*
J_Sec_Sleeve*
J_Sec_*_end
```

This avoids driving spring-bone, hair, skirt, sleeve, and accessory structures as if they were body bones.

---

## Known Limitations | 已知限制

- This is a lightweight production workflow, not a full professional IK retargeting solver.
- BVH files with unusual rest poses, bone rolls, or coordinate systems may require custom mapping or manual adjustment.
- UE5 output is UE-friendly humanoid output, not a guaranteed one-to-one replacement for Epic Manny/Quinn skeleton assets.
- VRM models vary significantly; some models may need knee compensation or manual cleanup.
- Long skirts, hair, sleeves, and accessories controlled by VRM secondary bones are not physically simulated by this add-on.
- Foot locking, contact solving, loop correction, and advanced IK cleanup are not included in this release.

---

## Troubleshooting | 常见问题

### The add-on is installed but does not appear in the sidebar.

Make sure you installed the ZIP as a Blender add-on or extension, enabled **BVH Motion Retargeter**, then opened the 3D Viewport sidebar with `N`. The tab name is **BVH Retarget**.

### The conversion reports zero matched bones.

The BVH source bone names do not match the selected mapping file. Use a custom JSON mapping file whose source names exactly match the BVH file.

### The animation speed is wrong.

Enable **Match BVH Frame Rate** so the add-on reads the BVH `Frame Time` and applies the corresponding FPS to the Blender scene.

### The selected character does not move correctly.

Check whether the selected target armature matches the chosen target profile. A Mixamo rig should use `mixamorig:*` bones; a VRM body rig should use `J_Bip_*` body bones.

### VRM knees twist after binding.

Enable **VRM Leg Axis Correction** and adjust **Left Knee Compensation** or **Right Knee Compensation**. Change only the side that shows visible twisting.

### UE5 import works, but it does not match Manny/Quinn perfectly.

The UE5 profile is a UE-friendly humanoid skeleton profile. For Manny/Quinn workflows, import the output as a compatible source skeleton and use UE5 IK Rig / IK Retargeter for final retargeting.

### The exported FBX contains no mesh.

Enable **Include Mesh** before export. Disable it only when you intentionally need animation-only FBX output.

---

## Version History | 版本历史

### v1.0

- Initial BVH to Mixamo skeleton conversion.
- 初步实现 BVH → Mixamo 骨骼转换。

### v2.0

- Improved scale handling and bone size conversion.
- 优化骨骼比例与尺寸处理。

### v2.1

- Improved user interface layout.
- 优化插件界面。

### v2.2

- Fixed hip joint connection issues.
- 修复胯部连接问题。

### v2.3

- Added automatic BVH frame-rate detection.
- 新增 BVH 帧率自动识别。

### v2.4

- Added binding to existing Mixamo armatures.
- Added constraint-based animation transfer and NLA baking.
- 新增绑定到已有 Mixamo 骨架、约束转移和 NLA 烘焙。

### v3.0

- Added JSON-based source mapping.
- Added custom mapping support and mapping diagnostics.
- 新增 JSON 映射、自定义映射与映射诊断。

### v3.1

- Added built-in Mixamo character template binding.
- Added custom FBX template support.
- Added template registry structure.
- 新增内置 Mixamo 人物模板绑定、自定义 FBX 模板和模板注册结构。

### v3.2.0

- Renamed the add-on to **BVH Motion Retargeter** for release.
- Reorganized the add-on into a modular architecture.
- Added target rig profiles: Mixamo Standard, Unreal Engine 5 Humanoid, and VRM Humanoid Body.
- Added integrated Mixamo FBX and UE5 FBX export presets.
- Added built-in Mixamo-compatible character material variants.
- Added VRM body-only mapping and knee compensation controls.
- Removed personal test files from the release package.
- 将插件正式命名为 **BVH Motion Retargeter**。
- 重构为模块化架构。
- 新增 Mixamo、UE5 Humanoid、VRM Body 三类目标骨架配置。
- 新增 Mixamo FBX 与 UE5 FBX 内置导出预设。
- 新增多个内置人物模板颜色变体。
- 新增 VRM 躯体映射与膝盖补偿控制。
- 移除个人测试文件，整理为发布版本。

---

## Author | 作者

Junius Tang / BacteriaJun

GitHub: [BacteriaJun/BVH-Motion-Retargeter](https://github.com/BacteriaJun/BVH-Motion-Retargeter)

---

## License | 许可证

[MIT](LICENSE), matching `bvh_to_mixamo/blender_manifest.toml`.
