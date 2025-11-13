#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比对JSON文件与Ground Truth表格的字段
"""
import json
import re
from typing import Dict, List, Set, Tuple

# 文件路径
MARKDOWN_FILE = "match /比對結果.md"
JSON_FILES = {
    "1756771600": "match /1756771600_out.json",
    "1755859287": "match /1755859287_out.json",
    "1754668881": "match /1754668881_out.json",
    "acer": "match /Acer线上数据包内部数据结构.json"
}

# 字段名到JSON路径的映射
FIELD_TO_JSON_PATH = {
    # 顶层结构
    "顶层结构": {
        "activitys": ["activitys"],
        "fulldaySteps": ["fulldaySteps"],
        "sleeps": ["sleeps"],
        "sleepTypes": ["sleepTypes"],
        "fulldayHeartRate": ["fulldayHeartRate"],
        "fulldayHRV": ["fulldayHRV"],
        "singleHeartRate": ["singleHeartRate"],
        "singleHRV": ["singleHRV"],
        "singleBloodOxygen": ["singleBloodOxygen"],
        "singleStress": ["singleStress"],
        "fulldayTemperature": ["fulldayTemperature"],
        "trainings": ["trainings"]
    },
    # Activity
    "Activity": {
        "date": ["activitys", 0, "date"],
        "step": ["activitys", 0, "step"],
        "calorie": ["activitys", 0, "calorie"],
        "distance": ["activitys", 0, "distance"],
        "duration": ["activitys", 0, "duration"],
        "goalStep": ["activitys", 0, "goalStep"],
        "goalCalorie": ["activitys", 0, "goalCalorie"],
        "goalDistance": ["activitys", 0, "goalDistance"],
        "goalDuration": ["activitys", 0, "goalDuration"]
    },
    # FullDaySteps
    "FullDaySteps": {
        "date": ["fulldaySteps", 0, "date"],
        "steps": ["fulldaySteps", 0, "steps"]
    },
    # Sleep
    "Sleep": {
        "date": ["gomoreSleeps", 0, "date"],
        "deep": ["gomoreSleeps", 0, "deep"],
        "light": ["gomoreSleeps", 0, "light"],
        "rem": ["gomoreSleeps", 0, "rem"],
        "detail": ["gomoreSleeps", 0, "detail"],
        "type": ["gomoreSleeps", 0, "type"],
        "startTime": ["gomoreSleeps", 0, "startTime"],
        "endTime": ["gomoreSleeps", 0, "endTime"]
    },
    # SleepDetail
    "SleepDetail": {
        "start": ["gomoreSleeps", 0, "detail", 0, "start"],
        "end": ["gomoreSleeps", 0, "detail", 0, "end"],
        "total": ["gomoreSleeps", 0, "detail", 0, "total"],
        "type": ["gomoreSleeps", 0, "detail", 0, "type"]
    },
    # SleepType
    "SleepType": {
        "date": ["sleepTypes", 0, "date"],
        "reliability": ["sleepTypes", 0, "reliability"],
        "bedtime": ["sleepTypes", 0, "bedtime"],
        "type": ["sleepTypes", 0, "type"],
        "state": ["sleepTypes", 0, "state"]
    },
    # FullDayHeartRate
    "FullDayHeartRate": {
        "date": ["fulldayHeartRate", 0, "date"],
        "hearts": ["fulldayHeartRate", 0, "hearts"]
    },
    # FullDayHRV
    "FullDayHRV": {
        "date": ["fulldayHRV", 0, "date"],
        "hrvs": ["fulldayHRV", 0, "hrvs"]
    },
    # SingleHeart
    "SingleHeart": {
        "date": ["singleHeartRate", 0, "date"],
        "heart": ["singleHeartRate", 0, "heart"]
    },
    # SingleHRV
    "SingleHRV": {
        "date": ["singleHRV", 0, "date"],
        "hrv": ["singleHRV", 0, "hrv"]
    },
    # SingleBloodOxygen
    "SingleBloodOxygen": {
        "date": ["singleBloodOxygen", 0, "date"],
        "bloodOxygen": ["singleBloodOxygen", 0, "bloodOxygen"]
    },
    # SingleStress
    "SingleStress": {
        "date": ["singleStress", 0, "date"],
        "stress": ["singleStress", 0, "stress"]
    },
    # FullDayTemperature
    "FullDayTemperature": {
        "date": ["fulldayTemperature", 0, "date"],
        "tempeartures": ["fulldayTemperature", 0, "tempeartures"]
    },
    # Training
    "Training": {
        "startTime": ["trainings", 0, "startTime"],
        "endTime": ["trainings", 0, "endTime"],
        "avalidTime": ["trainings", 0, "avalidTime"],
        "hrAvg": ["trainings", 0, "hrAvg"],
        "trainType": ["trainings", 0, "trainType"],
        "step": ["trainings", 0, "step"],
        "distance": ["trainings", 0, "distance"],
        "kcal": ["trainings", 0, "kcal"],
        "heartRate": ["trainings", 0, "heartRate"],
        "goalType": ["trainings", 0, "goalType"]
    }
}

def load_json(file_path: str) -> Dict:
    """加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_nested_field(data: Dict, path: List) -> Tuple[bool, any]:
    """
    根据路径获取嵌套字段
    返回: (字段是否存在, 字段值)
    """
    current = data
    for i, key in enumerate(path):
        if isinstance(current, dict):
            if key not in current:
                return False, None
            current = current[key]
        elif isinstance(current, list):
            if not current:
                return False, None
            # 对于数组，需要遍历检查是否有任何元素包含该路径
            # 如果是数组中的索引，检查该索引是否存在
            if isinstance(key, int):
                if len(current) <= key:
                    return False, None
                current = current[key]
            else:
                # 如果不是索引，说明路径有问题
                return False, None
        else:
            return False, None
    return True, current

