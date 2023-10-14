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
ProjectName = "0927"
# 翼型を保管しておき、コマンドファイルを出力するディレクトリのPath
Directory = r"C:\Users\ryota2002\Documents\libu"

# 翼関連
# 端、根の翼弦長(流れ方向)[mm]
RootChord = 1016
EndChord = 1016
# 端、根のねじり上げ(流れ方向)[°]
RootDelta = 0

EndDelta = 0
# 端、根の桁位置[%]
RootR = 37
EndR = 37
# 端、根の翼型のファイル名 datファイルを入れる
RootFoilName = "dae21.dat"
EndFoilName = "dae21.dat"
# リブ枚数
n = 3
# 何翼?
PlaneNumber = "4"
# 半リブあり?
use_half = True

# リブ以外の要素関連
# プランク厚さ[mm]
tp = 2.7
# ストリンガー断面の一辺[mm](翼弦垂直方向)
e = 5
# ストリンガー断面の１辺[mm](翼弦平行方向)
e1 = 5.5
# リブキャップ厚さ[mm]
t = 1
# 桁径[mm]	楕円の短軸方向
d = 89.75
# 桁径		楕円の長軸-短軸 円なら0
dd = 89.75 - d
# アセンブリ棒径[mm]
da = 30  # 元は30
# アセンブリ棒余白[mm]
h = 7
# 後縁材の前縁側の辺の長さ[mm]
ht = 8  # 元は8
# 前縁材があるか boolean
use_l = False
# 前縁材の端線、水平線,offset線の出力
use_la = False
# 前縁材と翼型の前縁のずれ[mm]
lo = 10
# 前縁材のoffset[mm]
offset_l = 1
# 三角肉抜き最小骨格幅[mm]
w_tri = 15
# 三角肉抜き端半径[mm]
r_tri = 10
# 前縁-肉抜き 長さ[%]
first_light_r = 10
# 丸肉抜き 最小骨格幅[mm]
w_circle = 15

# 位置関連
# プランク上開始位置[%]
rpu = 60
# プランク下開始位置[%] r plank downside
rpd = EndR - 100 * (d / 2 + 30) / EndChord
# ストリンガー下後縁側位置[%] r stringer downside trailing edge #半リブの切り取り線に依存
rsdt = rpd + 20
# ストリンガー前縁[mm] x stringer leading edge
xsl = 20 + e

# 設定値はあざみ野の翼を参考にしている
# ストリンガー位置翼上部[%]
stringerU1Rate = 4
stringerU2Rate = 10
stringerU4Rate = 20
stringerU5Rate = 40
stringerU3Rate = 57
# ストリンガー位置翼下部[%]
stringerD1Rate = 2
stringerD2Rate = 6
stringerD3Rate = rpd - 3

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

# import matplotlib.pyplot as pyplot
import scipy.interpolate as interp
import scipy.optimize as optimize
import sympy
import random

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
        ABVecForLineAD = ABVec_e * e1  # ABベクトルの長さをe1へ、これを回転させてADベクトルを作る
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


class ellipse:
    """
    中心座標C、長軸上の一点P、短軸と中心の距離b を保持するオブジェクト
    """

    def __init__(self, C, P, b):
        self.C = C
        self.P = P
        self.b = b


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


def to_numpy(vectors):
    """numpyで書かれた配列をvectorのリストに直して返す"""
    ret = numpy.zeros((len(vectors), 2))
    for i in range(len(vectors)):
        ret[i][0] = vectors[i].x
        ret[i][1] = vectors[i].y
    return ret


def relation(Ps, r, O):
    """
    半径r、中心Oの円とPsがかぶっていないとき"Separated"
    かぶっていてPsが下にある時"Downside"、上にある時"Upside"を返す
    """
    for P in Ps:
        if abs(O - P) > r:  # OP > rならPは円の外
            pass
        elif O.y > P.y:  # 円の中で、下のほうがかぶっているとき
            # print("距離が" + str(abs(O - P)))
            return "Downside"
        else:
            # print("距離が" + str(abs(O - P)))
            return "Upside"
    return "Separated"


