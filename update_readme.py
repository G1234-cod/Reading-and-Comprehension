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

            # 默认标题就是你的文件名（去掉.md）
            title = filename.replace(".md", "")

            # 🌟 终极修复 1：逐行扫描，只要找到带 # 的真正标题就立刻替换并跳出！
            # 再也不怕第一行是空行了！
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("#"):
                            # 提取真正的标题文字
                            title = line.replace("# 📖 阅读笔记：", "").replace("#", "").strip()
                            break  # 找到了真正的标题，立刻停止扫描
            except Exception as e:
                print(f"⚠️ 读取 {filename} 失败，将使用文件名作为标题。")

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
        # 🌟 终极修复 2：彻底废弃正则！使用最暴力的物理切片法！
        # 找到开始标签的末尾位置
        start_idx = content.find(start_label) + len(start_label)
        # 找到结束标签的起始位置
        end_idx = content.find(end_label)

        # 将中间的内容彻底挖空，强行拼接上新的目录
        new_content = content[:start_idx] + f"\n{new_catalog}\n" + content[end_idx:]

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ README 更新成功！物理切片执行完毕，绝不可能重复！")
    else:
        print("❌ 错误：在 README.md 中找不到标签！请检查拼写。")


if __name__ == "__main__":
    update_readme()