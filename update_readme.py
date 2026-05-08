import os
import re
from urllib.parse import quote


# 假设这是一个遍历文件夹并生成目录的函数
def generate_catalog(folder):
    catalog_lines = []
    for filename in os.listdir(folder):
        # 安全处理文件名，避免特殊字符问题
        safe_title = re.sub(r'[^\w\s-]', '', filename)

        # 原始文件路径
        file_path = f"{folder}/{filename}"

        # URL 编码处理特殊字符（中括号、空格等）
        encoded_path = quote(file_path, safe='/')

        # 🌟 双重保障：尖括号语法 + URL 编码
        # 无论路径里有多少个中括号、空格、特殊字符，Markdown 都能完美识别
        catalog_lines.append(f"- [x] [{safe_title}](<{encoded_path}>)")

    return catalog_lines


import os
import re


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
            # 原始文件路径
            file_path = f"{folder}/{filename}"

            # 读取文件里的标题
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    line = f.readline().strip()
                    title = line.replace("# 📖 阅读笔记：", "").replace("#", "").strip()
                    if not title:  # 如果第一行是空的，就用文件名
                        title = filename.replace(".md", "")
            except:
                title = filename.replace(".md", "")

            # 🌟 防线 1：把标题里的 [ 和 ] 加上反斜杠转义，防止打断前面的括号
            safe_title = title.replace("[", "\\[").replace("]", "\\]")

            # 🌟 防线 2（核心杀手锏）：用尖括号 < > 把路径包起来！
            # 这样无论路径里有多少个中括号、空格，Markdown 都能完美识别
            catalog_lines.append(f"- [x] [{safe_title}](<{file_path}>)\n")

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

    # 正则替换
    pattern = re.compile(rf"{start_label}.*?{end_label}", re.DOTALL)
    replacement = f"{start_label}\n{new_catalog}\n{end_label}"

    new_content = pattern.sub(replacement, content)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ README 更新成功！")


if __name__ == "__main__":
    update_readme()
