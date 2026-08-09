import json
import os

from .bone_data import CRITICAL_BONES, DEFAULT_BONE_MAPPING, OPTIONAL_BONE_KEYWORDS, SECONDARY_BONES
from .logger import log_info, log_warning
from .paths import get_default_mapping_json_path

MAPPING_PRESET_DEFAULT = 'DEFAULT_JSON'
MAPPING_PRESET_CUSTOM = 'CUSTOM_JSON'


def get_default_mapping():
    return DEFAULT_BONE_MAPPING.copy()


def validate_mapping_dict(mapping):
    if not isinstance(mapping, dict):
        raise ValueError("mapping字段必须是JSON对象/dict")
    cleaned = {}
    for source_name, target_name in mapping.items():
        if not isinstance(source_name, str) or not isinstance(target_name, str):
            continue
        source_name = source_name.strip()
        target_name = target_name.strip()
        if source_name and target_name:
            cleaned[source_name] = target_name
    if not cleaned:
        raise ValueError("mapping字段为空，未找到有效骨骼映射")
    return cleaned


def load_mapping_json(filepath):
    if not filepath:
        raise FileNotFoundError("未提供JSON映射文件路径")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"JSON映射文件不存在: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    mapping = data.get("mapping", data) if isinstance(data, dict) else data
    return validate_mapping_dict(mapping)


def load_builtin_default_mapping():
    path = get_default_mapping_json_path()
    try:
        mapping = load_mapping_json(path)
        log_info(f"已加载内置JSON骨骼映射: {path}")
        return mapping
    except Exception as exc:
        log_warning(f"内置JSON映射加载失败，使用代码内置默认映射: {exc}")
        return get_default_mapping()


def get_active_bone_mapping(context):
    preset = getattr(context.scene, "bvh_mapping_preset", MAPPING_PRESET_DEFAULT)
    if preset == MAPPING_PRESET_CUSTOM:
        path = getattr(context.scene, "bvh_custom_mapping_path", "")
        mapping = load_mapping_json(path)
        log_info(f"已加载自定义JSON骨骼映射: {path}")
        return mapping
    return load_builtin_default_mapping()


def classify_bone(target_name):
    if target_name in CRITICAL_BONES:
        return "critical"
    if target_name in SECONDARY_BONES:
        return "secondary"
    if any(keyword in target_name for keyword in OPTIONAL_BONE_KEYWORDS):
        return "optional"
    return "secondary"


def validate_skeleton_mapping(source_armature, bone_mapping, target_armature=None):
    source_bones = set(b.name for b in source_armature.data.bones) if source_armature else set()
    target_bones = set(b.name for b in target_armature.data.bones) if target_armature else set()
    mapping_sources = set(bone_mapping.keys())
    mapping_targets = set(bone_mapping.values())

    matched_sources = source_bones.intersection(mapping_sources)
    missing_sources = mapping_sources - source_bones
    extra_sources = source_bones - mapping_sources

    missing_target_bones = mapping_targets - target_bones if target_armature else set()
    critical_targets = {v for v in bone_mapping.values() if classify_bone(v) == "critical"}
    secondary_targets = {v for v in bone_mapping.values() if classify_bone(v) == "secondary"}
    optional_targets = {v for v in bone_mapping.values() if classify_bone(v) == "optional"}

    matched_targets_from_sources = {bone_mapping[s] for s in matched_sources if s in bone_mapping}
    critical_matched = critical_targets.intersection(matched_targets_from_sources)
    secondary_matched = secondary_targets.intersection(matched_targets_from_sources)
    optional_matched = optional_targets.intersection(matched_targets_from_sources)

    score = 0
    score += int(60 * len(critical_matched) / max(1, len(critical_targets)))
    score += int(20 * len(secondary_matched) / max(1, len(secondary_targets)))
    score += int(10 * len(optional_matched) / max(1, len(optional_targets)))
    if source_armature and source_armature.animation_data and source_armature.animation_data.action:
        score += 5
    if not target_armature or not missing_target_bones:
        score += 5

    report = {
        "source_bone_count": len(source_bones),
        "mapping_count": len(mapping_sources),
        "matched_count": len(matched_sources),
        "missing_count": len(missing_sources),
        "extra_count": len(extra_sources),
        "missing_target_count": len(missing_target_bones),
        "matched": sorted(matched_sources),
        "missing": sorted(missing_sources),
        "extra": sorted(extra_sources),
        "missing_target_bones": sorted(missing_target_bones),
        "critical_total": len(critical_targets),
        "critical_matched": len(critical_matched),
        "secondary_total": len(secondary_targets),
        "secondary_matched": len(secondary_matched),
        "optional_total": len(optional_targets),
        "optional_matched": len(optional_matched),
        "score": min(score, 100),
        "can_continue": len(critical_matched) >= max(1, int(len(critical_targets) * 0.65)),
    }

    log_info("===== 骨骼映射质量检查 =====")
    log_info(f"源骨骼数量: {report['source_bone_count']} | 映射数量: {report['mapping_count']} | 成功匹配: {report['matched_count']}")
    log_info(f"关键骨骼: {report['critical_matched']}/{report['critical_total']} | 次级骨骼: {report['secondary_matched']}/{report['secondary_total']} | 可选骨骼: {report['optional_matched']}/{report['optional_total']}")
    log_info(f"Retarget Compatibility Score: {report['score']}/100")
    if report["missing"]:
        log_warning("映射表中存在但BVH缺失的骨骼(前20个): " + ", ".join(report["missing"][:20]))
    if report["missing_target_bones"]:
        log_warning("目标骨架缺失的Mixamo骨骼(前20个): " + ", ".join(report["missing_target_bones"][:20]))
    return report
