# BVH Motion Retargeter

> 在 Blender 中将 BVH 动捕数据重定向到 Mixamo、Unreal Engine 5 与 VRM 人形骨架。

[![Release](https://img.shields.io/github/v/release/BacteriaJun/BVH-Motion-Retargeter)](https://github.com/BacteriaJun/BVH-Motion-Retargeter/releases/latest)
[![CI](https://github.com/BacteriaJun/BVH-Motion-Retargeter/actions/workflows/ci.yml/badge.svg)](https://github.com/BacteriaJun/BVH-Motion-Retargeter/actions/workflows/ci.yml)
[![Blender](https://img.shields.io/badge/Blender-4.2%2B-orange)](https://www.blender.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[English](README.md) | **简体中文**

**BVH Motion Retargeter** 是一个面向 Blender 的 BVH 动作重定向插件，用于将不同来源的 BVH 动捕数据转换并绑定到常见的人形骨骼体系。

插件提供从骨骼映射、动作重定向、动画烘焙，到曲线清理和 FBX 导出的完整工作流。

目前支持：

* **Mixamo**
* **Unreal Engine 5**
* **VRM 人形角色**

---

## 演示

<!--
录制演示 GIF 后，将文件保存为：

docs/assets/demo.gif

然后取消下面代码的注释：

<p align="center">
  <img src="docs/assets/demo.gif" width="900" alt="BVH Motion Retargeter 演示">
</p>

<p align="center">
  BVH → 重定向 → 烘焙 → 导出
</p>
-->

```text
BVH 动作
   │
   ▼
源骨骼映射
   │
   ▼
目标骨架配置
┌─────┼─────┐
▼     ▼     ▼
Mixamo UE5  VRM
   │
   ▼
重定向与烘焙
   │
   ▼
Blender 动画 / FBX
```

---

## 为什么需要 BVH Motion Retargeter？

不同动捕系统生成的 BVH 文件，往往存在不同的：

* 骨骼名称
* 骨骼层级
* 坐标轴定义
* 帧率
* Root Motion 处理方式

如果手工适配，通常需要反复进行：

```text
重命名骨骼
→ 建立约束
→ 调整骨架
→ 烘焙动画
→ 清理曲线
→ 配置导出参数
```

BVH Motion Retargeter 将这些步骤整合为一个统一流程：

**导入 → 映射 → 重定向 → 烘焙 → 导出**

---

## 核心功能

### Constraint Bake 动作重定向

插件通过 Blender 的 Copy Location / Copy Rotation 约束与 NLA Bake，将 BVH 动作传递到目标骨架，并最终生成真实动画关键帧。

这意味着重定向后的动画不依赖运行时约束，可以继续进行：

* 手工调整
* 曲线编辑
* 动画混合
* FBX 导出
* 游戏引擎导入

---

### 多种目标骨架

内置支持：

* Mixamo Standard
* Unreal Engine 5 Humanoid
* VRM Humanoid Body

可根据最终使用环境选择对应目标骨架。

---

### 灵活的绑定方式

可以将 BVH 动作绑定到：

* 自动创建的目标骨架
* Blender 场景中已经存在的兼容骨架
* 插件内置人物模板
* 自定义 FBX / VRM / GLB / GLTF 角色

---

### JSON 骨骼映射

插件使用 JSON 文件描述 BVH 源骨骼与内部目标骨骼之间的映射关系。

这样可以适配不同动捕系统，而无需修改插件核心代码。

---

### FBX 导出工作流

插件内置：

* Mixamo FBX 导出配置
* Unreal Engine 5 FBX 导出配置
* 根据目标骨架自动选择的 Auto 模式

可以减少 Blender FBX 导出过程中重复配置参数的问题。

---

### 动画清理工具

包括：

* BVH 帧率自动匹配
* Root Motion 处理
* 可选 F-Curve 简化
* VRM 大腿本地轴修正
* 左右膝盖独立补偿

这些功能用于处理动作重定向后常见的动画质量问题。

---

## 支持的目标骨架

| 目标                  | 骨骼体系                         | 常见用途                    |
| ------------------- | ---------------------------- | ----------------------- |
| **Mixamo**          | `mixamorig:*`                | Mixamo 角色、通用人形动画        |
| **Unreal Engine 5** | `root`、`pelvis`、`spine_01` 等 | UE5 人形骨架与 IK Retargeter |
| **VRM**             | `J_Bip_*`                    | VRM 虚拟角色                |

VRM 模式主要针对标准人形躯体骨骼。

插件会有意忽略：

```text
J_Sec_*
```

等二级物理骨骼，例如：

* 头发
* 裙摆
* 袖子
* 装饰物

避免这些辅助骨骼参与人体动作重定向。

---

## 快速开始

### 环境要求

* Blender **4.2 或更高版本**
* 一个 `.bvh` 动捕文件

如果需要处理 VRM 角色，可能需要先安装兼容的 Blender VRM 导入插件。

---

### 安装

1. 前往 **[GitHub Releases](https://github.com/BacteriaJun/BVH-Motion-Retargeter/releases/latest)** 下载最新 ZIP。
2. 打开 Blender。
3. 进入 **Edit → Preferences → Add-ons / Extensions**。
4. 选择 **Install from Disk**。
5. 选择下载的 ZIP。
6. 启用 **BVH Motion Retargeter**。

插件面板位于：

```text
3D Viewport
→ N Sidebar
→ BVH Retarget
```

---

## 基本工作流

### 1. 选择 BVH 动作

选择需要处理的 `.bvh` 文件。

插件可以读取 BVH 的 Frame Time，并根据需要自动同步 Blender Scene FPS。

---

### 2. 选择源骨骼映射

可以使用：

* 内置默认映射
* 自定义 JSON 映射

用于适配不同来源的 BVH 骨骼命名。

---

### 3. 选择目标骨架

可选：

```text
Mixamo Standard
Unreal Engine 5 Humanoid
VRM Humanoid Body
```

---

### 4. 选择绑定方式

可选：

```text
Create Target Armature
Bind to Selected Armature
Bind to Character Template
```

分别对应：

* 创建新的目标骨架
* 绑定场景中已选择的角色骨架
* 导入并绑定人物模板

---

### 5. 重定向与烘焙

插件会：

```text
导入 BVH
→ 建立骨骼对应关系
→ 创建约束
→ 传递动作
→ Bake 动画
→ 清除临时约束
```

最终动画会成为目标骨架上的真实关键帧。

---

### 6. 导出

可以直接选择：

```text
Mixamo FBX
UE5 FBX
Auto
```

完成最终 FBX 输出。

---

## 人物模板

插件包含多个 Mixamo 兼容人物模板：

* Default
* White
* Pink
* Purple
* Black
* Green

为了避免将大型 FBX 文件直接长期存储在源码历史中，模板文件通过发布资产进行管理。

开发或构建 Release 时可以通过：

```bash
python scripts/fetch_templates.py
```

下载模板，并使用 SHA-256 校验文件完整性。

---

## 自定义骨骼映射

骨骼映射通过 JSON 文件定义。

示例：

```json
{
  "Hips": "mixamorig:Hips",
  "Spine": "mixamorig:Spine",
  "LeftArm": "mixamorig:LeftArm",
  "RightArm": "mixamorig:RightArm"
}
```

映射文件位于：

```text
bvh_to_mixamo/presets/
```

如果你的 BVH 来源使用不同骨骼名称，可以创建新的映射文件，而不需要修改重定向逻辑。

---

## 项目结构

```text
BVH-Motion-Retargeter/
├── bvh_to_mixamo/
│   ├── core/
│   ├── operators/
│   ├── presets/
│   ├── templates/
│   └── ui/
│
├── docs/
├── scripts/
├── tests/
│
├── .github/workflows/
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── README_zh-CN.md
└── pyproject.toml
```

项目将：

* Blender 运行时代码
* 文档
* 测试
* Release 构建工具
* CI

分别组织，避免插件安装包与开发工具混在一起。

---

## 开发

克隆仓库：

```bash
git clone https://github.com/BacteriaJun/BVH-Motion-Retargeter.git
cd BVH-Motion-Retargeter
```

安装 Ruff：

```bash
python -m pip install ruff
```

下载并校验人物模板：

```bash
python scripts/fetch_templates.py
```

执行代码检查：

```bash
ruff check .
```

执行 Python 编译检查：

```bash
python -m compileall -q bvh_to_mixamo scripts tests
```

运行单元测试：

```bash
python -m unittest discover -s tests -v
```

构建 Blender 安装包：

```bash
python scripts/build_release.py
```

生成的 ZIP 位于：

```text
dist/
```

---

## 持续集成

仓库通过 GitHub Actions 对 Push 和 Pull Request 自动进行验证。

当前 CI 包括：

* Ruff 静态检查
* Python Compile 检查
* 人物模板 SHA-256 校验
* Repository Unit Tests
* Release ZIP 构建

这样可以确保源码结构、资源文件和最终插件安装包保持一致。

---

## 文档

更多内容可以在 [`docs/`](docs/) 中维护。

现有文档：

* [用户指南](docs/user-guide.md)
* [版本变更记录](CHANGELOG.md)
* [贡献指南](CONTRIBUTING.md)

后续推荐继续拆分：

```text
docs/
├── user-guide.md
├── target-rigs.md
├── source-mapping.md
├── architecture.md
├── troubleshooting.md
└── assets/
```

其中分别维护：

* Mixamo / UE5 / VRM 骨骼细节
* 自定义映射方法
* 插件架构
* 常见错误
* Demo GIF 与截图

---

## 贡献

欢迎提交：

* Bug Report
* Feature Request
* Pull Request
* 新 BVH 骨骼映射
* 新目标骨架支持
* 文档改进

提交代码前请阅读：

[CONTRIBUTING.md](CONTRIBUTING.md)

涉及 Blender 行为变化时，请注明用于测试的 Blender 版本。

---

## Release

稳定版本通过 GitHub Releases 发布：

**[下载最新版本](https://github.com/BacteriaJun/BVH-Motion-Retargeter/releases/latest)**

生成的 Release ZIP 不直接提交到 `main` 分支。

---

## 作者

**Junius Tang / BacteriaJun**

GitHub: [@BacteriaJun](https://github.com/BacteriaJun)

---

## License

本项目采用 [MIT License](LICENSE)。