def check_field_exists(data: Dict, section: str, field: str) -> bool:
    """检查字段是否存在于JSON数据中"""
    if section not in FIELD_TO_JSON_PATH:
        return False

    if field not in FIELD_TO_JSON_PATH[section]:
        return False

    path = FIELD_TO_JSON_PATH[section][field]

    # 对于嵌套在数组中的字段（如 SleepDetail），需要遍历数组检查
    # 路径格式如: ["gomoreSleeps", 0, "detail", 0, "start"]
    # 我们需要检查是否有任何数组元素包含该字段

    # 找到路径中的所有数组索引位置
    array_indices = []
    for i, key in enumerate(path):
        if isinstance(key, int):
            array_indices.append(i)

    if not array_indices:
        # 没有数组索引，直接检查
        exists, _ = get_nested_field(data, path)
        return exists
    else:
        # 有数组索引，需要遍历数组检查
        # 对于最外层的数组，遍历所有元素
        base_path = path[:array_indices[0]]
        exists, array_data = get_nested_field(data, base_path)

        if not exists or not isinstance(array_data, list):
            return False

        # 遍历数组中的每个元素
        for item_idx in range(len(array_data)):
            # 构建新的路径，替换第一个数组索引
            new_path = base_path + [item_idx] + path[array_indices[0]+1:]

            # 如果有第二层数组（如 detail）
            if len(array_indices) > 1:
                # 检查第二层数组
                second_base_path = new_path[:array_indices[1]]
                exists2, second_array = get_nested_field(data, second_base_path)

                if exists2 and isinstance(second_array, list) and len(second_array) > 0:
                    # 遍历第二层数组
                    for detail_idx in range(len(second_array)):
                        final_path = second_base_path + [detail_idx] + new_path[array_indices[1]+1:]
                        exists3, _ = get_nested_field(data, final_path)
                        if exists3:
                            return True
            else:
                # 只有一层数组
                exists2, _ = get_nested_field(data, new_path)
                if exists2:
                    return True

        return False

def get_all_top_level_fields(data: Dict) -> Set[str]:
    """获取JSON中所有顶层字段"""
    return set(data.keys())

def get_all_nested_fields(data: Dict, path: List[str]) -> Set[str]:
    """获取嵌套对象的所有字段"""
    exists, value = get_nested_field(data, path)
    if not exists or not isinstance(value, dict):
        return set()
    return set(value.keys())

