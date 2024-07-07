# -------------------------------------------------------------------------
# 使いかた
# 下記Directoryに翼型をすべていれておく。必要に応じて変える。
# 翼型は 後縁->上->前縁->下->後縁 の順になっていることを確認
# 翼弦長などの定義に注意
# 三角肉抜きが変な形になるときは、w_triやr_triを小さく調整するとよい
# ただし、小さくしすぎるとリブが折れるかもしれないので気を付ける

# 使いかたおわり
# ----------------------------------------------------------------------------------------
# 設定

# ファイル関連
# 出力するテキストファイルの名前。拡張子は不要
ProjectName = "垂直下側"
# 翼型を保管しておき、コマンドファイルを出2024詩集版力するディレクトリのPath
Directory = r"C:\Users\ryota2002\Documents\2024確定版\リブ図面"

# 翼関連
# 端、根の翼弦長(流れ方向)[mm]
RootChord = 984
EndChord = 870
# 端、根のねじり上げ(流れ方向)[°]
RootDelta = 0
EndDelta = 0
# 端、根の桁位置[%]
RootR = 25
EndR = 25
# 端、根の翼型のファイル名 datファイルを入れる
FoilName = "DAE-41.dat"
# リブ枚数(1つの翼に立てる枚数)
n = 5
# 分割してリブを出力
isUseBunkatuShuturyoku = False
startRib = 11  # 何枚目から出力を行うか
endRib = 13  # 何枚目まで出力するか
# 何翼?
PlaneNumber = "0"
# 半リブあり?
use_half = False

# 上反角を付けるために桁をy軸方向へ移動させるか？
use_JouhannkakuChousei = False
# 各リブのy軸の移動量をxに対応する翼厚みに対する％でリスト形式で渡す
y_chousei = [0, 1, 2]

# リブ以外の要素関連
# プランク厚さ[mm]
tp = 3
# ストリンガー断面の一辺[mm](翼弦垂直方向)
e = 5
# ストリンガー断面の１辺[mm](翼弦平行方向)
e1 = 5.5
# リブキャップ厚さ[mm]
t = 0.3


##リブガキの際の分割数を指定
# 基本は200、数が大きいほど精密なリブが書けるが大きくし過ぎるとエラー
bunnkatyu = 100


# 機体諸元
# 0翼取り付け角[°]
alpha = 0
# 後退角(リブ厚みの修正用)[°]
sweep = 0

# 設定おわり
# ------------------------------------------------------------------------------------------
# 準備

import os
import numpy

import matplotlib.pyplot as plt
import scipy.interpolate as interp
import scipy.optimize as optimize
import sympy

inter = interp.Akima1DInterpolator
import math

sin, cos, tan, atan2 = (math.sin, math.cos, math.tan, math.atan2)
from scipy.optimize import fsolve
import warnings
import csv
import time

os.chdir(Directory)  # ディレクトリ移動

# ライブラリおわり
# ----------------------------------------------------------------------------------------
# 関数、クラス定義


class vector:
    """(x,y,z)の点、ベクトル
    z=0 がデフォルト
    v + w, v - w, v*k, v/k は通常の定義済み　ただし*、/の前はベクトル
    v @ w　は内積、v * wは外積
    abs(v)　はvの大きさ
    .iで反時計回りに回転
    """

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        if self.z == 0:
            return "({}, {})".format(self.x, self.y)
        else:
            return "({}, {}, {})".format(self.x, self.y, self.z)

    def __repr__(self):
        if self.z == 0:
            return "vector({}, {})".format(self.x, self.y)
        else:
            return "vector({}, {}, {})".format(self.x, self.y, self.z)

    def __add__(self, other):
        return vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, k):  # 入力により実数倍か外積を返す
        if type(self) == vector and type(k) != vector:
            return vector(self.x * k, self.y * k, self.z * k)
        elif type(self) == vector and type(k) == vector:
            return vector(
                self.y * k.z - self.z * k.y,
                -self.x * k.z + self.z * k.x,
                self.x * k.y - self.y * k.x,
            )

    def __matmul__(self, other):  # 内積
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __truediv__(self, k):
        return vector(self.x / k, self.y / k, self.z / k)

    def __abs__(self):
        return (self @ self) ** (1 / 2)

    @property
    def i(self):
        return vector(-self.y, self.x)

    def rotate(self, angle, unit="degree"):
        """
        ベクトルvを反時計回りにangleだけ回転させる
        angleの単位はunitを"degree"か"radian"にして指定
        """
        if unit == "degree":
            angle *= numpy.pi / 180
        elif unit == "radian":
            pass
        else:
            print("単位が不正です")
            raise ValueError("単位が不正です")
        return vector(
            self.x * cos(angle) - self.y * sin(angle),
            self.x * sin(angle) + self.y * cos(angle),
        )


