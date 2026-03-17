---

# BVH to Mixamo Converter

A Blender addon for converting BVH motion capture data into a Mixamo-standard rig, with support for binding animation directly to an existing Mixamo armature.
一个基于 Blender 的插件，用于将 BVH 动捕数据转换为 Mixamo 标准骨骼，并支持将动画直接绑定到现有 Mixamo 骨骼。

---

## 📌 项目简介 | Overview

**BVH to Mixamo Converter** 是一个面向实际动画流程的 Blender 工具插件，用于解决 BVH 动捕数据与 Mixamo 骨骼不兼容的问题。
**BVH to Mixamo Converter** is a Blender addon designed for real animation workflows, solving incompatibility issues between BVH motion capture data and Mixamo rigs.

项目从最初的骨骼层级转换功能出发，逐步演进，解决了骨骼比例、层级结构、UI体验、帧率同步等问题
Starting from basic skeleton hierarchy conversion, the project evolved through multiple versions, addressing scale mapping, hierarchy structure, UI usability, and framerate synchronization.

目前已经从“可用脚本”发展为一个具备实际工作流意义的动画工具。
It has evolved from a simple script into a practical animation pipeline tool.

---

## ✨ 核心特性 | Key Features

* 一键 BVH → Mixamo 骨骼转换
  One-click BVH to Mixamo skeleton conversion

* 支持绑定到现有 Mixamo 骨骼（不破坏原模型）
  Bind animation to existing Mixamo rigs without breaking mesh binding

* 自动读取 BVH 帧率并同步 Blender 场景
  Automatically detect BVH framerate and sync Blender scene FPS

* 自动修复骨骼层级结构
  Reconstruct Mixamo-style bone hierarchy

* 动画数据路径自动重映射（F-Curve 修复）
  Automatic animation data path remapping (F-Curve fix)

* 基于约束 + NLA Bake 的动画迁移系统
  Constraint-driven animation transfer with NLA baking

---

## 🔄 工作流程 | Workflow

### 模式一：创建新骨骼 | Create New Armature

1. 选择 BVH 文件
   Select BVH file
2. 勾选帧率匹配（可选）
   Enable FPS matching (optional)
3. 点击转换
   Run conversion
4. 自动生成 Mixamo 骨骼与动画
   Generate Mixamo rig with animation

---

### 模式二：绑定到现有骨骼 | Bind to Existing Rig

1. 选中场景中的 Mixamo 骨骼
   Select a Mixamo armature in the scene
2. 选择 BVH 文件
   Select BVH file
3. 点击绑定
   Run binding
4. 自动完成：
   Automatically performs:

   * BVH 导入
     BVH import
   * 骨骼转换
     Skeleton conversion
   * 比例匹配
     Scale matching
   * 动画转移
     Animation transfer
   * 动画烘焙
     Animation baking
   * 删除临时骨骼
     Remove temporary armature

---

## 🧠 技术实现细节 | Technical Details

本插件的核心并非简单“改名”，而是一个完整的动画处理流程：
This addon is not just a renaming script, but a complete animation processing pipeline:

### 1. BVH 帧率解析 | BVH Framerate Parsing

* 通过解析 `Frame Time` 自动计算 FPS
* Automatically parses `Frame Time` to compute FPS
* 并同步 Blender 场景帧率
* Synchronizes Blender scene framerate

---

### 2. 骨骼映射系统 | Bone Mapping System

* 使用预定义字典进行 BVH → Mixamo 命名映射
* Uses a predefined mapping dictionary
* 保证动画数据路径可重定向
* Ensures animation data path consistency

---

### 3. 动画数据修复 | Animation Data Remapping

* 自动修改 F-Curve 的 data_path
* Updates F-Curve data paths
* 避免骨骼重命名后动画丢失
* Prevents animation loss after renaming

---

### 4. 骨骼层级重建 | Hierarchy Reconstruction

* 根据 Mixamo 标准重建父子关系
* Rebuilds parent-child relationships
* 同时保留原始骨骼空间位置
* Preserves original bone transforms

---

### 5. 动画迁移（核心）| Animation Retargeting (Core)

通过以下方式实现动画转移：
Animation transfer is implemented via:

* Copy Location（根骨骼）
* Copy Rotation（所有骨骼）
* 区分 LOCAL / POSE 空间
* Differentiates LOCAL vs POSE space

---

### 6. NLA 烘焙 | NLA Baking

* 使用 `bpy.ops.nla.bake`
* 将约束动画转为关键帧
* Converts constraint-driven motion into keyframes

---

### 7. 骨骼比例适配 | Scale Matching

* 基于 Hips 骨骼长度计算比例
* Uses Hips bone length as reference
* 自动缩放源骨骼以匹配目标骨骼
* Automatically scales source armature

---

👉 本质上，这是一个简化版 Retarget Pipeline
👉 Essentially, this is a lightweight retargeting pipeline

---

## 📜 版本历史 | Version History

### v1.0

实现 BVH → Mixamo 骨骼层级基础转换
Basic BVH to Mixamo hierarchy conversion

### v2.0

修复骨骼映射中的比例/大小问题
Fixed scale and size issues in bone mapping

### v2.1

优化 UI 界面显示
Improved UI layout and usability

### v2.2

修复胯部骨骼粘连问题
Fixed hip joint connection issue

### v2.3

实现 BVH 帧率自动识别与场景同步（可选）
Added automatic BVH framerate detection and scene synchronization

### v2.4

新增绑定到现有 Mixamo 骨骼功能（动画迁移 + 烘焙）
Added binding to existing Mixamo rigs (animation transfer + baking)

---

## ⚙️ 环境要求 | Requirements

* Blender 4.0+
* BVH 动捕文件
  BVH motion capture files
* Mixamo 标准骨骼（绑定模式）
  Mixamo-style rig (for binding mode)

---

## 📦 安装方法 | Installation

1. 下载 `.py` 插件
   Download the `.py` file
2. Blender → Preferences → Add-ons → Install
3. 启用插件
   Enable addon
4. 在侧边栏使用
   Access in Sidebar

---

## ⚠️ 注意事项 | Notes

* 仅适用于人形骨骼
  Designed for humanoid rigs only
* 不同 BVH 可能存在坐标差异
  BVH sources may have orientation differences
* 复杂骨架可能需要微调
  Complex rigs may require manual adjustment

---

## 👤 Author

**Junius Tang**

---

## 📌 License

MIT License (recommended)

---

