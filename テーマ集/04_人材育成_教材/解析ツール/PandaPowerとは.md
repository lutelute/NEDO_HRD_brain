---
tag: ツール
---


![[pandapower_logo_S.jpg]]

# 🐼 **PandaPowerとは？**

> [!abstract]  
> **📌 概要**  
> PandaPower は、**Python ベースのオープンソース電力系統解析ライブラリ** です。  
> **MATPOWER の Python 版** とも言われ、潮流計算（PF）、最適潮流計算（OPF）、短絡計算（SC）、時系列シミュレーションなどが可能です。
> 
> **🔹 特徴**  
> ✅ 完全にオープンソース & Python ネイティブ  
> ✅ **pandas & NumPy** を活用し、高速な計算が可能  
> ✅ **MATPOWER との互換性** を備えたデータ構造  
> ✅ 送電系統・配電系統の両方に対応
> 
> **🔹 主な用途**
> 
> - 電力系統の潮流計算 (PF)・最適潮流計算 (OPF)
> - 再生可能エネルギーの統合・時系列解析
> - 配電網の解析 & 短絡計算
> - 送配電シミュレーションと最適化

---

## **1. PandaPowerとは？**

PandaPower は、Python で電力系統解析を行うための強力なオープンソースライブラリです。  
MATPOWER や PSS/E などの商用ソフトウェアと同様の機能を提供しつつ、**Python のエコシステムと完全統合** されています。

- **開発元**: Fraunhofer IEE（ドイツの研究機関）
- **ライセンス**: MIT License（商用利用可）
- **主な用途**:
    - 送電系統・配電系統のモデリング & 解析
    - 最適潮流計算（OPF）・経済負荷配分（ED）
    - スマートグリッド & 再生可能エネルギー統合シミュレーション
    - 短絡解析（SC）・電圧安定性解析

---

## **2. PandaPowerの主な機能**

PandaPower は、電力システム解析に必要な主要な機能を備えています。

|機能|説明|
|---|---|
|**潮流計算 (Power Flow, PF)**|Newton-Raphson法、直流潮流 (DC-PF) に対応|
|**最適潮流計算 (Optimal Power Flow, OPF)**|発電コスト最小化・電圧制御などを最適化|
|**短絡計算 (Short-Circuit Analysis, SC)**|IEC60909に準拠した短絡電流計算|
|**時系列解析 (Time Series Simulation)**|需要変動や再生可能エネルギーの統合をシミュレーション|
|**潮流解析の可視化**|matplotlib, Plotly でネットワークを可視化|
|**MATPOWER 互換データフォーマット**|MATPOWER のケースファイルをインポート可能|

特に、PandaPower は **MATPOWER の代替として利用されることが多く**、Python ユーザーにとって非常に扱いやすいツールです。

---

## **3. PandaPower のインストール**

PandaPower は、`pip` を使用して簡単にインストールできます。

```bash
pip install pandapower
```

または、開発版を GitHub からインストールする場合：

```bash
pip install git+https://github.com/e2nIEE/pandapower.git
```

依存ライブラリ：

- **NumPy, pandas**：データ構造の操作
- **SciPy**：数値計算
- **Matplotlib, Plotly**：可視化
- **Pyomo**：最適化問題の解決（OPF 計算）

---

## **4. PandaPower の基本的な使い方**

### **4.1. 電力系統の作成**

PandaPower では、**ネットワークをオブジェクト指向的に構築** できます。

```python
import pandapower as pp

# 空のネットワークを作成
net = pp.create_empty_network()

# バスを追加
bus1 = pp.create_bus(net, vn_kv=110)  # 110kVのバス
bus2 = pp.create_bus(net, vn_kv=110)

# 発電機を追加
pp.create_gen(net, bus1, p_mw=100, min_p_mw=0, max_p_mw=100, vm_pu=1.02)

# 負荷を追加
pp.create_load(net, bus2, p_mw=50, q_mvar=30)

# 送電線を追加
pp.create_line(net, bus1, bus2, length_km=10, std_type="149-AL1/24-ST1A 110.0")

# 潮流計算の実行
pp.runpp(net)

# 計算結果の表示
print(net.res_bus)
```

---

### **4.2. 最適潮流計算（OPF）**

PandaPower では、Pyomo を使用して **最適潮流計算（OPF）** を実行できます。

```python
import pandapower.optimal_powerflow as opf

# OPF用のコスト関数を設定（発電コスト最小化）
pp.create_poly_cost(net, 0, "gen", cp1_eur_per_mw=50)

# OPFの実行
opf.runopp(net)

# 結果の表示
print(net.res_gen)
```

---

### **4.3. ネットワークの可視化**

PandaPower には、**電力ネットワークの可視化機能** も備わっています。

```python
import pandapower.plotting as plot

# ネットワークを可視化
plot.simple_plot(net)
```

また、Plotly を使ったインタラクティブな可視化も可能です。

---

## **5. PandaPower vs MATPOWER**

PandaPower は **MATPOWER の Python 版** と言われることが多いですが、いくつかの違いがあります。

|項目|PandaPower|MATPOWER|
|---|---|---|
|**プラットフォーム**|Python|MATLAB|
|**オープンソース**|✅|✅|
|**潮流計算 (PF)**|✅|✅|
|**最適潮流計算 (OPF)**|✅|✅|
|**時系列解析**|✅|❌|
|**可視化機能**|✅|❌|
|**商用ソフト統合**|PSS/E, PyPSA など|PSS/E, PowerWorld など|

Python を主に使う場合は **PandaPower** を、MATLAB ベースの解析を行う場合は **MATPOWER** を選択するとよいでしょう。

---

## **6. 産業応用**

PandaPower は、以下のような分野で利用されています。

- **再生可能エネルギー統合**：PV・風力発電のシミュレーション
- **電力系統の最適化**：最適潮流（OPF）・経済負荷配分（ED）
- **配電網の解析**：短絡計算・電圧制御
- **スマートグリッド**：需要応答（DR）・マイクログリッド制御

---

## **7. 参考文献 & リンク**

1. PandaPower 公式サイト: [https://www.pandapower.org/](https://www.pandapower.org/)
2. GitHub リポジトリ: [https://github.com/e2nIEE/pandapower](https://github.com/e2nIEE/pandapower)
3. “PandaPower - A Python Tool for Power System Analysis” (Fraunhofer IEE)

---

## **📌 まとめ**

✔ PandaPower は **Python ベースの電力系統解析ライブラリ**  
✔ **潮流計算（PF）、最適潮流（OPF）、短絡計算（SC）、時系列解析** が可能  
✔ **MATPOWER の Python 版として利用可能**  
✔ **可視化・最適化機能が充実し、送配電系統解析に広く活用**

