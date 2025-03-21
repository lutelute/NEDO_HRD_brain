import os
import pandas as pd
from datetime import datetime
import openai
from dotenv import load_dotenv

# ========================
# 設定
# ========================
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

excel_file = "テーマ集DB案.xlsx"
output_folder = "knowledge_cards"

os.makedirs(output_folder, exist_ok=True)

# ========================
# 1. Excelからデータを読み込む
# ========================
df = pd.read_excel(excel_file, header=0)

# 列名を確認
print("エクセル内の列名:", df.columns.tolist())

# 列名を標準化（空白や不要なスペースを削除）
df.columns = df.columns.str.strip()

# プロパティ（属性）の確認
properties = df.columns.tolist()
print("プロパティ（属性）:", properties)

# NaNを空文字列に変換
df = df.fillna("")

# データ部分の取得
data = df.to_dict(orient='records')
print("データ部分:", data)

# ========================
# 2. 初期のMarkdownファイル（ナレッジカード）を作成
# ========================
def create_initial_md(row):
    theme_name = row.get('テーマ名', '無題')
    category = row.get('カテゴリー', '未分類')  # カテゴリーがない場合は「未分類」とする
    metadata = row.get('メタデータ', '')
    project_name = row.get('事業', '')  # 事業名を取得
    
    # ファイル名を安全な形式に変換
    safe_title = "".join([c for c in theme_name if c.isalnum() or c in (' ', '_')]).strip().replace(' ', '_')
    filename = os.path.join(output_folder, f"{safe_title}.md")
    
    # タグ設定 (カテゴリータグ、事業タグ、#事業を追加)
    tags = [f"#{category}"]
    project_tags = []
    
    if project_name:
        # #事業 タグを追加
        tags.append("#事業")
        
        # 事業名からタグを生成（カンマや改行区切りに対応）
        project_tags = [f"#{tag.strip()}" for tag in str(project_name).replace('\n', ',').split(',') if tag.strip()]
        tags.extend(project_tags)
    
    # フロントマターの作成
    front_matter = f"""---
title: "{theme_name}"
tags: {tags}
date: "{datetime.now().strftime('%Y-%m-%d')}"
metadata: "{metadata}"
---

# {theme_name}

この技術課題に関する詳細情報を以下に記載予定です。
"""

    # 本文に事業タグを追加（事業名がある場合）
    body = ""
    if project_name:
        body += "\n\n#事業\n"  # 単体の #事業 タグを追加
        for tag in project_tags:
            body += f"{tag}\n"

    # Markdownファイルの作成
    with open(filename, "w", encoding="utf-8") as f:
        f.write(front_matter + body)
    
    return filename

# 各テーマについてMarkdownファイルを作成
md_files = {row['テーマ名']: create_initial_md(row) for row in data}

print("✅ 初期Markdownファイルの作成完了")
