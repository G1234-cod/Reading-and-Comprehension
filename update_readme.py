import os
import re
import urllib.parse  # 🌟 新增：专门用来对付各种特殊符号的官方库


def generate_catalog():
    catalog_lines = []
    # 获取所有以数字开头的文件夹
    folders = sorted([f for f in os.listdir('.') if os.path.isdir(f) and f[0].isdigit()])

    for folder in folders:
        # 处理文件夹名字
        folder_display = folder.replace("_", " ").title()
        if "_" in folder:
            parts = folder.split("_", 1)
            folder_display = f"{parts[0]}. {parts[1].replace('_', ' ').title()}"

        catalog_lines.append(f"\n### {folder_display}\n")

        # 扫描 .md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            # 原始的本地路径
            file_path = f"{folder}/{filename}"

            # 🌟 核心防线 1：将路径转化为安全的网页链接格式（把空格变成 %20，中括号变成 %5B 等）
            safe_file_path = urllib.parse.quote(file_path)

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    line = f.readline().strip()
                    title = line.replace("# 📖 阅读笔记：", "").replace("#", "").strip()
            except:
                title = filename.replace(".md", "")

            # 🌟 核心防线 2：如果文章标题本身包含中括号 []，给它加上反斜杠进行“转义”，防止 Markdown 认错
            safe_title = title.replace("[", "\\[").replace("]", "\\]")

            # 写入 README，使用安全的标题和安全的路径
            catalog_lines.append(f"- [x] [{safe_title or filename}]({safe_file_path})\n")

    return "".join(catalog_lines)


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_catalog = generate_catalog()

    start_label = ""
    end_label = ""

    if start_label not in content or end_label not in content:
        print(f"❌ 错误：在 README.md 中找不到标签！请检查拼写。")
        return

    # 匹配并替换
    pattern = re.compile(rf"{start_label}.*?{end_label}", re.DOTALL)
    replacement = f"{start_label}\n{new_catalog}\n{end_label}"

    new_content = pattern.sub(replacement, content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ README 更新成功！")


if __name__ == "__main__":
    update_readme()