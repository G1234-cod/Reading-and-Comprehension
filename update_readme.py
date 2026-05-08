import os


def generate_catalog():
    catalog_lines = []
    # 自动获取所有以数字开头的文件夹
    folders = sorted([f for f in os.listdir('.') if os.path.isdir(f) and f[0].isdigit()])

    for folder in folders:
        # 优化文件夹名字显示
        folder_display = folder.replace("_", " ").title()
        if "_" in folder:
            parts = folder.split("_", 1)
            folder_display = f"{parts[0]}. {parts[1].replace('_', ' ').title()}"

        catalog_lines.append(f"\n### {folder_display}\n")

        # 扫描所有的 .md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            file_path = f"{folder}/{filename}"

            # 🌟 极简逻辑：不再去读取文件内部了！直接把文件名（去掉.md）当作标题！
            title = filename.replace(".md", "")

            # 处理标题里的中括号，使用 HTML 实体替换，保护 Markdown 不崩溃
            safe_title = title.replace("[", "&#91;").replace("]", "&#93;")

            # 使用尖括号语法保护路径，末尾加上换行符 \n
            catalog_lines.append(f"- [x] [{safe_title}](<{file_path}>)\n")

    return "".join(catalog_lines)


def update_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_catalog = generate_catalog()

    start_label = ""
    end_label = ""

    if start_label in content and end_label in content:
        # 找到标签位置，物理挖空替换
        start_idx = content.find(start_label) + len(start_label)
        end_idx = content.find(end_label)

        new_content = content[:start_idx] + f"\n{new_catalog}\n" + content[end_idx:]

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ README 更新成功！")
    else:
        print("❌ 错误：在 README.md 中找不到标签！请检查拼写。")


if __name__ == "__main__":
    update_readme()