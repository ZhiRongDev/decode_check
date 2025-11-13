#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理比對結果.md文件中重复的示例表格
"""
import re

MARKDOWN_FILE = "match /比對結果.md"

def cleanup_markdown():
    """清理Markdown文件，移除重复的示例表格"""
    with open(MARKDOWN_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    cleaned_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        cleaned_lines.append(line)

        # 检查是否是"多出來的欄位"后的表格
        if line.strip() == "多出來的欄位":
            # 添加空行
            i += 1
            if i < len(lines) and not lines[i].strip():
                cleaned_lines.append(lines[i])
                i += 1

            # 添加第一个表格（正确的表格）
            if i < len(lines) and lines[i].startswith('|'):
                # 表头
                cleaned_lines.append(lines[i])
                i += 1
                # 分隔线
                if i < len(lines) and lines[i].startswith('|'):
                    cleaned_lines.append(lines[i])
                    i += 1

                # 数据行
                while i < len(lines) and lines[i].strip().startswith('|'):
                    cleaned_lines.append(lines[i])
                    i += 1

                # 跳过重复的表格（示例表格）
                # 跳过空行
                while i < len(lines) and not lines[i].strip():
                    i += 1

                # 如果遇到另一个表格头（重复的），跳过整个表格
                if i < len(lines) and lines[i].startswith('| Hti 比對結果'):
                    # 跳过表头
                    i += 1
                    # 跳过分隔线
                    if i < len(lines) and lines[i].startswith('|'):
                        i += 1
                    # 跳过数据行
                    while i < len(lines) and lines[i].strip().startswith('|'):
                        i += 1

                # 继续处理
                continue

        i += 1

    # 保存清理后的内容
    with open(MARKDOWN_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))

    print(f"✓ 清理完成！已移除重复的示例表格")

if __name__ == "__main__":
    cleanup_markdown()
