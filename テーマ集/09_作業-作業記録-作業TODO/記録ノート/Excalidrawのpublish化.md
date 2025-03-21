



| webサイト                       | 目的                          | リンク                                      |
| ---------------------------- | --------------------------- | ---------------------------------------- |
| Namecheap                    | 格安ドメインの購入1$/年くらい            | https://www.namecheap.com/               |
| CloudFlare                   | web管理                       | https://www.cloudflare.com               |
| Obsidian publish domein help | obsidian publishでドメインに関する設定 | https://help.obsidian.md/publish/domains |


# **Excalidraw を Obsidian Publish で公開する方法**

## **📌 目次**

1. **概要**
2. **必要な準備**
3. **CloudFlare を使ったカスタムドメイン設定**
4. **Excalidraw の設定と SVG エクスポート**
5. **Obsidian Publish で Excalidraw を表示する**
6. **トラブルシューティング**
7. **まとめ**

---

## **1️⃣ 概要**

Obsidian Publish は Obsidian の Markdown ファイルを簡単に Web ページとして公開できる機能ですが、プラグインが動作しないため **Excalidraw を直接埋め込むことができません**。そこで、**Excalidraw の描画を SVG 形式でエクスポートし、Obsidian Publish に埋め込む** 方法を使います。

---

## **2️⃣ 必要な準備**

### **✅ 事前に用意するもの**

- **Obsidian Publish に登録**（有料サービス）
- **カスタムドメインを取得**（Namecheap など）
- **CloudFlare アカウントを作成**（無料プランでOK）
- **Obsidian に Excalidraw プラグインをインストール**

---

## **3️⃣ CloudFlare を使ったカスタムドメイン設定**

Obsidian Publish では、CloudFlare 経由でカスタムドメインを設定する必要があります。

### **✅ Namecheap でドメインを購入した後の手順**

1. **CloudFlare にログインし、購入したドメインを追加**
2. **CloudFlare で DNS 設定を行う**
    - **CNAME レコードを追加**
        - **ルートドメインの場合 (**``**)**
            - `Type`: `CNAME`
            - `Name`: `@`
            - `Target`: `publish-main.obsidian.md`
            - `Proxy Status`: **有効（オレンジの雲）**
        - **サブドメインの場合 (**``**)**
            - `Type`: `CNAME`
            - `Name`: `notes`
            - `Target`: `publish-main.obsidian.md`
            - `Proxy Status`: **有効（オレンジの雲）**
3. **SSL 設定を「Full」に変更**
4. **CloudFlare の「キャッシュ」をクリア**
5. **Obsidian 側でカスタムドメインを設定**

---

## **4️⃣ Excalidraw の設定と SVG エクスポート**

### **✅ Excalidraw のエクスポート設定**

1. **Obsidian の「設定（Ctrl + ,）」を開く**
2. **「Community Plugins」→ 「Excalidraw」を開く**
3. **「Saving」の設定を確認**
    - `exol Auto export SVG` を `true` にする（必要な場合のみ）
4. **Excalidraw で描画し、SVG としてエクスポート**
5. **Obsidian Publish にアップロード**

---

## **5️⃣ Obsidian Publish で Excalidraw を表示する**

### **✅ SVG ファイルを埋め込む方法**

Obsidian の Markdown ファイルに以下のように記述すると、SVG を埋め込めます。

```markdown
![[example-drawing.svg]]
```

### **✅ CSS を適用し、見栄えを調整**

```css
.ex-page-height {
    height: 100vh;
    width: auto;
}
```

---

## **6️⃣ トラブルシューティング**

### **⚠ 「SSL handshake failed」エラーが出る場合**

- **CloudFlare の SSL 設定を「Full」に変更**
- **DNS 設定で **``** のみを使用**
- **CloudFlare のキャッシュをクリア**

### **⚠ 「⚠ Switch to EXCALIDRAW VIEW」エラーが出る場合**

- **Obsidian で Excalidraw ファイルを開く → 「More Options」→ 「Switch to Excalidraw View」を選択**
- **コマンドパレット (**``**) で「Decompress current Excalidraw file」を実行**

---
リンク404
文字化け，エンコード，デコード問題，日本語コード問題

オリジナルテキスト，エンコード前
```
https://www.nedo-hrd.online/NEDO特別講座マップ作業/テーマ集/08_その他/SSO
```

