---

---


![[matpower_logo_S.png]]

# MATPOWERとは

## 1. 概要

MATPOWERは、MATLABおよびGNU Octave上で動作する電力系統解析ツールです。主に最適潮流計算（Optimal Power Flow, OPF）や潮流計算（Power Flow Analysis）など、電力システムの解析・最適化を目的としたツールボックスです。

## 2. 特徴

- **オープンソース**: 無料で利用可能であり、カスタマイズも可能
- **高機能**: 潮流計算、最適潮流計算、ユニットコミットメント、経済負荷配分など多様な解析が可能
- **MATLAB/GNU Octave互換**: MATLABとOctaveの両方で使用可能
- **拡張性**: ユーザーが独自の最適化手法や解析手法を組み込める

## 3. 主な機能

- **潮流計算 (Power Flow Analysis)**: Newton-Raphson法や直流潮流計算（DC Power Flow）をサポート
- **最適潮流計算 (Optimal Power Flow, OPF)**: 送電コスト最小化や電圧制御などの最適化が可能
- **ユニットコミットメント (Unit Commitment, UC)**: 発電機のスケジューリング問題の解析
- **経済負荷配分 (Economic Dispatch, ED)**: 燃料コストを最小化する発電出力の決定

## 4. 利用方法

### 4.1 インストール

MATPOWERは以下の公式サイトからダウンロード可能です。 [https://matpower.org/](https://matpower.org/)

### 4.2 基本的なコマンド

```matlab
% MATPOWERの起動
addpath('MATPOWERのインストールパス');

% 潮流計算の実行
results = runpf('case30');
printpf(results);

% 最適潮流計算の実行
results_opf = runopf('case30');
printpf(results_opf);
```

## 5. 応用例

- **電力市場のシミュレーション**
- **再生可能エネルギーの統合解析**
- **送電網の最適化**

## 6. まとめ

MATPOWERは、電力系統の解析や最適化に非常に有用なツールです。MATLABやOctaveを利用して、電力系統のモデルを簡単に構築し、多様な解析を行うことができます。