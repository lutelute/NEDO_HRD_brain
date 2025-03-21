---
tag: 負荷モデル
---



# **⏳ 周波数依存負荷モデル（Frequency-Dependent Load Model）**

> [!abstract]  
> **📌 概要**  
> 周波数依存負荷モデルは、電力系統の周波数変動に対する負荷の応答を考慮するモデルです。  
> **特徴**：
> 
> - 🔄 需給バランスの変動に応じた負荷の変化をモデル化
> - 📉 低周波時の負荷低下（アンダーフリークエンシー・ロードシェディング）を考慮可能
> - 🏭 産業用プロセス負荷、送風機、ポンプ負荷のモデリングに有効  
>     **適用例**：
> - 需給バランス異常時の負荷応答評価
> - 周波数制御（一次・二次制御）シミュレーション
> - 大規模停電時の負荷遮断解析

---

## **1. 周波数依存負荷モデルとは？**

周波数依存負荷モデル（Frequency-Dependent Load Model）は、電力系統の周波数変動に対する負荷の応答を考慮する負荷モデルです。  
一般的に、電力系統の周波数が変動すると、以下のような影響が生じます。

1. **周波数低下（$f < f_0$）**
    - 送風機、ポンプ、誘導電動機の負荷低下
    - 負荷遮断制御（UFLS: Under-Frequency Load Shedding）
2. **周波数上昇（$f > f_0$）**
    - 回転機器の負荷増加
    - 過負荷による機器故障のリスク増大

このモデルは、特に**電力系統の一次制御・二次制御や、大規模停電解析において重要**となります。

---

## **2. 数学的モデル**

周波数依存負荷モデルは、以下の関係式で表されます。

### **(1) 負荷の周波数感度モデル**

負荷の消費電力は、周波数変化に応じて変動し、以下のようにモデル化されます。
$$
P_L = P_0 \left(1 + K_p \Delta f \right), Q_L = Q_0 \left(1 + K_q \Delta f \right)
$$
ここで：

- $P_L, Q_L$ ：負荷の有効電力および無効電力
- $P_0, Q_0$ ：基準周波数 $f_0$ における有効・無効電力
- $\Delta f = f - f_0$ ：周波数変化量
- $K_p, K_q$ ：周波数感度係数（通常 $K_p = 0.5 \sim 2.0$）

周波数が低下すると（$\Delta f < 0$）、$P_L$ や $Q_L$ も低下し、負荷の減少を再現できます。

---

### **(2) 周波数依存負荷の過渡応答**

負荷の応答には一定の遅れがあり、一般的に**時定数 $\tau$ を持つ一次遅れ系**としてモデル化されます。
$$
\frac{dP_L}{dt} = \frac{1}{\tau} \left( P_0 (1 + K_p \Delta f) - P_L \right) , \frac{dQ_L}{dt} = \frac{1}{\tau} \left( Q_0 (1 + K_q \Delta f) - Q_L \right)
$$
ここで：

- $\tau$ ：負荷の時定数（通常 $\tau = 0.1 \sim 2.0$ 秒）
- 負荷は瞬時に変化するのではなく、**一定の遅れを伴って周波数変化に追従**する

---

## **3. 代表的な負荷の周波数感度**

負荷の種類によって、周波数変化に対する応答（$K_p, K_q$）は異なります。

|負荷の種類|有効電力感度 $K_p$|無効電力感度 $K_q$|時定数 $\tau$|
|---|---|---|---|
|**送風機・ポンプ負荷**|1.5|0.5|0.5 s|
|**電気ヒーター**|0.0|0.0|なし|
|**誘導電動機負荷**|1.0|2.0|1.0 s|
|**データセンター（電子負荷）**|0.3|0.2|0.1 s|

- **送風機・ポンプ負荷** は周波数変動に敏感であり、低周波時に電力消費が急減する
- **電気ヒーター** は周波数変動に影響されにくい
- **データセンターなどの電子負荷** は比較的安定しているが、瞬時応答性が高い

---

## **4. MATLAB / MATPOWER における実装**

MATLABを使用して、周波数依存負荷の動作をシミュレーションできます。

```matlab
% 基本パラメータ
f0 = 50;    % 基準周波数 (Hz)
P0 = 100;   % 基準有効電力 (MW)
Q0 = 50;    % 基準無効電力 (MVar)
Kp = 1.5;   % 有効電力感度
Kq = 0.5;   % 無効電力感度
tau = 0.5;  % 時定数 (s)

% 時間変化
t = linspace(0, 10, 100);
df = -0.02 * exp(-t); % 周波数低下

% 負荷応答の計算
P_L = P0 * (1 + Kp * df);
Q_L = Q0 * (1 + Kq * df);

% プロット
figure;
plot(t, P_L, 'b-', 'LineWidth', 2);
hold on;
plot(t, Q_L, 'r--', 'LineWidth', 2);
xlabel('時間 (秒)');
ylabel('負荷電力 (MW, MVar)');
legend('有効電力 P_L', '無効電力 Q_L');
title('周波数依存負荷の応答');
grid on;
```

このスクリプトを実行すると、周波数低下時の負荷変動が可視化されます。

---

## **5. 産業応用**

周波数依存負荷モデルは、以下のような分野で使用されます。

- **需給調整と周波数制御**
    - 一次・二次周波数制御の応答解析
- **大規模停電の防止**
    - アンダーフリークエンシー・ロードシェディング（UFLS）の評価
- **再生可能エネルギーの統合**
    - 太陽光・風力発電の変動が周波数安定性に与える影響解析

---

## **6. 参考文献**

1. IEEE Task Force, **“Load Representation for Dynamic Performance Analysis”**, IEEE Transactions on Power Systems, 1993.
2. Kundur, **“Power System Stability and Control”**, McGraw-Hill, 1994.
3. Anderson, P. M., **“Power System Control and Stability”**, IEEE Press, 2003.

---

## **📌 まとめ**

✔ 周波数依存負荷モデルは、系統の周波数変動に対する負荷の応答を考慮する手法  
✔ 需給バランスの変動時の負荷挙動を正確にシミュレーション可能  
✔ 電力系統の周波数制御、大規模停電の防止、再生可能エネルギーの安定化に活用

---

全ての負荷モデルのノートが揃いました。他に追加したい内容があれば教えてください。