def define_Oa(
    EndFoilPs,
    RootFoilPs,
    da,
    h,
    EndPipeO,
    RootPipeO,
    sharpness=0.1,
    StartO=vector(0, 0),
):
    """
    EndFoilPsでも、RootFoilPsでもh以上の余白を持ったアセンブリ棒穴(直径da)の中心のうち最も後方にあるものを求める
    原点は桁の中心
    FoilPsはvectorのリスト
    First_Oは翼内に入っている必要がある。
    桁穴+StartOの地点から試行できる
    sharpnessの精度で返す
    """
    # 円の半径に使う
    r = da / 2 + h
    FoilPs = [EndFoilPs, RootFoilPs]
    Os = [EndPipeO, RootPipeO]

    ret = [0, 0]
    for i in range(2):
        dx = 2 * r  # 最初からdx=sharpnessでもいいが、収束を速くする
        current_O = Os[i] + StartO  # 前縁原点
        PastRelation = 0  # 過去の値を保持して比較する
        while True:
            Relation = relation(FoilPs[i], r, current_O)
            if Relation == "Separated":
                # 穴が翼型内ならdxだけ右にずらす
                current_O += vector(dx, 0)
            elif dx == 2 * r:
                # まだ精度が悪いとき、一つ前に戻して精度を上げる
                current_O -= vector(dx, 0)
                dx = sharpness
            elif (PastRelation != 0) and (Relation != PastRelation):
                # 上下に行ってもはみ出るとき
                ret[i] = current_O - Os[i]  # 原点を桁の中心に
                break
            elif Relation == "Downside":
                # 穴が翼型からはみ出たが、dxだけ上に行くとはみ出ないとき
                current_O += vector(0, dx)
                PastRelation = Relation
            elif Relation == "Upside":
                # dxだけ下に行くとはみ出ないとき
                current_O -= vector(0, dx)
                PastRelation = Relation
            else:
                print("define_Oaに不明なエラー")
        if (
            relation(FoilPs[1], r, ret[0] + Os[1]) == "Separated"
        ):  # ret[0]がRootでも中に入っていたら
            return ret[0]
    return ret[1]


# 関数、クラス定義おわり
# ------------------------------------------------------------------------------------------------
# メイン
sweep *= numpy.pi / 180

