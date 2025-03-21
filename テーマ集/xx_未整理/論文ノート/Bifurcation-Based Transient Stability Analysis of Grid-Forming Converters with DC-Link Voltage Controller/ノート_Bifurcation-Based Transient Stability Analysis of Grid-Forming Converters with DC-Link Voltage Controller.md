
> [!note] 
> 
| AIによる作成                              | オリジナル                                |
| ------------------------------------ | ------------------------------------ |
| ![[Pasted image 20250316165302.png]] | ![[Pasted image 20250316165240.png]] |
|                                      |                                      |
微分方程式を，動揺方程式，電力の式，電圧の式，から導出。(微分代数方程式)




## TODO
GFMにDCバス制御は必要か？
安定性は向上するか？
- 目的は？
	- - **過渡安定性の向上**
	    - DCバス電圧の適切な制御により、インバータの同期喪失（Loss of Synchronism: LOS）を防ぎ、大きな系統擾乱（フェーズジャンプ、短絡事故など）に対する耐性を向上させる。
	    - 例えば、従来の飽和リミッター（CSL: Conventional Saturation Limiter）はDVCと組み合わせることで、一時的なダンピングを提供し、過渡安定性を向上させる。
	- **DCバスの過電圧抑制**
	    - 適切なDCバス電圧制御を行わないと、インバータの出力電力が急激に変動し、DCバスに過剰なエネルギーが流れ込み、電圧が上昇してしまう。
	    - 特に、過電圧が発生すると保護回路が作動し、インバータの動作が停止する可能性がある。柔軟な飽和リミッター（FSL: Flexible Saturation Limiter）を用いることで、DCバス電圧のピークを抑えることが可能となる。
	- **電力変動の平滑化**
	    - DCバス電圧を安定に保つことで、インバータの出力電力の急激な変動を抑制し、系統への影響を低減する。
	    - これにより、インバータベースの電源が系統周波数の調整に貢献しやすくなる。
	- **故障時の電流制限**
	    - 事故（短絡や地絡）が発生した際に、DCバス電圧を適切に低下させることで、故障電流を抑制し、電力系統の保護に貢献する。
	    - これは、従来の交流系統で発生する過渡現象（例えば、発電機の加速エネルギーが蓄積され、事故除去後に減速エネルギーが不足し脱調する現象）に相当する影響を直流系統で軽減する働きを持つ。

下記2つの系統図+制御図(簡易)，動揺方程式とDCバスのPI制御の連結について，伝達関数でモデル化し，安定性を評価。
この安定性は，GFMのDCバスの安定性のことであり，[[系統安定性]]や[[動態安定度]]，[[系統の過渡安定性]]などではない。
![[Pasted image 20250316164925.png]]
![[Pasted image 20250316164944.png]]
# GFMコンバータの過渡安定性解析（第2章まで）

このノートでは、GFM（Grid-Forming）コンバータの過渡安定性解析について解説し、MATLABコードを用いて位相図を描画する方法を示します。

## **1. 基本定数の定義**
まず、システムの基本的なパラメータを定義します。

```matlab
% 定数の定義（表Iのデータ）
Vg = 40; % グリッド電圧(V, rms)
E0 = 40; % 定格電圧
Lg = 8e-3; % グリッドインダクタンス(H)
Lf = 3e-3; % フィルタインダクタンス(H)
Cf = 20e-6; % フィルタキャパシタ(F)
Vdc_ref = 400; % 定格DCリンク電圧(V)
Cdc = 450e-6; % DC側キャパシタ(F)
kpf = 0.0126; % P-fドロップ係数
kidc = 0.025; % DVCの積分ゲイン
kpdc_values = [0.0080, 0.0040, 0.0024]; % DVCの比例ゲイン
Pd = 640; % 定格有効電力(W)
f0 = 50; % 系統周波数(Hz)
```

## **2. 平衡点の計算**
GFMコンバータの平衡点は以下の式で求められます。

$$
\delta_{eq} = \arcsin\left( \frac{2 P_d X_T}{3 E_0 V_g} \right)
$$

MATLABコードでの実装は以下のようになります。

```matlab
XT = 2.90; % 修正後の総インピーダンス
Vg_fault = 0.6 * 40 * sqrt(2); % 故障時のグリッド電圧
E0_amp = E0 * sqrt(2);

delta_eq = asin((2 * Pd * XT) / (3 * E0_amp * Vg_fault));
Vdc_eq = Vdc_ref^2;
P_eq = Pd;
eq_point = [delta_eq; Vdc_eq; P_eq];

% 平衡点の表示
disp('Stable Equilibrium Point (h_a):');
disp(['δ_eq = ', num2str(delta_eq), ' rad']);
disp(['Vdc_eq = ', num2str(Vdc_eq), ' V^2']);
disp(['P_eq = ', num2str(P_eq), ' W']);
```

## **3. 初期条件の設定**
シミュレーションの初期条件として、$\delta = 0.51$  を設定し、 $\dot{\delta}$  を自動計算します。

```matlab
% 角速度 dδ/dt の初期値を計算
d_delta_dt_0 = kpf * (P_eq - (3/2) * (E0_amp * Vg_fault / XT) * sin(0.51));
x0 = [0.51; d_delta_dt_0; 0];
```

## **4. 位相図のシミュレーション**
位相軌道を[[ODE(Ordinary Differential Equation)]]を使ってシミュレーションします。

```matlab
figure;
hold on;
grid on;
tspan = [0, 10]; % 時間範囲
options = odeset('RelTol',1e-6,'AbsTol',1e-8); % 精度設定

for kpdc = kpdc_values
    [t, x] = ode45(@(t,x) [
        kpf * (x(3) - (3/2) * (E0_amp * Vg_fault / XT) * sin(x(1)));
        (2/Cdc) * (Pd - (3/2) * (E0_amp * Vg_fault / XT) * sin(x(1)));
        (1/2) * kidc * (x(2) - Vdc_ref^2) + (kpdc / Cdc) * (Pd - (3/2) * (E0_amp * Vg_fault / XT) * sin(x(1)))
    ], tspan, x0, options);

    % 収束点の取得
    c_point = x(end, :);
    disp('Converged Point (c):');
    disp(['δ_c = ', num2str(c_point(1)), ' rad']);
    disp(['Vdc_c = ', num2str(c_point(2)), ' V^2']);
    disp(['P_c = ', num2str(c_point(3)), ' W']);

    % dδ/dt の計算
d_delta_dt = kpf * (x(:,3) - (3/2) * (E0_amp * Vg_fault / XT) * sin(x(:,1)));
    
    % 位相図のプロット
    plot(x(:,1), d_delta_dt, 'LineWidth', 1.5, 'DisplayName', ['kpdc=', num2str(kpdc)]);
end

xlabel('Power Angle δ (rad)');
ylabel('dδ/dt (rad/s)');
title('Phase portraits under different kpdc');
legend show;
xlim([-0.5 2.5]);
ylim([-10 15]);
hold off;
```

## **5. 結果の考察**
- シミュレーション結果を Fig. 3（論文の図）と比較し、システムの過渡特性を確認。
- 初期状態 \( a \) から、最大角速度点 \( b \) を通過し、平衡点 \( c \) に収束する。
- \( kpdc \) を小さくすると、収束が困難になることが確認できる。

これで、GFMコンバータの過渡安定性解析を MATLAB でシミュレーションし、論文の位相図を再現しました。
