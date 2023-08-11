import itertools
import math
import random
import sys
from scipy import integrate
import numpy as np
import matplotlib.pyplot as plt
import time

# グローバル変数
N = int(input("ストリンガーの本数を入力してください"))  # ストリンガーの本数
L = int(input("解析したい長さを入力してください"))  # 解析したい梁の長さを入力してください
SEED = 100000  # 乱数の種
R = 1  # 実験の繰り返し回数　何ループさせるか？
E = 100  # たわみ量計算
I = 100  # たわみ量計算


# 解を求める
def solvekp(p, nlimit, N):
    minimumTawami = float("inf")  # 合計たわみの最小値
    bestep = [0 for _ in range(N)]  # 合計たわみの最小値の時の乱数Pの組
    display_P = None  # ストリンガーの配置の初期化
    counter = 0
    while counter < nlimit + 1:
        counter += 1
        p = restp(N)  # 乱数によるストリンガーの配置
        # 各区間のたわみを保持するリスト(2次元配列[[区間１の１mm刻みのたわみ量][][][]])
        tawamiList = calculationOfTawami(p)
        tawamiList1D = list(itertools.chain.from_iterable(tawamiList))

        tawami = sum(tawamiList1D)
        if tawami < minimumTawami:  # 最良解を更新
            minimumTawami = tawami
            bestep = p[:]
            display_P = sorted(bestep)
    return display_P


# 荷重の分布する関数
def fx(x):
    return 1  # ここに関数を入力


# 集中荷重をかけるx座標を求めるための関数
def fx2(x):
    return fx(x) * x


# 乱数を用いたストリンガーの配置
def restp(N):
    p = []
    for _ in range(N - 2):
        pAddition = random.random()  # 0~1の値の中で乱数の生成
        p.append(pAddition)
    p.append(0)
    p.append(1)
    p = sorted(p)  # 乱数を小さい順に並べ変える
    return p


# 分割区間内の任意の位置でたわみ量を表す関数を作る
# 第一引数は荷重の掛かる点の座標、第２引数へxが小さい側の支点座標、第3引数へｘが大きい側の始点座標、第４引数へ区間の長さ、第五引数へ荷重
def tawamiForPartX(weightPointInPart, supportPointmin_x, supportPointmax_x, weight):
    # 各区間の荷重よりもｘ座標が小さい側の点の集合
    x_min = np.arange(supportPointmin_x, weightPointInPart, 1)
    # 各区間の荷重よりもｘ座標が大きい側の点の集合
    x_max = np.arange(weightPointInPart, supportPointmax_x, 1)
    # x座標が小さい側のたわみ量計算 各点におけるたわみの値をリストで保持
    tawami_x_min = []
    # x座標が大きい側のたわみ量計算 各点におけるたわみの値をリストで保持
    tawami_x_max = []

    ##計算に必要な定数を作る (L1:荷重点からxが小さい側の支点座標の距離、区間長さ＝L1＋L2)
    L1 = weightPointInPart - supportPointmin_x
    L2 = supportPointmax_x - weightPointInPart
    L = supportPointmax_x - supportPointmin_x

    for i in range(len(x_min)):
        x = x_min[i] - supportPointmin_x
        tawami_x_min.append(
            weight * L2 * x * (2 * L1 * L - L1 * L1 - x**2) / 6 / E / I / L
        )

    for j in range(len(x_max)):
        x = x_max[j] - supportPointmin_x
        tawami_x_max.append(
            weight * L1 * (L - x) * (2 * L * x - L1 * L1 - x**2) / 6 / E / I / L
        )
    return np.hstack((tawami_x_min, tawami_x_max))