```エンコード後
https://www.nedo-hrd.online/%C3%A3%C2%83%C2%86%C3%A3%C2%83%C2%BC%C3%A3%C2%83%C2%9E%C3%A9%C2%9B%C2%86/01_%C3%A7%C2%A0%C2%94%C3%A7%C2%A9%C2%B6%C3%A3%C2%83%C2%86%C3%A3%C2%83%C2%BC%C3%A3%C2%83%C2%9E-%C3%A7%C2%A0%C2%94%C3%A7%C2%A9%C2%B6%C3%A3%C2%82%C2%BD%C3%A3%C2%83%C2%BC%C3%A3%C2%82%C2%B9/%C3%A8%C2%A4%C2%87%C3%A6%C2%95%C2%B0%C3%A9%C2%9B%C2%BB%C3%A5%C2%9C%C2%A7%C3%A5%C2%88%C2%B6%C3%A5%C2%BE%C2%A1%C3%A6%C2%A9%C2%9F%C3%A5%C2%99%C2%A8%C3%A3%C2%81%C2%AE%C3%A5%C2%8D%C2%94%C3%A8%C2%AA%C2%BF%C3%A5%C2%88%C2%B6%C3%A5%C2%BE%C2%A1%C3%A6%C2%8A%C2%80%C3%A8%C2%A1%C2%93
```

```デコード後
https://www.nedo-hrd.online/ãã¼ãé/01_ç ç©¶ãã¼ã-ç ç©¶ã½ã¼ã¹/è¤æ°é»å§å¶å¾¡æ©å¨ã®åèª¿å¶å¾¡æè¡
```
文字コードが原因か？
- 文字コードShift-JIS, EUCUTF-8(16ビット)などでデコードして確認。-> 原因不明
- ２重エンコーディング問題
	- 自動でSVGが作成されるので，ここで問題があるのでは？
- web上だけの問題。web関連コードは.js
	- コードの修正

[[publish.js]]
```javascript
const clickToEnlarge = "Click and hold to enlarge. SHIFT + wheel to zoom. ESC to reset.";

const clickToCollapse = "ESC to reset. Click and hold to collapse. SHIFT + wheel to zoom";

  

// Check if in iFrame - if yes the page is assumed to be an embedded frame

if (window.self !== window.top) {

  ["div.site-body-right-column", "div.site-body-left-column", "div.site-header", "div.site-footer"].forEach(selector => {

    document.querySelectorAll(selector).forEach(div => {

      div.style.display = "none";

    });

  });

}

  

// 修正済みのデコード関数

const correctUrlEncoding = (url) => {

  try {

    return decodeURIComponent(escape(url));

  } catch (e) {

    return decodeURIComponent(url);

  }

};

  

const processIMG = (img) => {

  const svgURL = img.src;

  const container = img.parentElement;

  

  fetch(svgURL)

    .then(response => response.ok ? response.text() : Promise.reject('Failed to fetch SVG'))

    .then(svgContent => {

      const svgContainer = document.createElement('div');

      svgContainer.innerHTML = svgContent;

  

      svgContainer.querySelectorAll(`a[href]`).forEach(el => {

        let href = el.getAttribute("href");

        if (href.startsWith("obsidian://open?vault=")) {

          let filePart = href.split('&file=')[1] || "";

          let webUrl = "https://www.nedo-hrd.online/" + decodeURIComponent(filePart);

          el.setAttribute("href", webUrl);

        }

      });

  

      svgContainer.querySelectorAll(`iframe[src]`).forEach(el => {

        let src = el.getAttribute("src");

        if (src.startsWith("obsidian://open?vault=")) {

          let filePart = src.split('&file=')[1] || "";

          let webUrl = "https://www.nedo-hrd.online/" + decodeURIComponent(filePart);

          el.setAttribute("src", webUrl);

        }

      });

  

      container.removeChild(img);

      container.appendChild(svgContainer);

    })

    .catch(error => console.error('Error:', error));

};

  

const addImgMutationObserver = () => {

  const observer = new MutationObserver(mutationsList => {

    for (const mutation of mutationsList) {

      if (mutation.type === 'childList') {

        mutation.addedNodes.forEach(node => {

          if (node instanceof Element && node.querySelector(`img[alt$=".svg"]`)) {

            processIMG(node.querySelector(`img[alt$=".svg"]`));

          }

        });

      }

    }

  });

  

  observer.observe(document.body, { childList: true, subtree: true });

};

  

// Process images after loading

document.body.querySelectorAll(`img[alt$=".svg"]`).forEach(processIMG);

addImgMutationObserver();
```


エラーの起こるjs
[オリジナル](https://excalidraw-obsidian.online/wiki/publish/setup)では，英語でのエンコード・デコードだったから問題なかった可能性あり。ブラウザの問題もある？


## **7️⃣ まとめ**

✅ **CloudFlare でカスタムドメインを設定し、Obsidian Publish を有効化**  
✅ **Excalidraw の SVG エクスポートを有効にし、描画を SVG 形式で保存**  
✅ **Markdown に SVG を埋め込んで Obsidian Publish で表示**  
✅ **CloudFlare の SSL/TLS 設定を「Full」にし、エラーを回避**

🚀 **これで Excalidraw を Obsidian Publish に公開できます！**