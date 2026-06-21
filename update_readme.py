import os

def generate_catalog():
    catalog_lines = []
    # 自动获取所有以数字开头的文件夹 (例如 01-AI-Agent)
    folders = sorted([f for f in os.listdir('.') if os.path.isdir(f) and f[0].isdigit()])

    for folder in folders:
        # 优化文件夹名字显示: "01-AI-Agent" -> "01. AI Agent"
        if "-" in folder:
            parts = folder.split("-", 1)
            folder_display = f"{parts[0]}. {parts[1].replace('-', ' ')}"
        else:
            folder_display = folder.title()

        catalog_lines.append(f"\n### {folder_display}\n")

        # 扫描该目录下所有的 .md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            file_path = f"{folder}/{filename}"
            # 极简逻辑：去掉.md当作标题
            title = filename.replace(".md", "")
            # 处理标题里的中括号，使用 HTML 实体替换，保护 Markdown 不崩溃
            safe_title = title.replace("[", "&#91;").replace("]", "&#93;")
            
            # 使用尖括号语法保护路径
            catalog_lines.append(f"- [x] [{safe_title}](<{file_path}>)\n")

    return "".join(catalog_lines)


def update_readme():
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("❌ 错误：当前目录下找不到 README.md 文件！")
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_catalog = generate_catalog()

    # 🔥 核心修复：定义明确的物理替换锚点（绝不能是空字符串！）
    start_label = ""
    end_label = ""

    if start_label in content and end_label in content:
        # 找到标签位置，物理挖空并替换
        start_idx = content.find(start_label) + len(start_label)
        end_idx = content.find(end_label)

        new_content = content[:start_idx] + f"\n{new_catalog}\n" + content[end_idx:]

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ README 自动化目录更新成功！")
    else:
        print(f"❌ 错误：在 README.md 中找不到锚点标签！\n请确保你的 README.md 中包含 '{start_label}' 和 '{end_label}'。")


if __name__ == "__main__":
    update_readme()