# たわみ量の計算
def calculationOfTawami(p):
    # 各分割点を保持するリスト
    stringerPoint = [L * p[i] for i in range(len(p))]
    # 各分割区間の長さを計算
    stringerPartLength = [L * (p[i] - p[i - 1]) for i in range(1, len(p))]
    # 各分割区間にかかる荷重を計算
    stringerPartWeight = []
    for i in range(1, len(p)):
        stringerPartWeightAdding = integrate.quad(
            fx, stringerPoint[i], stringerPoint[i - 1]
        )[0]
        stringerWeightAbsolute = abs(stringerPartWeightAdding)
        stringerPartWeight.append(stringerWeightAbsolute)

    # 各分割区間で集中荷重をかけるx座標を求める
    weight_point_x = [
        integrate.quad(fx2, stringerPoint[i - 1], stringerPoint[i])[0]
        / integrate.quad(fx, stringerPoint[i - 1], stringerPoint[i])[0]
        for i in range(1, len(p))
    ]
    ## 各分割区間のたわみ量を計算
    # 各区間のたわみ量を保持するリスト
    tawamiForEachPart = []
    for i in range(0, len(p) - 1):
        tawamiPart = tawamiForPartX(
            weight_point_x[i],
            stringerPoint[i],
            stringerPoint[i + 1],
            stringerPartWeight[i],
        )
        tawamiForEachPart.append(tawamiPart)
    return tawamiForEachPart


p = []
# 試行回数の入力
nlimit = int(input("試行回数（乱数の生成個数）を入力してください:"))
# 乱数の初期化
random.seed(SEED)

# 実験の繰り返し
for _ in range(R):
    solvekp(p, nlimit, N)
# ここまでは、全体に対する解析を行う


# ここからは、探索を行う範囲を絞りながら解の精度を上げる
# 再探索の際の乱数の発生回数
nlimit = int(input("試行回数（乱数の生成個数）を入力してください（再検索用):"))
# 再検索の際の乱数の核
SEEDFIRST = int(input("再探索時の乱数の核を代入して下さい"))
# 再検索の絞り込み回数を入力
newR = int(input("再検索のための絞り込み回数を入力してださい"))
# 1回目の再検索での探索幅
rangeRateFirst = float(input("1回目の再検索を行う幅(10%の場合0.10の形で入力)を入力して下さい"))
# 検索幅の狭め方(0から１以上の値を入力、ここで入力した幅が検索幅の公比になる等比数列へ)
rangeShrinkRate = float(input("検索幅の狭め方(0から１以上の値を入力、ここで入力した幅が検索幅の公比になる等比数列へ)"))


# 値を一時的に保存するための定数
bestPForAgainSearch = []  # 一つ前の狭められた範囲での最適なストリンガー位置
SEED = 0  # 1つ前の乱数の核を保持
rateLength = 0  # 1つ前のループの解析した幅を保持


##上の最適化計算で得られた解の近傍を探索するための関数 第一引数：再探索を行う解　第２引数：範囲（+-OO%
def evaluateNearTheAnswer(answer, rate):
    # del answer[0]
    # del answer[-1]

    for k in range(nlimit):
        p = []
        bestPForAgainSearch = []
        bsettawamiForAgainSearch = float("inf")
        for _ in range(N - 2):
            pAddition = random.random()  # 0~1の値の中で乱数の生成
            p.append(pAddition)
        # 各ストリンガーの移動幅を保持する
        lengthOfMove = [random.choice((-1, 1)) * rate * p[i] for i in range(len(p))]
        lengthOfMove.insert(0, 0)
        lengthOfMove.append(0)

        # 探索を行うストリンガ位置を保持（placeOfStringer）([0,0.10,0.37]みたいな形で保持される)
        placeOfStringer = [answer[i] + lengthOfMove[i] for i in range(len(answer))]
        placeOfStringer.append(1)
        placeOfStringer.insert(0, 0)
        tawamiList_ForAgainSearch = calculationOfTawami(placeOfStringer)
        tawamiList_ForAgainSearch_1D = list(
            itertools.chain.from_iterable(tawamiList_ForAgainSearch)
        )
        tawmiForAgainSearch = sum(tawamiList_ForAgainSearch_1D)

        # 最良解の更新
        if tawmiForAgainSearch > bsettawamiForAgainSearch:
            bsettawamiForAgainSearch = tawmiForAgainSearch
            bestPForAgainSearch = sorted(placeOfStringer)
    return bestPForAgainSearch


for k in range(newR):
    if k == 0:
        SEED = SEEDFIRST
        random.seed(SEED)
        p = restp(N)
        rateLength = rangeRateFirst
        bestPForAgainSearch = solvekp(p, nlimit, N)
    else:
        SEED = SEED + 74  # 乱数の核を更新
        rateLength = rangeShrinkRate * rateLength  # 探索幅の更新
        evaluateNearTheAnswer(bestPForAgainSearch, rateLength)
    print("最適な配置は", bestPForAgainSearch, "探索幅", rateLength)
