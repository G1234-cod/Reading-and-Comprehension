import os
import re


def generate_catalog():
    catalog_lines = []
    # 获取所有以数字开头的文件夹
    folders = sorted([f for f in os.listdir('.') if os.path.isdir(f) and f[0].isdigit()])

    if not folders:
        return ""

    for folder in folders:
        # 处理文件夹名称
        folder_display = folder.replace("_", " ").title()
        if "_" in folder:
            parts = folder.split("_", 1)
            folder_display = f"{parts[0]}. {parts[1].replace('_', ' ').title()}"

        catalog_lines.append(f"\n### {folder_display}\n")

        # 扫描 .md 文件
        files = sorted([f for f in os.listdir(folder) if f.endswith(".md")])
        for filename in files:
            file_path = f"{folder}/{filename}"  # 强制使用正斜杠，兼容性更好
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    line = f.readline().strip()
                    title = line.replace("# 📖 阅读笔记：", "").replace("#", "").strip()
            except:
                title = filename.replace(".md", "")

            catalog_lines.append(f"- [x] [{title or filename}]({file_path})\n")

    return "".join(catalog_lines)


def update_readme():
    # 强制使用 utf-8 读取，防止编码报错
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    new_catalog = generate_catalog()

    # 定义标签
    start_label = ""
    end_label = ""

    # 检查标签是否存在，不存在直接报错提示，而不是乱写
    if start_label not in content or end_label not in content:
        print(f"❌ 错误：在 README.md 中找不到标签！请检查拼写。")
        return

    # 终极正则方案：更宽松的匹配，兼容各种换行符
    pattern = re.compile(rf"{start_label}.*?{end_label}", re.DOTALL)
    replacement = f"{start_label}\n{new_catalog}\n{end_label}"

    new_content = pattern.sub(replacement, content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ README 更新成功！")


if __name__ == "__main__":
    update_readme()