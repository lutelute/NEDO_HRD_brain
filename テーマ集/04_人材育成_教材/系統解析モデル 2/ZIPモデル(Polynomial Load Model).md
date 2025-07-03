---
tag: 負荷モデル
---



# **📌 ZIPモデル（Polynomial Load Model）**




>[!abstract]
> 🔹 **概要**  
> ZIPモデル（Polynomial Load Model）は、負荷を **定インピーダンス (Z)、定電流 (I)、定電力 (P)** の3つの成分に分解して表現する負荷モデルです。  
> これにより、電圧変動に対する負荷の特性を柔軟にモデリングできます。
> 
> 🔹 **特長**  
> ✅ 3つの成分の割合を調整することで、多様な負荷特性を表現可能  
> ✅ 電圧安定性解析や最適潮流計算（OPF）に有用  
> ✅ MATPOWERやPSSEなどの電力系統解析ツールで広く採用
> 
> 🔹 **適用例**
> 
> - 再生可能エネルギー統合時の負荷影響評価
> - 需要応答（Demand Response）モデリング
> - 電圧制御戦略の最適化

---

## **1. ZIPモデルとは？**

ZIPモデルは、負荷の電圧依存特性を3つの成分で表現する汎用的な負荷モデルです。
$$
P_L = P_0 \left( k_Z \left(\frac{V}{V_0}\right)^2 + k_I \left(\frac{V}{V_0}\right) + k_P \right), Q_L = Q_0 \left( k_{Zq} \left(\frac{V}{V_0}\right)^2 + k_{Iq} \left(\frac{V}{V_0}\right) + k_{Pq} \right)
$$
ここで：

- $P_L, Q_L$ : 負荷の有効電力・無効電力
- $P_0, Q_0$ : 基準電圧 $V_0$ における有効・無効電力
- $V$ : 実際のバス電圧
- $V_0$ : 基準電圧（通常 1.0 p.u.）
- $k_Z, k_I, k_P$ : 有効電力に対する **定インピーダンス・定電流・定電力** の割合（$k_Z + k_I + k_P = 1$）
- $k_{Zq}, k_{Iq}, k_{Pq}$ : 無効電力に対する定数

各係数を調整することで、電圧変動に対する負荷の応答を柔軟に設計できます。

---

## **2. ZIPモデルの各成分**

|成分|説明|電圧依存性|
|---|---|---|
|**定インピーダンス (Z)**|負荷が一定のインピーダンスを持つと仮定|$V^2$ に比例|
|**定電流 (I)**|負荷が一定の電流を消費すると仮定|$V$ に比例|
|**定電力 (P)**|負荷が一定の電力を消費すると仮定|電圧非依存|

特定の負荷に対して、それぞれの成分の比率を調整することで、現実的な負荷特性を再現できます。

---

## **3. 代表的な負荷のZIP成分**

|負荷の種類|$k_Z$ (定インピーダンス)|$k_I$ (定電流)|$k_P$ (定電力)|
|---|---|---|---|
|**照明負荷 (Lighting Load)**|1.8|0.2|0.0|
|**電熱負荷 (Electric Heating)**|0.0|0.0|1.0|
|**誘導電動機 (Induction Motor Load)**|0.4|0.3|0.3|
|**電子機器 (Electronic Devices)**|0.2|0.5|0.3|

例えば、**電熱負荷** は定電力成分 $k_P = 1$ が大きく、**照明負荷** は定インピーダンス成分が大きいことがわかります。

---

## **4. MATLAB / MATPOWER における実装**

MATPOWERでは、ZIPモデルの負荷は `bus` データに組み込まれています。  
MATLABでZIP負荷モデルをシミュレーションする基本コードは以下のようになります。

```matlab
% 基準電圧と負荷の初期値
V0 = 1.0;   % 基準電圧 (p.u.)
P0 = 100;   % 基準有効電力 (MW)
Q0 = 50;    % 基準無効電力 (MVar)

% 電圧変化の範囲
V = linspace(0.8, 1.2, 100);

% ZIPモデルのパラメータ
k_Z = 0.4;
k_I = 0.3;
k_P = 0.3;

% 負荷の計算
P_L = P0 * (k_Z * (V/V0).^2 + k_I * (V/V0) + k_P);
Q_L = Q0 * (k_Z * (V/V0).^2 + k_I * (V/V0) + k_P);

% プロット
figure;
plot(V, P_L, 'b-', 'LineWidth', 2);
hold on;
plot(V, Q_L, 'r--', 'LineWidth', 2);
xlabel('電圧 (p.u.)');
ylabel('負荷電力 (MW, MVar)');
legend('有効電力 P_L', '無効電力 Q_L');
title('ZIP負荷モデルの特性');
grid on;
```

このスクリプトを実行すると、電圧変動に対する負荷応答を可視化できます。

---

## **5. 産業応用**

ZIPモデルは、以下のような分野で活用されています。

- **電力系統の安定性解析**
    - 負荷の電圧依存性を考慮したシミュレーション
- **電圧制御**
    - 需要家側の電圧調整の影響を解析
- **スマートグリッドと需要応答**
    - 負荷の動的な変化を考慮した最適化

---

## **6. 参考文献**

1. IEEE Task Force, **“Load Representation for Dynamic Performance Analysis”**, IEEE Transactions on Power Systems, 1993.
2. R. D. Zimmerman, C. E. Murillo-Sánchez, and R. J. Thomas, **“MATPOWER: Steady-State Operations, Planning, and Analysis Tools for Power Systems Research and Education”**, IEEE Transactions on Power Systems, Vol. 26, No. 1, 2011.
3. P. Kundur, **“Power System Stability and Control”**, McGraw-Hill, 1994.

---

## **📌 まとめ**

✔ ZIPモデルは、負荷の電圧依存特性を **定インピーダンス (Z)、定電流 (I)、定電力 (P)** の3成分で表現する汎用的なモデル  
✔ パラメータの設定次第で、様々な負荷特性を表現可能  
✔ 電力系統解析、電圧制御、最適潮流計算に広く活用

---

この形式で問題なければ、次に **過渡負荷モデル (Induction Motor Load Model)** を作成します。修正点や追加の要望があれば教えてください。