def compare_fields():
    """比对所有JSON文件的字段"""
    # 加载JSON文件
    json_data = {}
    for key, path in JSON_FILES.items():
        json_data[key] = load_json(path)

    # 存储比对结果
    results = {}

    # 比对每个section
    for section, fields in FIELD_TO_JSON_PATH.items():
        results[section] = {
            "fields": {},
            "missing": {"1756771600": [], "1755859287": [], "1754668881": [], "acer": []},
            "extra": {"1756771600": [], "1755859287": [], "1754668881": [], "acer": []}
        }

        # 检查每个字段
        for field in fields:
            results[section]["fields"][field] = {}
            for json_key, data in json_data.items():
                exists = check_field_exists(data, section, field)
                results[section]["fields"][field][json_key] = "match" if exists else ""

                # 记录缺少的字段
                if not exists:
                    results[section]["missing"][json_key].append(field)

        # 查找多出来的字段
        for json_key, data in json_data.items():
            if section == "顶层结构":
                # 顶层字段
                json_fields = get_all_top_level_fields(data)
                ground_truth_fields = set(fields.keys())
                extra_fields = json_fields - ground_truth_fields - {"updateDate", "originalStartTime"}
                results[section]["extra"][json_key] = list(extra_fields)
            else:
                # 嵌套字段 - 需要根据路径查找
                # 获取该section对应的顶层路径
                if fields:
                    first_field = list(fields.keys())[0]
                    path = fields[first_field]
                    # 获取到对象级别的路径（不包括具体字段名）
                    obj_path = path[:-1]

                    json_fields = get_all_nested_fields(data, obj_path)
                    ground_truth_fields = set(fields.keys())
                    extra_fields = json_fields - ground_truth_fields - {"originalStartTime"}
                    results[section]["extra"][json_key] = list(extra_fields)

    return results

def generate_markdown_table(section: str, results: Dict) -> str:
    """生成Markdown表格"""
    lines = []

    # 主表格
    lines.append("| 字段名 | 类型 | 描述 | Hti 比對結果 (1756771600) | Hti 比對結果 (1755859287) | Hti 比對結果 (1754668881) | Acer线上数据包内部数据结构 |")
    lines.append("| --- | --- | --- | --- | --- | --- | --- |")

    for field, comparisons in results["fields"].items():
        # 保留原始的类型和描述（从原文件中读取）
        lines.append(f"| {field} |  |  | {comparisons.get('1756771600', '')} | {comparisons.get('1755859287', '')} | {comparisons.get('1754668881', '')} |  |")

    lines.append("")
    lines.append("缺少欄位")
    lines.append("")
    lines.append("| Hti 比對結果 (1756771600) | Hti 比對結果 (1755859287) | Hti 比對結果 (1754668881) | Acer线上数据包内部数据结构 |")
    lines.append("| --- | --- | --- | --- |")

    # 获取最多的缺少字段数量
    max_missing = max(
        len(results["missing"]["1756771600"]),
        len(results["missing"]["1755859287"]),
        len(results["missing"]["1754668881"])
    )

    if max_missing > 0:
        for i in range(max_missing):
            col1 = results["missing"]["1756771600"][i] if i < len(results["missing"]["1756771600"]) else ""
            col2 = results["missing"]["1755859287"][i] if i < len(results["missing"]["1755859287"]) else ""
            col3 = results["missing"]["1754668881"][i] if i < len(results["missing"]["1754668881"]) else ""
            lines.append(f"| {col1} | {col2} | {col3} |  |")
    else:
        lines.append("|  |  |  |  |")

    lines.append("")
    lines.append("多出來的欄位")
    lines.append("")
    lines.append("| Hti 比對結果 (1756771600) | Hti 比對結果 (1755859287) | Hti 比對結果 (1754668881) | Acer线上数据包内部数据结构 |")
    lines.append("| --- | --- | --- | --- |")

    # 获取最多的多余字段数量
    max_extra = max(
        len(results["extra"]["1756771600"]),
        len(results["extra"]["1755859287"]),
        len(results["extra"]["1754668881"])
    )

    if max_extra > 0:
        for i in range(max_extra):
            col1 = results["extra"]["1756771600"][i] if i < len(results["extra"]["1756771600"]) else ""
            col2 = results["extra"]["1755859287"][i] if i < len(results["extra"]["1755859287"]) else ""
            col3 = results["extra"]["1754668881"][i] if i < len(results["extra"]["1754668881"]) else ""
            lines.append(f"| {col1} | {col2} | {col3} |  |")
    else:
        lines.append("|  |  |  |  |")

    return "\n".join(lines)

def main():
    """主函数"""
    print("开始比对字段...")
    results = compare_fields()

    print("\n=== 比对结果 ===\n")
    for section, data in results.items():
        print(f"\n## {section}")
        print(generate_markdown_table(section, data))
        print()

    # 将结果保存为JSON以便后续处理
    with open("comparison_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n比对完成！结果已保存到 comparison_results.json")

if __name__ == "__main__":
    main()