class stringer:
    """
    ストリンガーを図のように定義できる。これをそのまま用いてコマンドも出力できる。
    Aを一点に持つ。Pで方向を決める。eは一辺。RがFalseならそのまま、Trueなら反転。
    A、Pはvectorオブジェクト
    .A、.B、.C、.Dがそれぞれの点
    """

    def __init__(self, A, P, e, R=False):
        self.A = A
        self.P = P
        self.e = e
        self.R = R

    @property
    def AB(self):
        return (self.P - self.A) / abs(self.P - self.A) * self.e  # ABベクトル

    @property
    def B(self):
        return self.A + self.AB

    @property
    def D(self):
        ABVec_e = self.AB / abs(self.AB)
        ABVecForLineAD = (
            ABVec_e * e1
        )  # ABベクトルの長さをe1へ、これを回転させてADベクトルを作る
        if not self.R:
            return self.A + ABVecForLineAD.i
        else:
            return self.A - ABVecForLineAD.i

    @property
    def C(self):
        return self.B + self.D - self.A


class circle:
    """
    円の半径と中心を保持するオブジェクト
    """

    def __init__(self, r, O):
        self.r = r
        self.O = O


def div_P(P1, P2, known, index):
    """
    P1,P2を結ぶ直線上にP3があってP3.index=knownがわかっているとき、その点をvectorとして返す。
    index=0のときx、1のときy
    """
    if index == 0:
        return div_P2(P1, P2, (known - P1.x) / (P2.x - P1.x))
    if index == 1:
        return div_P2(P1, P2, (known - P1.y) / (P2.y - P1.y))


def div_P2(P1, P2, ratio):
    """
    P1,P2をP1P2:P1P3=1:ratioに内分、外分する点P3の座標をvectorとして返す。
    """
    return P1 + (P2 - P1) * ratio


def offset(l, t, updown, end=0):
    """
    l=[vector,...]をtだけずらした点のリストを出力。
    endが0のとき、最初、最後の点は除かれる。つまり、出力は元のリストより要素が2つすくない。
    endが1のときは全ての点が残る。端の点は端から2番目の点との傾きを使う。
    点の向きに対して左にずらすときupdown=0、右にずらすとき1。
    """
    ret = []
    i = 1
    while i + 1 < len(l):
        ret.append(
            (l[i + 1] - l[i - 1]).i / abs(l[i + 1] - l[i - 1]) * t * (-1) ** updown
            + l[i]
        )
        i += 1
    if end == 1:
        ret = (
            [(l[1] - l[0]).i / abs(l[1] - l[0]) * t * (-1) ** updown + l[0]]
            + ret
            + [(l[-1] - l[-2]).i / abs(l[-1] - l[-2]) * t * (-1) ** updown + l[-1]]
        )
    return ret


def to_vectors(array):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    return [vector(P[0], P[1]) for P in array]


def to_vectors2(numpy_x, numpy_y):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = [vector(numpy_x[i], numpy_y[i]) for i in range(len(numpy_x))]
    return ret


def to_numpy_x(vectors):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = numpy.zeros(len(vectors))
    for i in range(len(vectors)):
        ret[i] = vectors[i].x
    return ret


def to_numpy_y(vectors):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = numpy.zeros(len(vectors))
    for i in range(len(vectors)):
        ret[i] = vectors[i].y
    return ret


# 関数、クラス定義おわり
# ------------------------------------------------------------------------------------------------
# メイン
sweep *= numpy.pi / 180

# 翼型読み込み
EndFoilData = to_vectors(
    numpy.loadtxt(FoilName, skiprows=1, dtype=float)
)  # 上下で分けるためにベクトルに変換 1行目は翼型名なのでスキップ
# 端の上側だけの点(無次元)                           ↓上側ではx座標が減少することを利用
EndFoilDataU = [
    EndFoilData[i]
    for i in range(len(EndFoilData) - 1)
    if EndFoilData[i].x - EndFoilData[i + 1].x >= 0
] + [vector(0, 0)]
EndFoilDataU_x = to_numpy_x(EndFoilDataU)  # 上側のx座標(無次元)
EndFoilDataU_y = to_numpy_y(EndFoilDataU)  # 上側のy座標(無次元)
# 端の下側
EndFoilDataD = [vector(0, 0)] + [
    EndFoilData[i]
    for i in range(1, len(EndFoilData))
    if EndFoilData[i].x - EndFoilData[i - 1].x >= 0
]
EndFoilDataD_x = to_numpy_x(EndFoilDataD)  # 下側のx座標(無次元)
EndFoilDataD_y = to_numpy_y(EndFoilDataD)  # 下側のy座標(無次元)