# 翼型読み込み
EndFoilData = to_vectors(
    numpy.loadtxt(EndFoilName, skiprows=1, dtype=float)
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
    numpy.loadtxt(RootFoilName, skiprows=1, dtype=float)
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


# アセンブリ棒用
# 翼型を上下別に関数に近似。 上下一緒に近似する方法は思いつかなかった。 fはfunctionの略
f_uEnd = inter(
    EndFoilDataU_x[::-1] * EndChord * cos(sweep), EndFoilDataU_y[::-1] * EndChord
)
f_dEnd = inter(EndFoilDataD_x * EndChord * cos(sweep), EndFoilDataD_y * EndChord)
f_uRoot = inter(
    RootFoilDataU_x[::-1] * RootChord * cos(sweep), RootFoilDataU_y[::-1] * RootChord
)
f_dRoot = inter(RootFoilDataD_x * RootChord * cos(sweep), RootFoilDataD_y * RootChord)
EndFoilPs = [vector(P.x * EndChord * cos(sweep), P.y * EndChord) for P in EndFoilData]
RootFoilPs = [
    vector(P.x * RootChord * cos(sweep), P.y * RootChord) for P in RootFoilData
]
# パイプの中心
EndPipeO = vector(
    EndR * EndChord / 100, f_uEnd(0.25 * EndChord) / 2 + f_dEnd(0.25 * EndChord) / 2
)
RootPipeO = vector(
    RootR * RootChord / 100,
    f_uRoot(0.25 * RootChord) / 2 + f_dRoot(0.25 * RootChord) / 2,
)
# アセンブリ棒の準備
Oa = define_Oa(
    EndFoilPs,
    RootFoilPs,
    da,
    h + t,
    EndPipeO,
    RootPipeO,
    StartO=vector(
        0.6 * EndChord, f_uEnd(0.6 * EndChord) / 2 + f_dEnd(0.6 * EndChord) / 2
    )
    - EndPipeO,
)

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
    s = numpy.linspace(0, 1, 150)
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

    # 中心線の関数、点のリスト
    s = numpy.linspace(0, x_d[-1], 50)  # 端で定義域を狭くするのは計算誤差でf_uの定義域を超えないため。
    f_camber = inter(s, (f_u(s) + f_d(s)) / 2)  # 上下の翼型の関数の平均であると近似 特に前縁付近は信用できない
    CamberPs = to_vectors2(s, f_camber(s))
    del s

    # 境目になるようなx座標を定義する
    x_plank_u = c * (rpu / 100) * cos(sweep)
    x_plank_d = c * (rpd / 100) * cos(sweep)
    x_stringer_u1 = c * (stringerU1Rate / 100) * cos(sweep)
    x_stringer_u2 = c * (stringerU2Rate / 100) * cos(sweep)
    x_stringer_u3 = c * (stringerU3Rate / 100) * cos(sweep)
    x_stringer_D1 = c * (stringerD1Rate / 100) * cos(sweep)
    x_stringer_D2 = c * (stringerD2Rate / 100) * cos(sweep)
    x_stringer_D3 = c * (stringerD3Rate / 100) * cos(sweep)
    x_stringer_dt = c * rsdt / 100 * cos(sweep)
    x_pipe = c * (RootR + (EndR - RootR) * r) / 100 * cos(sweep)
    x_25pc = c * cos(sweep) * 0.25

    # プランクの点のリストの出力
    PlankPs = offset(
        [FoilU[i] for i in range(len(FoilU) - 2) if FoilU[i + 2].x <= x_plank_u]
        + [FoilU[-2], FoilD[0], FoilD[1]]
        + [FoilD[i] for i in range(2, len(FoilD)) if FoilD[i - 2].x <= x_plank_d],
        tp,
        0,
    )
    PlankPsU = [P for P in PlankPs if P.y >= 0][::-1]
    PlankPsD = [P for P in PlankPs if P.y <= 0]
    # リブキャップの点のリストの出力 プランクの開始点より後縁側であることを利用
    RibCap_uPs = offset(
        [FoilU[i] for i in range(2, len(FoilU)) if FoilU[i - 2].x >= x_plank_u], t, 0
    )
    RibCap_dPs = offset(
        [FoilD[i] for i in range(len(FoilD) - 2) if FoilD[i + 2].x >= x_plank_d], t, 0
    )

    # ストリンガーの出力
    StringerU = stringer(div_P(PlankPsU[0], PlankPs[1], x_plank_u, 0), PlankPs[1], e)
    StringerDL = stringer(
        div_P(PlankPs[-1], PlankPs[-2], x_plank_d, 0), PlankPs[-2], e, R=True
    )  # leading edge

    # プランク線pipe.bの端を切り取る
    del PlankPs[0], PlankPs[-1]
    PlankPs = [StringerU.A] + PlankPs + [StringerDL.A]  # 端点をストリンガーの頂点と一致させる。

    # 桁穴の出力 y座標は25%のcamber位置で固定
    delta = RootDelta + (EndDelta - RootDelta) * r
    RibAngle = math.atan(tan((alpha + delta) * numpy.pi / 180) * cos(sweep))
    Pipe_C = vector(x_pipe, f_camber(x_pipe))
    Pipe = ellipse(
        Pipe_C, Pipe_C + vector(0, 1).rotate(RibAngle, "radian") * (d + dd) / 2, d / 2
    )

    # 水平、鉛直線関連
    hlineP1 = Pipe_C + vector(0, 1).rotate(RibAngle, "radian").i * c * 0.35
    hlineP2 = Pipe_C - vector(0, 1).rotate(RibAngle, "radian").i * c * 0.35
    vlineP1 = Pipe_C + vector(1, 0).rotate(RibAngle, "radian").i * c * 0.07
    vlineP2 = Pipe_C - vector(1, 0).rotate(RibAngle, "radian").i * c * 0.07

    # アセンブリ棒穴の出力
    Assembly = circle(da / 2, Oa + Pipe_C)

    # 後縁材の出力
    # 後縁材の上側の一点を求める。下をoffsetした関数と上の関数の交点とする。
    FoilD_offsetPs = offset(FoilD[5:], ht, 0)
    s = numpy.linspace(FoilD_offsetPs[0].x, FoilD_offsetPs[-1].x)
    f_dOffset = inter(to_numpy_x(FoilD_offsetPs), to_numpy_y(FoilD_offsetPs))
    TrailU_x = optimize.newton(lambda x: f_dOffset(x) - f_u(x), c * cos(sweep) * 0.95)
    TrailU = vector(TrailU_x, f_u(TrailU_x))
    # 後縁材の下側の一点を求める。 TrailUを挟む点を求め、これら三点でoffsetする。
    EdgeTrailU = [
        FoilD_offsetPs[i]
        for i in range(1, len(FoilD_offsetPs))
        if FoilD_offsetPs[i - 1].x <= TrailU.x
    ][
        -2:
    ]  # TrailUを挟む点
    TrailD = offset([EdgeTrailU[0], TrailU, EdgeTrailU[1]], ht, 1)[0]
    del s

    # 前縁材出力
    # Relation関数を用いて前縁材の点を出力する LeadDは最初から最前縁の点は含んでいない
    if use_l:
        LeadU = [P + vector(lo, 0) for P in FoilU if P.x < x_pipe]
        LeadD = [
            P + vector(lo, 0) for P in FoilD[1:] if P.x < c * cos(sweep) * rpd / 100
        ]
        # プランクの上、下側を関数として扱えるようにする
        f_pu = inter(to_numpy_x(PlankPsU), to_numpy_y(PlankPsU))
        f_pd = inter(to_numpy_x(PlankPsD), to_numpy_y(PlankPsD))
        # 前縁材の上、下側を関数として扱えるようにする
        f_lu = inter(to_numpy_x(LeadU[::-1]), to_numpy_y(LeadU[::-1]))
        f_ld = inter(to_numpy_x(LeadD), to_numpy_y(LeadD))
        # 前縁材上下の後縁側のx座標
        x_pu = optimize.newton(lambda x: f_lu(x) - f_pu(x), 0.1 * c)
        x_pd = optimize.newton(lambda x: f_ld(x) - f_pd(x), lo + tp)
        LeadU = [vector(x_pu, f_lu(x_pu))] + [P for P in LeadU if P.x < x_pu]
        LeadD = [P for P in LeadD if P.x < x_pd] + [vector(x_pd, f_ld(x_pd))]
        LeadPs = LeadU + LeadD
        # 前縁材端の線の端点
        LeadEndP2U = (
            LeadPs[0]
            + (
                (vector(LeadPs[0].x + tp, f_pu(LeadPs[0].x + tp)) - LeadPs[0])
                / abs(vector(LeadPs[0].x + tp, f_pu(LeadPs[0].x + tp)) - LeadPs[0])
            ).i
            * tp
        )
        LeadEndP2D = (
            LeadPs[-1]
            + (
                (vector(LeadPs[-1].x - tp, f_pd(LeadPs[-1].x - tp)) - LeadPs[-1])
                / abs(vector(LeadPs[-1].x - tp, f_pd(LeadPs[-1].x - tp)) - LeadPs[-1])
            ).i
            * tp
        )
    ###トラス肉抜きを行うための部分
    # 出力したいトラスの外周厚み
    gaishuuAtumi = 0.20
    # 出力したいトラスの斜材厚み
    torasuuAtumi = 5

    # 各基準点を保持する配列
    basePointArrayLists_fixed = [[(0.05, 0.20), (0.10, 0.20)]]

    # arrayの形で渡された点の集まりから、第一引数のｘに最も近い座標を返すための関数
    def findNearestPointBasedOnX(x, arrayOfSearch):
        return [
            arrayOfSearch[i]
            for i in range(1, len(arrayOfSearch))
            if arrayOfSearch[i - 1].x <= x
        ][-2:]

    # 翼弦のx座標の％、その翼の厚みに対しての移動％を渡された際に移動後のy座標を返す関数
    def calucaulateYokuactuu(yokuGennRate_x, yokugennRate_y):
        x = c * yokuGennRate_x
        y_up = f_u(x)
        y_down = f_d(x)
        if yokugennRate_y < 0:
            return (y_up - y_down) * yokugennRate_y + y_up
        elif yokugennRate_y > 0:
            return (y_up - y_down) * yokugennRate_y + y_down

    # 翼弦のx座標の％に対応する翼の厚みを返す関数
    def calucaulateYokuaAtumi(yokuGennRate_x):
        x = yokuGennRate_x
        y_up = f_u(x)
        y_down = f_d(x)
        return y_up - y_down

    # 2点を決めることで直線の方程式を返すような関数
    def makeLinearEquation(x1, y1, x2, y2):
        line = {}
        # y = mx + n
        line["m"] = (y1 - y2) / (x1 - x2)
        line["n"] = y1 - (line["m"] * x1)
        return line

    # 点と直線の距離
    def Calc_distance(a, b, c, point_x, point_y):  # 直線ax+by+c=0 点(x0,y0)
        numer = abs(a * point_x + b * point_y + c)  # 分子
        denom = math.sqrt(pow(a, 2) + pow(b, 2))  # 分母
        return numer / denom  # 計算結果

    # 翼の外周の厚みを返す関数
    def sannkakuNikunuki(basePointArrayInput, angle):
        # basePointArrayに含まれるトラス情報を並び帰る
        if basePointArrayInput[0][0] > basePointArrayInput[1][0]:
            basePointArray = [
                (basePointArrayInput[1][0], basePointArrayInput[1][1]),
                (basePointArrayInput[0][0], basePointArrayInput[0][1]),
            ]
        else:
            basePointArray = basePointArrayInput
        # 各座標を計算する
        basePoint1_x = c * basePointArray[0][0]
        basePoint1_y = calucaulateYokuactuu(basePointArray[0][0], basePointArray[0][1])
        basePoint2_x = c * basePointArray[1][0]
        basePoint2_y = calucaulateYokuactuu(basePointArray[1][0], basePointArray[1][1])
        basePointVector12 = vector(
            basePoint2_x - basePoint1_x, basePoint2_y - basePoint1_y
        )
        basepointVector13 = basePointVector12.rotate(angle)
        basePoint3Vector = basepointVector13 + vector(basePoint1_x, basePoint1_y)
        basePoint3_x = basePoint3Vector.x
        basePoint3_y = basePoint3Vector.y
        # base3,base2を結ぶ直線の方程式を求める
        line23 = makeLinearEquation(
            basePoint2_x, basePoint2_y, basePoint3_x, basePoint3_y
        )
        # トラスの外周幅を計算
        gaishuugosa = 0
        if basePointArray[0][1] > 0:
            diff = basePoint3_y - f_u(basePoint3_x)
            gaishuugosa = abs(diff / calucaulateYokuaAtumi(basePoint3_x))
        elif basePointArray[0][1] <= 0:
            diff = f_d(basePoint3_x) - basePoint3_y
            gaishuugosa = abs(diff / calucaulateYokuaAtumi(basePoint3_x))
        # 翼のトラス斜め材の太さを計算
        # 1つ前の三角形の点を利用して計算を進める
        torasuBefore_x = basePointArrayLists_fixed[::-1][0][1][0] * c
        torasuBefore_y = calucaulateYokuactuu(
            basePointArrayLists_fixed[::-1][0][1][0],
            basePointArrayLists_fixed[::-1][0][1][1],
        )
        lengthOfTorasu = Calc_distance(
            line23["m"], -1, line23["n"], torasuBefore_x, torasuBefore_y
        )
        torasuuNanamezaiGosa = abs(lengthOfTorasu - torasuuAtumi)
        ##設定値からのずれを評価
        gosa = abs(gaishuugosa + torasuuNanamezaiGosa)
        if gosa < minimumGosa:
            return [True, gosa, basePointArray]
        else:
            return [False]

    timesOfKaiseki = 100000
    # ここからトラス構造の探索が行われる
    saerchPointArrayLists = []
    counter = 0
    # これまでの最小となる誤差を入力
    minimumGosa = float("inf")
    minimumBasePointarray = []
    while counter < timesOfKaiseki:
        counter += 1
        saerchPointArrayLists.append(
            [(random.random(), gaishuuAtumi), (random.random(), gaishuuAtumi)]
        )
    for basePointArray in saerchPointArrayLists:
        if basePointArray[0][1] > 0:
            calucurateGosa = sannkakuNikunuki(basePointArray, 60)
            if calucurateGosa[0] == True:
                minimumGosa = calucurateGosa[1]
                minimumBasePointarray = calucurateGosa[2]

        elif basePointArray[0][1] <= 0:
            calucurateGosa = sannkakuNikunuki(basePointArray, -60)
            if calucurateGosa[0] == True:
                minimumGosa = calucurateGosa[1]
                minimumBasePointarray = calucurateGosa[2]
    basePointArrayLists_fixed.append(minimumBasePointarray)
    print(basePointArrayLists_fixed, "findAnswer")

    ##各トラス座標に対して配置の最適化を行うロジックは完成
    ##ここから、複数個数のトラス位置を計算するためのロジックを作るを作る

    # ここに出力を行うトラスの個数を打ち込む
    torasuuumber = 5
    # 各トラスの解析を行う際のループ数を入力
    timesOfKaiseki = 10000
    # ここからトラス構造の探索が行われる
    saerchPointArrayLists = []
    counter = 0
    # これまでの最小となる誤差を保持
    minimumGosa = float("inf")
    minimumBasePointarray = []
    while counter < timesOfKaiseki:
        counter += 1
        saerchPointArrayLists.append(
            [(random.random(), gaishuuAtumi), (random.random(), gaishuuAtumi)]
        )
    for basePointArray in saerchPointArrayLists:
        if basePointArray[0][1] > 0:
            calucurateGosa = sannkakuNikunuki(basePointArray, 60)
            if calucurateGosa[0] == True:
                minimumGosa = calucurateGosa[1]
                minimumBasePointarray = calucurateGosa[2]

        elif basePointArray[0][1] <= 0:
            calucurateGosa = sannkakuNikunuki(basePointArray, -60)
            if calucurateGosa[0] == True:
                minimumGosa = calucurateGosa[1]
                minimumBasePointarray = calucurateGosa[2]
    basePointArrayLists_fixed.append(minimumBasePointarray)
    print(basePointArrayLists_fixed, "findAnswer")
