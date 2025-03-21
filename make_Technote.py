import os
import openai
from dotenv import load_dotenv
from datetime import datetime

# ========================
# 設定
# ========================
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

markdown_folder = "knowledge_cards"  # 既存のMarkdownファイルのフォルダ
instruction_file = "knowledge_cards/instruction.md"  # ノート作成用インストラクションファイル

# ========================
# 1. ノート記述のインストラクションファイルを作成
# ========================
def create_instruction_file():
    instruction_content = '''
# ナレッジノート作成インストラクション

各テーマごとに以下の項目に基づいてノートを作成してください。

## 構成
1. 概要
   - 技術課題に関する簡潔な説明

2. 技術的なポイント
   - 実装上の工夫や技術的なチャレンジ

3. 原理（数式を含む場合はLaTeX形式で記述）
   - 例: $E=mc^2$

4. グラフィカルアブストラクト
   - 図や概念図の説明（画像生成や追加は別途対応）

5. 関連文献や論文の紹介
   - 信頼性のある文献や研究成果を引用

## 形式
- Markdown形式で記述
- 数式は `$` で囲んでLaTeX形式を使用
- 引用文献は `[著者名, 年, 論文タイトル]` の形式
'''

    with open(instruction_file, "w", encoding="utf-8") as f:
        f.write(instruction_content)
    print(f"✅ インストラクションファイルを作成しました: {instruction_file}")

# ========================
# 2. ChatGPT APIを利用してノートを取得
# ========================
def get_note_for_theme(theme_name):
    prompt = f'''
以下の技術課題に関するノートを作成してください。

- 概要
- 技術的なポイント
- 原理（数式はLaTeX形式で記述）
- グラフィカルアブストラクト（図や概念図の説明）
- 関連文献や論文の紹介

技術課題: {theme_name}
'''
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "あなたは技術課題のノート作成アシスタントです。"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    # 修正箇所: 正しい形式でAPIレスポンスから内容を取得
    return response.choices[0].message["content"]

# ========================
# 3. 既存のMarkdownファイルにノートを追記
# ========================
def update_markdown_with_note(filename, theme_name):
    # APIからノートを取得
    note_content = get_note_for_theme(theme_name)
    
    # 既存のMarkdownファイルを読み込み
    with open(filename, "r", encoding="utf-8") as f:
        original_content = f.read()
    
    # ノートを追記して保存
    updated_content = original_content + "\n\n" + note_content
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print(f"✅ ノートを追記しました: {filename}")

# ========================
# 4. 実行：すべてのMarkdownファイルにノートを追加
# ========================
def add_notes_to_all_markdown():
    create_instruction_file()
    
    for file_name in os.listdir(markdown_folder):
        if file_name.endswith(".md"):
            theme_name = os.path.splitext(file_name)[0].replace('_', ' ')
            file_path = os.path.join(markdown_folder, file_name)
            
            try:
                update_markdown_with_note(file_path, theme_name)
            except Exception as e:
                print(f"❌ エラーが発生しました: {theme_name} - {e}")

    print("🎉 すべてのナレッジカードにノートを追加しました。")

# 実行
add_notes_to_all_markdown()