RootFoilData = to_vectors(
    numpy.loadtxt(FoilName, skiprows=1, dtype=float)
)  # 上下で分けるためにベクトルに変換
# 根の上側
RootFoilDataU = [
    RootFoilData[i]
    for i in range(len(RootFoilData) - 1)
    if RootFoilData[i].x - RootFoilData[i + 1].x >= 0
] + [vector(0, 0)]
RootFoilDataU_x = to_numpy_x(RootFoilDataU)  # 上側のx座標(無次元)
RootFoilDataU_y = to_numpy_y(RootFoilDataU)  # 上側のy座標(無次元)
# 根の下側
RootFoilDataD = [vector(0, 0)] + [
    RootFoilData[i]
    for i in range(1, len(RootFoilData))
    if RootFoilData[i].x - RootFoilData[i - 1].x >= 0
]
RootFoilDataD_x = to_numpy_x(RootFoilDataD)  # 下側のx座標(無次元)
RootFoilDataD_y = to_numpy_y(RootFoilDataD)  # 下側のy座標(無次元)


file = open(f"{ProjectName}.txt", "w")

file.write("texted\n1\n")  # textをコマンドで入力できるように設定
file.write("-lweight\n0.001\n")  # 線の太さ設定

O = vector(0, 0)  # それぞれのリブの前縁のy座標
y_u, y_d = [], []  # 定義前に使うと誤解されないように
for k in range(1, n + 1):  # range(1,n+1):				 	#根から k 枚目のリブ
    # y座標の設定 かぶらないようにするため。1cmの隙間もあける
    if k > 1:  # k=1のときO=(0,0)にしている
        O.y -= numpy.max(y_u) - numpy.min(y_d) + 150

    # 翼型の点のリストの出力。 上下の翼型を関数として作成。
    # 混ぜる割合。　根で0、端で1。
    r = (k - 1) / (n - 1)
    # 翼弦 流れ方向
    c = RootChord + (EndChord - RootChord) * r
    # 翼型を上下別に関数に近似。 上下一緒に近似する方法は思いつかなかった。 fはfunctionの略
    f_uEnd = inter(EndFoilDataU_x[::-1] * c * cos(sweep), EndFoilDataU_y[::-1] * c)
    f_dEnd = inter(EndFoilDataD_x * c * cos(sweep), EndFoilDataD_y * c)
    f_uRoot = inter(RootFoilDataU_x[::-1] * c * cos(sweep), RootFoilDataU_y[::-1] * c)
    f_dRoot = inter(RootFoilDataD_x * c * cos(sweep), RootFoilDataD_y * c)

    # x座標の列を端と同じにする
    s = numpy.linspace(0, 1, bunnkatyu)
    x_d = numpy.delete(
        numpy.cos(numpy.pi * (s - 1) / 2) ** 2 * c * cos(sweep), 1
    )  # 再前縁から2番目の点があると不安定になることを防ぐ
    # 端点は正確に
    x_d[0] = 0
    x_d[-1] = c * cos(sweep)
    # x_uは点の向きと同じ(降順)
    x_u = x_d[::-1]

    # 翼型の混合
    y_u = f_uRoot(x_u) + (f_uEnd(x_u) - f_uRoot(x_u)) * r
    y_d = f_dRoot(x_d) + (f_dEnd(x_d) - f_dRoot(x_d)) * r

    # 翼型をベクトルのリストにする
    FoilU = to_vectors2(x_u, y_u)
    FoilD = to_vectors2(x_d, y_d)
    FoilPs = FoilU + FoilD[1:]  # FoilDは(0,0)を取り除く
    # 上下の翼型を関数として扱えるようにする
    f_u = inter(x_u[::-1], y_u[::-1])
    f_d = inter(x_d, y_d)
    del s

    ##リブ書きプログラムで補完した曲線を書く
    s = numpy.linspace(0, x_d[-1], 1000)
    x_ribuData = s
    y_ribuData_u = f_u(s)
    y_ribuData_d = f_d(s)

    ##Datファイルの中身をプロットする
    x_u = EndFoilDataU_x[::-1] * c * cos(sweep)
    y_u = EndFoilDataU_y[::-1] * c
    x_d = EndFoilDataD_x * c * cos(sweep)
    y_d = EndFoilDataD_y * c

    # グラフの描写
    plt.plot(
        x_ribuData, y_ribuData_u, "o", label="ribuProgram", color="r", markersize=0.10
    )
    plt.plot(
        x_ribuData, y_ribuData_d, "o", label="ribuProgram", color="r", markersize=0.10
    )
    plt.plot(x_u, y_u, "o", label="datファイル", color="b", markersize=0.80)
    plt.plot(x_d, y_d, "o", label="datファイル", color="b", markersize=0.80)
    plt.title("DatFileData vs ribuProgram")  # タイトル
    plt.xlabel("x-axis(mm)")  # x軸のラベル
    plt.ylabel("y-axis(mm)")  # y軸のラベル
    plt.grid(True)  # gridの表示
    plt.show()
