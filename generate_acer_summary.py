#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Acer线上数据包缺少字段的总结
"""
import json

def generate_acer_missing_summary():
    """生成 Acer 缺少字段的总结"""
    # 加载比对结果
    with open('comparison_results.json', 'r', encoding='utf-8') as f:
        results = json.load(f)

    # 统计 Acer 缺少字段的表格
    sections_with_missing = []

    for section_name, section_data in results.items():
        acer_missing = section_data['missing'].get('acer', [])
        if acer_missing:
            sections_with_missing.append({
                'section': section_name,
                'missing_fields': acer_missing
            })

    # 生成 Markdown 总结
    summary = []
    summary.append("## Acer线上数据包 缺少字段总结\n")

    if not sections_with_missing:
        summary.append("✅ Acer线上数据包包含所有 Ground Truth 表格中定义的字段。\n")
    else:
        summary.append(f"Acer线上数据包在以下 {len(sections_with_missing)} 个表格中缺少字段：\n")

        for item in sections_with_missing:
            section = item['section']
            missing = item['missing_fields']
            summary.append(f"### {section}")
            summary.append(f"缺少 {len(missing)} 个字段：")
            for field in missing:
                summary.append(f"- {field}")
            summary.append("")

    return '\n'.join(summary)

if __name__ == "__main__":
    summary = generate_acer_missing_summary()
    print(summary)

    # 读取原始 Markdown
    with open("match /比對結果.md", 'r', encoding='utf-8') as f:
        content = f.read()

    # 在第一个 # 顶层结构 之前插入总结
    lines = content.split('\n')
    insert_index = 0

    for i, line in enumerate(lines):
        if line.strip() == "# 顶层结构":
            insert_index = i
            break

    # 插入总结
    new_lines = lines[:insert_index] + summary.split('\n') + [''] + lines[insert_index:]

    # 保存
    with open("match /比對結果.md", 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

    print("\n✓ 已将 Acer 缺少字段总结添加到比對結果.md")
