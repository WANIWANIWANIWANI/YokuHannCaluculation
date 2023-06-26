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
ProjectName = "0626testPlankTann"
# 翼型を保管しておき、コマンドファイルを出力するディレクトリのPath
Directory = r"C:\Users\ryota2002\Documents\libu"

# 翼関連
# 端、根の翼弦長(流れ方向)[mm]
RootChord = 1288
EndChord = 700
# 端、根のねじり上げ(流れ方向)[°]
RootDelta = 0

EndDelta = 0
# 端、根の桁位置[%]
RootR = 31
EndR = 31
# 端、根の翼型のファイル名 datファイルを入れる
RootFoilName = "NACA0013.dat"
EndFoilName = "NACA0013.dat"
# リブ枚数
n = 10
# 何翼?
PlaneNumber = "4"
# 半リブあり?
use_half = False

# リブ以外の要素関連
# プランク厚さ[mm]
tp = 2.7
# ストリンガー断面の一辺[mm]
e = 5
# リブキャップ厚さ[mm]
t = 1
# 桁径[mm]	楕円の短軸方向
d = 31.388
# 桁径		楕円の長軸-短軸 円なら0
dd = 31.388 - d


# 位置関連
# プランク下開始位置[%] r plank downside
rpd = EndR - 100 * (d / 2 + 30) / EndChord
# プランク上開始位置[%]
rpu = 60

# ストリンガー上面下面の最後縁位置
stringerU3Rate = 57
stringerD3Rate = rpd - 3

# プランク端補強開始位置(翼弦に対する％)
plankHokyouStartRate_U = stringerU3Rate

# プランク端補強終了位置（翼弦に対する％）
plankHokyouEndPoint_U = rpu + 4  # 値を小さくしすぎるとエラーになる

# プランク補強材の厚み(最大翼厚にたいする％で表示)
plankHokyouStringerPlusA = 3

# 出力時の余白設定
margin = 30
# 機体諸元
# 0翼取り付け角[°]
alpha = -6.5
# 後退角(リブ厚みの修正用)[°]
sweep = 0

# 設定おわり
# ------------------------------------------------------------------------------------------
# 準備

import os
import numpy
from numpy import linalg

# import matplotlib.pyplot as pyplot
import scipy.interpolate as interp
import scipy.optimize as optimize

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

    def toNormalArray(self):
        return [self.x, self.y]


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
        if not self.R:
            return self.A + self.AB.i
        else:
            return self.A - self.AB.i

    @property
    def C(self):
        return self.B + self.D - self.A


def spline(file, l, O=vector(0, 0)):
    """
    リストl=[vector,vector,...]のspline曲線を描くコマンドをfileに出力
    Oに原点を移して描ける
    """
    file.write("spline\nm\nf\nk\nc\n")  # spline設定
    for P in l:
        file.write("{},{}\n".format(P.x + O.x, P.y + O.y))
    file.write("\n")


def line(file, P1, P2, O=vector(0, 0)):
    """
    点P1,P2(vector)を結ぶ線分を描くコマンドをfileに出力
    """
    file.write(f"line\n{P1.x+O.x},{P1.y+O.y}\n{P2.x+O.x},{P2.y+O.y}\n\n")


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


def color(file, r, g, b):
    """
    r,g,bで次から出力するオブジェクトの色を変えるコマンドをfileに出力
    """
    file.write(f"-color\nt\n{r},{g},{b}\n")


def WriteText(file, O, text, height=20, angle=0):
    """
    fileにtextを入力するコマンドを出力
    Oから始める。フォントの高さはheight、angleは字の角度[°]
    """
    file.write(f"text\n{O.x},{O.y}\n{str(height)}\n{str(angle)}\n{text}\n\n")


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


def arrayRotate(x, inputArray):
    # x;反時計回りに考えた際の回転角度、array;回転を行いたい配列
    degree = numpy.deg2rad(x)
    rot = numpy.array([[cos(degree), -sin(degree)], [sin(degree), cos(degree)]])
    v = numpy.array(inputArray)
    w = numpy.dot(rot, v)
    return w


def WriteText(file, O, text, height=20, angle=0):
    """
    fileにtextを入力するコマンドを出力
    Oから始める。フォントの高さはheight、angleは字の角度[°]
    """
    file.write(f"text\n{O.x},{O.y}\n{str(height)}\n{str(angle)}\n{text}\n\n")


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

