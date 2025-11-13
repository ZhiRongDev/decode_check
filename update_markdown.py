#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新比對結果.md文件，保留原有的类型和描述信息
"""
import json
import re
from typing import Dict, List, Tuple

# 文件路径
MARKDOWN_FILE = "match /比對結果.md"
COMPARISON_RESULTS_FILE = "comparison_results.json"

def read_markdown():
    """读取Markdown文件"""
    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def load_comparison_results():
    """加载比对结果"""
    with open(COMPARISON_RESULTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_field_table(lines: List[str], start_idx: int) -> Tuple[Dict, int]:
    """
    解析字段表格，提取字段名、类型、描述
    返回: (字段信息字典, 表格结束行号)
    """
    fields_info = {}
    idx = start_idx + 2  # 跳过表头和分隔线

    while idx < len(lines):
        line = lines[idx].strip()
        if not line or not line.startswith('|'):
            break

        # 解析表格行
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 4:  # | 字段名 | 类型 | 描述 | ...
            field_name = parts[1]
            field_type = parts[2]
            field_desc = parts[3]

            if field_name and field_name not in ['字段名', '---']:
                fields_info[field_name] = {
                    'type': field_type,
                    'description': field_desc
                }

        idx += 1

    return fields_info, idx

def update_section(section_name: str, content: str, comparison_data: Dict) -> str:
    """更新单个section的内容"""
    lines = content.split('\n')
    updated_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # 查找section标题
        if line.strip() == f"# {section_name}":
            updated_lines.append(line)
            i += 1

            # 跳过空行
            while i < len(lines) and not lines[i].strip():
                updated_lines.append(lines[i])
                i += 1

            # 解析原始表格以获取类型和描述
            if i < len(lines) and lines[i].startswith('|'):
                fields_info, table_end = parse_field_table(lines, i)

                # 生成更新后的主表格
                updated_lines.append("| 字段名 | 类型 | 描述 | Hti 比對結果 (1756771600) | Hti 比對結果 (1755859287) | Hti 比對結果 (1754668881) | Acer线上数据包内部数据结构 |")
                updated_lines.append("| --- | --- | --- | --- | --- | --- | --- |")

                for field_name, field_data in comparison_data['fields'].items():
                    field_type = fields_info.get(field_name, {}).get('type', '')
                    field_desc = fields_info.get(field_name, {}).get('description', '')
                    col1756 = field_data.get('1756771600', '')
                    col1755 = field_data.get('1755859287', '')
                    col1754 = field_data.get('1754668881', '')
                    col_acer = field_data.get('acer', '')

                    updated_lines.append(f"| {field_name} | {field_type} | {field_desc} | {col1756} | {col1755} | {col1754} | {col_acer} |")

                # 跳过原表格内容
                i = table_end

                # 跳过空行直到找到"缺少欄位"
                while i < len(lines) and not lines[i].strip().startswith("缺少欄位"):
                    if not lines[i].strip():
                        updated_lines.append(lines[i])
                    i += 1

                # 添加缺少字段表格
                if i < len(lines):
                    updated_lines.append("")
                    updated_lines.append("缺少欄位")
                    updated_lines.append("")
                    updated_lines.append("| Hti 比對結果 (1756771600) | Hti 比對結果 (1755859287) | Hti 比對結果 (1754668881) | Acer线上数据包内部数据结构 |")
                    updated_lines.append("| --- | --- | --- | --- |")

                    missing = comparison_data['missing']
                    max_missing = max(len(missing['1756771600']), len(missing['1755859287']), len(missing['1754668881']), len(missing['acer']), 1)

                    if any(missing.values()):
                        for idx in range(max_missing):
                            col1756 = missing['1756771600'][idx] if idx < len(missing['1756771600']) else ""
                            col1755 = missing['1755859287'][idx] if idx < len(missing['1755859287']) else ""
                            col1754 = missing['1754668881'][idx] if idx < len(missing['1754668881']) else ""
                            col_acer = missing['acer'][idx] if idx < len(missing['acer']) else ""
                            updated_lines.append(f"| {col1756} | {col1755} | {col1754} | {col_acer} |")
                    else:
                        updated_lines.append("|  |  |  |  |")

                    # 跳过原缺少字段表格
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith("多出來的欄位"):
                        if lines[i].strip().startswith("|"):
                            i += 1
                            continue
                        if not lines[i].strip():
                            i += 1
                            continue
                        i += 1

                    # 添加多出字段表格
                    if i < len(lines):
                        updated_lines.append("")
                        updated_lines.append("多出來的欄位")
                        updated_lines.append("")
                        updated_lines.append("| Hti 比對結果 (1756771600) | Hti 比對結果 (1755859287) | Hti 比對結果 (1754668881) | Acer线上数据包内部数据结构 |")
                        updated_lines.append("| --- | --- | --- | --- |")

                        extra = comparison_data['extra']
                        max_extra = max(len(extra['1756771600']), len(extra['1755859287']), len(extra['1754668881']), len(extra['acer']), 1)

                        if any(extra.values()):
                            for idx in range(max_extra):
                                col1756 = extra['1756771600'][idx] if idx < len(extra['1756771600']) else ""
                                col1755 = extra['1755859287'][idx] if idx < len(extra['1755859287']) else ""
                                col1754 = extra['1754668881'][idx] if idx < len(extra['1754668881']) else ""
                                col_acer = extra['acer'][idx] if idx < len(extra['acer']) else ""
                                updated_lines.append(f"| {col1756} | {col1755} | {col1754} | {col_acer} |")
                        else:
                            updated_lines.append("|  |  |  |  |")

                        # 跳过原多出字段表格
                        i += 1
                        while i < len(lines) and lines[i].strip().startswith("|"):
                            i += 1
                        continue
        else:
            updated_lines.append(line)

        i += 1

    return '\n'.join(updated_lines)

# Section名称映射（Markdown中的section名称）
SECTION_MAPPING = {
    "顶层结构": "顶层结构",
    "Activity": "Activity",
    "FullDaySteps": "FullDaySteps",
    "Sleep": "Sleep",
    "SleepDetail": "SleepDetail",
    "SleepType": "SleepType",
    "FullDayHeartRate": "FullDayHeartRate",
    "FullDayHRV": "FullDayHRV",
    "SingleHeart": "SingleHeart",
    "SingleHRV": "SingleHRV",
    "SingleBloodOxygen": "SingleBloodOxygen",
    "SingleStress": "SingleStress",
    "FullDayTemperature": "FullDayTemperature",
    "Training": "Training"
}

def main():
    """主函数"""
    print("开始更新Markdown文件...")

    # 加载比对结果
    comparison_results = load_comparison_results()

    # 读取原始Markdown
    content = read_markdown()

    # 逐个更新每个section
    for section_key, section_name in SECTION_MAPPING.items():
        if section_key in comparison_results:
            print(f"更新 {section_name}...")
            content = update_section(section_name, content, comparison_results[section_key])

    # 保存更新后的内容
    with open(MARKDOWN_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n✓ 更新完成！已保存到 {MARKDOWN_FILE}")

if __name__ == "__main__":
    main()
