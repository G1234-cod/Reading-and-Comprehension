import os
import re


def generate_catalog():
    catalog_lines = []
    # 自动获取所有以数字开头的文件夹，并按顺序排列
    folders = sorted([f for f in os.listdir('.') if os.path.isdir(f) and f[0].isdigit()])

    for folder in folders:
        # 将 "01_AI_Study" 转化为 "01. AI Study"
        folder_title = folder.replace("_", " ").title()
        if "_" in folder:
            parts = folder.split("_", 1)
            num = parts[0]
            name = parts[1] if len(parts) > 1 else ""
            folder_title = f"{num}. {name.replace('_', ' ').title()}"

        catalog_lines.append(f"\n### {folder_title}\n")

        # 扫描文件夹下的所有 .md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            file_path = os.path.join(folder, filename).replace("\\", "/")
            # 读取文件第一行作为标题
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    # 抓取第一行并去掉 Markdown 的标题符号
                    first_line = f.readline().strip()
                    title = first_line.replace("# 📖 阅读笔记：", "").replace("#", "").strip()
            except:
                title = filename.replace(".md", "")

            catalog_lines.append(f"- [x] [{title or filename}]({file_path})\n")

    return "".join(catalog_lines)


def update_readme():
    # 1. 读取当前的 README 内容
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # 2. 生成最新的目录字符串
    new_catalog = generate_catalog()

    # 3. 核心修复：定义明确的开始和结束标签占位符
    # 必须与你 README.md 中的注释完全一致
    start_label = ""
    end_label = ""

    # 正则表达式：匹配从开始标签到结束标签之间的所有内容（包括换行符）
    pattern = rf"({start_label}).*?({end_label})"

    # \1 和 \2 代表保留这两个标签，中间替换为新目录
    replacement = rf"\1\n{new_catalog}\n\2"

    # 4. 执行替换（flags=re.DOTALL 确保能匹配跨行的内容）
    if start_label in content and end_label in content:
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("README 目录已精准更新！")
    else:
        print("错误：未在 README.md 中找到指定的 HTML 注释占位符！")


if __name__ == "__main__":
    update_readme()