file = open(f"{ProjectName}.txt", "w")

file.write("texted\n1\n")  # textをコマンドで入力できるように設定
file.write("-lweight\n0.001\n")  # 線の太さ設定


y_u, y_d = [], []  # 定義前に使うと誤解されないように
for k in range(1, n + 1):  # range(1,n+1):				 	#根から k 枚目のリブ
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
    s = numpy.linspace(0, 1, 200)
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

    ### プランク端補強材の出力
    ### まず、境界となる座標を求める
    x_plankHokyouStartRatePosition_U = c * (plankHokyouStartRate_U / 100) * cos(sweep)
    x_plankHokyouEndPointPosition_U = c * (plankHokyouEndPoint_U / 100) * cos(sweep)
    x_plank_u = c * (rpu / 100) * cos(sweep)
    x_plank_d = c * (rpd / 100) * cos(sweep)

    ###AutoCad出力に必要な点の集合や起点を求める
    ## プランク上の点保持するリストを生成する
    PlankPs = offset(
        [FoilU[i] for i in range(len(FoilU) - 2) if FoilU[i + 2].x <= x_plank_u]
        + [FoilU[-2], FoilD[0], FoilD[1]]
        + [FoilD[i] for i in range(2, len(FoilD)) if FoilD[i - 2].x <= x_plank_d],
        tp,
        0,
    )

    ## 上面のプランク端補強のプランク上の点を保持
    planktannHokyouArrayOfPlank_u = [
        P for P in PlankPs if (P.y >= 0 and x_plankHokyouStartRatePosition_U <= P.x)
    ]
    ## 上面のプランク端補強のリブキャップ上の点を保持
    planktannHokyouArrayOfRibCap_u_1 = offset(
        [
            FoilU[i]
            for i in range(1, len(FoilU))
            if (FoilU[i].x <= x_plankHokyouEndPointPosition_U)
        ],
        t,
        0,
    )
    planktannHokyouArrayOfRibCap_u = [
        planktannHokyouArrayOfRibCap_u_1[i]
        for i in range(len(planktannHokyouArrayOfRibCap_u_1))
        if (planktannHokyouArrayOfRibCap_u_1[i].x >= x_plank_u)
    ]

    O = vector(0, 0)  # それぞれのリブの前縁のy座標
    # y座標の設定 かぶらないようにするため。1cmの隙間もあける
    O.y -= margin * k
    planktannHokyouArrayOfPlank_u_array = [
        planktannHokyouArrayOfPlank_u[i].toNormalArray()
        for i in range(len(planktannHokyouArrayOfPlank_u))
    ]
    planktannHokyouArrayOfPlank_u_array_x = [
        planktannHokyouArrayOfPlank_u_array[i][0]
        for i in range(len(planktannHokyouArrayOfPlank_u))
    ]
    print(planktannHokyouArrayOfPlank_u_array_x)
    O.x -= numpy.min(planktannHokyouArrayOfPlank_u_array_x) + 10

    ##lineの方向性を決めるための各ベクトル類を生成させる

    # vecU1について
    vec_u1 = (
        planktannHokyouArrayOfPlank_u[-1] - planktannHokyouArrayOfPlank_u[-2]
    )  # vecu1(単位ベクトルではないを生成)
    vec_u1_NoVec = vec_u1.toNormalArray()  # vecu1をvectorオブジェクトから2Darrayへ

    # vecU2について
    vec_u2 = vec_u1.rotate(90, "degree")
    vec_u2_NonVec_e = vec_u2.toNormalArray()
    vec_u2_NonVec_e = [
        vec_u2_NonVec_e[i]
        / (vec_u2_NonVec_e[0] ** 2 + vec_u2_NonVec_e[1] ** 2) ** (1 / 2)
        for i in range(len(vec_u2_NonVec_e))
    ]

    # vecU3について
    vec_u3 = vec_u2.rotate(-90, "degree")
    vec_u3_NonVec_e = vec_u3.toNormalArray()
    vec_u3_NonVec_e = [
        vec_u3_NonVec_e[i]
        / (vec_u3_NonVec_e[0] ** 2 + vec_u3_NonVec_e[1] ** 2) ** (1 / 2)
        for i in range(len(vec_u3_NonVec_e))
    ]

    # vecU4について
    vec_u4 = vec_u3.rotate(90, "degree")
    vec_u4_NonVec_e = vec_u4.toNormalArray()
    vec_u4_NonVec_e = [
        vec_u4_NonVec_e[i]
        / (vec_u4_NonVec_e[0] ** 2 + vec_u4_NonVec_e[1] ** 2) ** (1 / 2)
        for i in range(len(vec_u4_NonVec_e))
    ]

    # vecU5について
    vec_u5 = vec_u4.rotate(90, "degree")
    vec_u5_NonVec_e = vec_u5.toNormalArray()
    vec_u5_NonVec_e = [
        vec_u5_NonVec_e[i]
        / (vec_u5_NonVec_e[0] ** 2 + vec_u5_NonVec_e[1] ** 2) ** (1 / 2)
        for i in range(len(vec_u5_NonVec_e))
    ]

    # P0,P5をverctorオブジェクトからArrayに変換する
    P0_u_Nonvec = planktannHokyouArrayOfPlank_u[-1].toNormalArray()
    P5_u_NonVec = planktannHokyouArrayOfPlank_u[0].toNormalArray()

    # プランク端補強材のストリンガー上の厚みを計算する（入力値は、翼の最大厚み）
    y_maxU = numpy.amax(y_u)
    y_maxD = numpy.amin(y_d)
    maxThicknessOfYoku = y_maxU - y_maxD  # 翼の最大厚みを保持
    lengthOfvec4 = maxThicknessOfYoku * plankHokyouStringerPlusA / 100
    ##先ほど導出したベクトル類を用いて各点の座標を求める
    # P1 P2 P3(array)を求める（P1＝P0＋単位ベクトルu-1*ストリンガーの１辺の長さ）
    vec_u2_Nonvec_a = [e * vec_u2_NonVec_e[i] for i in range(len(vec_u2_NonVec_e))]
    vec_u3_Nonvec_a = [e * vec_u3_NonVec_e[i] for i in range(len(vec_u3_NonVec_e))]
    vec_u4_Nonvec_a = [
        lengthOfvec4 * vec_u4_NonVec_e[i] for i in range(len(vec_u4_NonVec_e))
    ]
    P1 = numpy.add(P0_u_Nonvec, vec_u2_Nonvec_a)
    P2 = numpy.add(P1, vec_u3_Nonvec_a)
    P3 = numpy.add(P2, vec_u4_Nonvec_a)

    # P4(array)を求める
    lengthP3ToP4 = (
        (P0_u_Nonvec[0] - P5_u_NonVec[0]) ** 2 + (P0_u_Nonvec[1] - P5_u_NonVec[1]) ** 2
    ) ** (1 / 2) + e
    # P4の座標を求める
    vec_u5_Nonvec_a = [
        lengthP3ToP4 * vec_u5_NonVec_e[i] for i in range(len(vec_u5_NonVec_e))
    ]
    P4 = numpy.add(P3, vec_u5_Nonvec_a)

    # P6,P7をVecオブジェクトからarrayへ
    P6 = planktannHokyouArrayOfRibCap_u[0].toNormalArray()
    P7 = planktannHokyouArrayOfRibCap_u[-1].toNormalArray()

    ###出力するために各点をvecオブジェクトへ変換する
    P0_Vec = vector(P0_u_Nonvec[0], P0_u_Nonvec[1], 0)
    P1_Vec = vector(P1[0], P1[1], 0)
    P2_Vec = vector(P2[0], P2[1], 0)
    P3_Vec = vector(P3[0], P3[1], 0)
    P4_Vec = vector(P4[0], P4[1], 0)
    P5_Vec = vector(P5_u_NonVec[0], P5_u_NonVec[1])
    P6_Vec = vector(P6[0], P6[1], 0)
    P7_Vec = vector(P7[0], P7[1], 0)

    ###文字の出力位置
    text = vector(
        O.x + numpy.min(planktannHokyouArrayOfPlank_u_array_x) - 40, O.y + margin
    )

    ###AutoCad出力用のコマンドファイル作成
    spline(file, planktannHokyouArrayOfPlank_u, O)
    line(file, P0_Vec, P1_Vec, O)
    line(file, P1_Vec, P2_Vec, O)
    line(file, P2_Vec, P3_Vec, O)
    line(file, P3_Vec, P4_Vec, O)
    line(file, P4_Vec, P6_Vec, O)
    spline(file, planktannHokyouArrayOfRibCap_u, O)
    line(file, P7_Vec, P5_Vec, O)
    WriteText(file, text, k, 10)
print("completed")
