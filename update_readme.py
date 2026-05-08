import os
import re
import urllib.parse


def generate_catalog():
    catalog_lines = []
    # 1. 遍历以数字开头的模块文件夹
    folders = sorted([f for f in os.listdir('.') if os.path.isdir(f) and f[0].isdigit()])

    for folder in folders:
        # 优化分类标题显示
        folder_display = folder.replace("_", " ").title()
        if "_" in folder:
            parts = folder.split("_", 1)
            folder_display = f"{parts[0]}. {parts[1].replace('_', ' ').title()}"

        catalog_lines.append(f"\n### {folder_display}\n")

        # 2. 遍历文件夹下的 md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            file_path = f"{folder}/{filename}"

            # 3. 读取真实文章标题（不要暴力截断文件名）
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    line = f.readline().strip()
                    title = line.replace("# 📖 阅读笔记：", "").replace("#", "").strip()
                    if not title:
                        title = filename.replace(".md", "")
            except:
                title = filename.replace(".md", "")

            # 🌟 核心修复 1：标题内部的括号转义，防止打断 Markdown 解析
            safe_title = title.replace("[", "\\[").replace("]", "\\]")

            # 🌟 核心修复 2：对路径进行合法的 URL 编码（Trae 提供的正确思路）
            safe_path = urllib.parse.quote(file_path)

            # 生成最终的安全超链接
            catalog_lines.append(f"- [x] [{safe_title}]({safe_path})\n")

    return "".join(catalog_lines)


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_catalog = generate_catalog()

    start_label = ""
    end_label = ""

    if start_label in content and end_label in content:
        pattern = re.compile(rf"{start_label}.*?{end_label}", re.DOTALL)
        replacement = f"{start_label}\n{new_catalog}\n{end_label}"
        new_content = pattern.sub(replacement, content)

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ README 目录已完美更新！")
    else:
        print("❌ 错误：README.md 中找不到占位符标签。")


if __name__ == "__main__":
    update_readme()