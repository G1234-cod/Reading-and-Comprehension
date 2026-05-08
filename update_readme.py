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
            num, name = folder.split("_", 1)
            folder_title = f"{num}. {name.replace('_', ' ').title()}"

        catalog_lines.append(f"\n### {folder_title}\n")

        # 扫描文件夹下的所有 .md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            file_path = os.path.join(folder, filename).replace("\\", "/")
            # 读取文件第一行作为标题
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    title = f.readline().strip().replace("# 📖 阅读笔记：", "").replace("#", "").strip()
            except:
                title = filename.replace(".md", "")

            catalog_lines.append(f"- [x] [{title or filename}]({file_path})\n")

    return "".join(catalog_lines)


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_catalog = generate_catalog()
    pattern = r"().*?()"
    replacement = rf"\1\n{new_catalog}\n\2"

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == "__main__":
    update_readme()