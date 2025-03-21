

このファイルはアウトライン(0_xxx)ファイルで直接書き込むことはしない。
ファイルリンクのみ。

---
## 未完了_All_TODO

> [!caution]  
> ~~Web上では、Dataviewのインタラクティブな動作は反映されない。~~  
> `Dataview Publisher` を使用すると、Dataviewのクエリ結果を静的なテキストとして保存し、Obsidian Publishで表示できる。  
> ただし、データの更新は手動で実行する必要があり、JavaScriptによる動的な動作は行われない。



%% DATAVIEW_PUBLISHER: start
```dataview
TASK FROM "テーマ集/09_作業-作業記録-作業TODO/TODO置き場"
WHERE !completed
SORT file.name ASC
```
%%

- [ ] Githubでノートごと全部アップロードして共有する環境構築
    - [ ] gitの設定 (重信苦手)
- [ ] TODO管理や研究進捗管理
- [ ] Metaデータの管理 [[TODO_DB化]]にも必要
- [ ] styleの設定
    - @2025-03-06まだうまくできていない可能性あり。アップロードされていない？
- [ ] Readmeをつくる
    - [ ] デモであることや，サイトの説明
- [ ] KANBANを使えるようにしたい。 
- [ ] ファイルの作成
- [ ] サイトデザイン
- [ ] コンテンツの充実

%% DATAVIEW_PUBLISHER: end %%





---
ファイルDB

```dataview
TABLE text AS "タスク", file.name AS "ファイル", description AS "説明", file.mtime AS "最終更新"
FROM "テーマ集/09_作業-作業記録-作業TODO/TODO置き場"
WHERE !completed
SORT file.mtime DESC

```

---
## [[TODO_DB化]]
![[TODO_DB化#概要]]


## [[TODO_Obsidianデザイン]]
![[TODO_Obsidianデザイン#概要]]


## [[xx_仕分け前TODO]]
![[xx_仕分け前TODO]]




