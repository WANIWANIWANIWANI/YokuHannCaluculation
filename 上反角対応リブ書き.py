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
ProjectName = "1012"
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

# 上反角を付けるために桁をy軸方向へ移動させるか？
use_JouhannkakuChousei = True
# 各リブのy軸の移動量をxに対応する翼厚みに対する％でリスト形式で渡す
y_chousei = [0, 1, 2]

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

# トラス肉抜きを行うための基準点を指定する(翼現に対する％表示で設定を行う)
# 前縁側上面
nikunukiBasePoint_u1_Zenenn = 6
nikunukiBasePoint_u2_Zenenn = 11
nikunukiBasePoint_u3_Zenenn = 13
nikunukiBasePoint_u4_Zenenn = 15
nikunukiBasePoint_u5_Zenenn = 24
nikunukiBasePoint_u6_Zenenn = 26
##前縁側下面
nikunukiBasePoint_d1_Zenenn = 8.5
nikunukiBasePoint_d2_Zenenn = 10.5
nikunukiBasePoint_d3_Zenenn = 18.5
nikunukiBasePoint_d4_Zenenn = 20.5
nikunukiBasePoint_d5_Zenenn = 22.5
nikunukiBasePoint_d6_Zenenn = 31.5
# 後縁側上面
nikunukiBasePoint_u1_Kouenn = 42.5
nikunukiBasePoint_u2_Kouenn = 50.5
nikunukiBasePoint_u3_Kouenn = 52.5
nikunukiBasePoint_u4_Kouenn = 54.5
nikunukiBasePoint_u5_Kouenn = 59.5
nikunukiBasePoint_u6_Kouenn = 61.5
nikunukiBasePoint_u7_Kouenn = 63.5
nikunukiBasePoint_u8_Kouenn = 68
# 後縁側下面
nikunukiBasePoint_d1_Kouenn = 46.5
nikunukiBasePoint_d2_Kouenn = 48.5
nikunukiBasePoint_d3_Kouenn = 54.5
nikunukiBasePoint_d4_Kouenn = 56.5
nikunukiBasePoint_d5_Kouenn = 58.5
nikunukiBasePoint_d6_Kouenn = 63
nikunukiBasePoint_d7_Kouenn = 65

##リブガキの際の分割数を指定
# 基本は200、数が大きいほど精密なリブが書けるが大きくし過ぎるとエラー
bunnkatyu = 200


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


def WriteEllipse(file, ell, O=vector(0, 0)):
    file.write(
        f"ellipse\nc\n{ell.C.x+O.x},{ell.C.y+O.y}\n{ell.P.x+O.x},{ell.P.y+O.y}\n{ell.b}\n"
    )


def WriteCircle(file, circle, O=vector(0, 0), WriteCenter=True):
    """circleオブジェクトを出力するコマンドを出力"""
    file.write(
        """circle
{xc},{yc}
{r}
""".format(
            xc=circle.O.x + O.x, yc=circle.O.y + O.y, r=circle.r
        )
    )
    if WriteCenter:
        line(file, circle.O + vector(0, 5), circle.O + vector(0, -5), O)
        line(file, circle.O + vector(5, 0), circle.O + vector(-5, 0), O)


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


def WriteStringer(file, stringer, O=vector(0, 0)):
    """上のstringerを入力にしてこれを描くコマンドを出力"""
    extentionLineVector_onDA = (stringer.A - stringer.D) * 1.20 + stringer.D
    extentionLineVector_onCB = (stringer.B - stringer.C) * 1.20 + stringer.C
    line(file, stringer.D, extentionLineVector_onDA, O)
    line(file, stringer.C, extentionLineVector_onCB, O)
    file.write(
        """line
{ax},{ay}
{dx},{dy}
{cx},{cy}
{bx},{by}

""".format(
            ax=stringer.A.x + O.x,
            ay=stringer.A.y + O.y,
            bx=stringer.B.x + O.x,
            by=stringer.B.y + O.y,
            cx=stringer.C.x + O.x,
            cy=stringer.C.y + O.y,
            dx=stringer.D.x + O.x,
            dy=stringer.D.y + O.y,
        )
    )


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
            print("距離が" + str(abs(O - P)))
            return "Downside"
        else:
            print("距離が" + str(abs(O - P)))
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
    EdgeDT = [
        RibCap_dPs[i]
        for i in range(1, len(RibCap_dPs))
        if RibCap_dPs[i - 1].x <= x_stringer_dt
    ][
        -2:
    ]  # StringerDT.Aを挟む点
    StringerDT = stringer(
        div_P(EdgeDT[0], EdgeDT[1], x_stringer_dt, 0), EdgeDT[0], e, R=True
    )  # trailing edge

    stringerDT_vec = [
        RibCap_dPs[i]
        for i in range(1, len(RibCap_dPs))
        if RibCap_dPs[i - 1].x <= x_stringer_dt
    ][-2:]
    stringerU1 = [
        PlankPsU[i]
        for i in range(1, len(PlankPsU))
        if PlankPsU[i - 1].x <= x_stringer_u1
    ][-2:]
    stringerU1ToVec = stringer(
        div_P(stringerU1[0], stringerU1[1], x_stringer_u1, 0), stringerU1[0], e
    )

    stringerU2 = [
        PlankPsU[i]
        for i in range(1, len(PlankPsU))
        if PlankPsU[i - 1].x <= x_stringer_u2
    ][-2:]
    stringerU2ToVec = stringer(
        div_P(stringerU2[0], stringerU2[1], x_stringer_u2, 0), stringerU2[0], e
    )

    stringerU3 = [
        PlankPsU[i]
        for i in range(1, len(PlankPsU))
        if PlankPsU[i - 1].x <= x_stringer_u3
    ][-2:]
    stringerU3ToVec = stringer(
        div_P(stringerU3[0], stringerU3[1], x_stringer_u3, 0), stringerU3[0], e
    )

    stringerD1 = [
        PlankPsD[i]
        for i in range(1, len(PlankPsD))
        if PlankPsD[i - 1].x <= x_stringer_D1
    ][-2:]
    stringerD1ToVec = stringer(
        div_P(stringerD1[0], stringerD1[1], x_stringer_D1, 0), stringerD1[0], e, R=True
    )

    stringerD2 = [
        PlankPsD[i]
        for i in range(1, len(PlankPsD))
        if PlankPsD[i - 1].x <= x_stringer_D2
    ][-2:]
    stringerD2ToVec = stringer(
        div_P(stringerD2[0], stringerD2[1], x_stringer_D2, 0), stringerD2[0], e, R=True
    )

    stringerD3 = [
        PlankPsD[i]
        for i in range(1, len(PlankPsD))
        if PlankPsD[i - 1].x <= x_stringer_D3
    ][-2:]
    stringerD3ToVec = stringer(
        div_P(stringerD3[0], stringerD3[1], x_stringer_D3, 0), stringerD3[0], e, R=True
    )

    # プランク線pipe.bの端を切り取る
    del PlankPs[0], PlankPs[-1]
    PlankPs = [StringerU.A] + PlankPs + [StringerDL.A]  # 端点をストリンガーの頂点と一致させる。

    # 上反角の調整用関数
    def calucaulateYokuaAtumi(x):
        y_up = f_u(x)
        y_down = f_d(x)
        return y_up - y_down

    # 桁穴の出力
    delta = RootDelta + (EndDelta - RootDelta) * r
    RibAngle = math.atan(tan((alpha + delta) * numpy.pi / 180) * cos(sweep))
    Pipe_C = vector(x_pipe, f_camber(x_pipe))
    # 上反角に関する桁穴のy座標の移動
    if use_JouhannkakuChousei:
        lengthOfMoveY = y_chousei[k - 1] * calucaulateYokuaAtumi(x_pipe) / 100
        print(x_pipe, "w")
        Pipe_C = vector(x_pipe, f_camber(x_pipe) + lengthOfMoveY)
        print(k, y_chousei[k - 1], calucaulateYokuaAtumi(x_pipe))
    else:
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

    # # 翼弦のx座標の％,外周余白("絶対値で入力する")を入力すると、点の座標を返す関数
    # # upOrDownの部分には、上辺or下辺を指定（"up","down"を第三引数へ指定する）
    # def convertAbstractDataToZahyou(yokuGennRate_x, gaishuYohaku, upOrDown):
    #     y = 0
    #     x = c * (yokuGennRate_x / 100) * cos(sweep)
    #     if upOrDown == "up":
    #         print("up", x, f_d(x))
    #         y = f_d(x) + calucaulateYokuaAtumi(yokuGennRate_x) * gaishuYohaku / 100
    #         return [x, y]
    #     elif upOrDown == "down":
    #         print("down", yokuGennRate_x)
    #         y = f_u(x) - calucaulateYokuaAtumi(yokuGennRate_x) * gaishuuYohaku / 100
    #         return [x, y]

    # Vecarrayの形で渡された点の集まりから、第一引数のｘに最も近い座標を返すための関数
    def findNearestPointBasedOnX(x, VecarrayOfSearch):
        return [
            VecarrayOfSearch[i]
            for i in range(1, len(VecarrayOfSearch))
            if VecarrayOfSearch[i - 1].x <= x
        ][-2:]

    # 翼弦のx座標の％、その翼の厚みに対しての移動％を渡された際に移動後のy座標を返す関数
    def convertYokugennRateGaishuuyohakuToZahyou(yokuGennRate_x, gaishuYohaku):
        x = c * yokuGennRate_x / 100
        y_up = findNearestPointBasedOnX(x, PlankPsU)[0].y
        y_down = findNearestPointBasedOnX(x, PlankPsD)[0].y
        if gaishuYohaku < 0:
            return [x, (y_up - y_down) * gaishuYohaku + y_up]
        elif gaishuYohaku > 0:
            return [x, (y_up - y_down) * gaishuYohaku + y_down]

    # 肉抜きを行う三角形の3点を[]の形式で渡すと、実際に肉抜きコマンドを出六するmakeSannkakuNikunuki()へ渡すためのsannkakkeiObjectを生成する
    def makeSannkakuNikunukiObject(P1_list, P2_list, P3_list):
        sannkakkeiObject = {}
        sannkakkeiObject["basepoint_1_vec"] = vector(P1_list[0], P1_list[1])
        sannkakkeiObject["basepoint_2_vec"] = vector(P2_list[0], P2_list[1])
        sannkakkeiObject["basepoint_3_vec"] = vector(P3_list[0], P3_list[1])
        return sannkakkeiObject

    # sannkakeiObjectから肉抜き穴を出力する
    def makeSannkakuNinuki(file, sannkakuNikunukiObject):
        line(
            file,
            sannkakuNikunukiObject["basepoint_1_vec"],
            sannkakuNikunukiObject["basepoint_2_vec"],
            O,
        )
        line(
            file,
            sannkakuNikunukiObject["basepoint_2_vec"],
            sannkakuNikunukiObject["basepoint_3_vec"],
            O,
        )
        line(
            file,
            sannkakuNikunukiObject["basepoint_1_vec"],
            sannkakuNikunukiObject["basepoint_3_vec"],
            O,
        )

    # トラス肉抜きを出力する
    sankakkeiObject_1 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u1_Zenenn, -0.50),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u2_Zenenn, -0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d1_Zenenn, 0.20),
    )
    sankakkeiObject_2 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u3_Zenenn, -0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d2_Zenenn, 0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d3_Zenenn, 0.20),
    )
    sankakkeiObject_3 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u4_Zenenn, -0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u5_Zenenn, -0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d4_Zenenn, 0.20),
    )
    sankakkeiObject_4 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u6_Zenenn, -0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d5_Zenenn, 0.20),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d6_Zenenn, 0.20),
    )
    sankakkeiObject_5 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u1_Kouenn, -0.25),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u2_Kouenn, -0.25),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d1_Kouenn, 0.30),
    )
    sankakkeiObject_6 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u3_Kouenn, -0.25),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d2_Kouenn, 0.30),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d3_Kouenn, 0.30),
    )
    sankakkeiObject_7 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u4_Kouenn, -0.25),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u5_Kouenn, -0.25),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d4_Kouenn, 0.30),
    )
    sankakkeiObject_8 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d6_Kouenn, 0.30),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d5_Kouenn, 0.30),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u6_Kouenn, -0.25),
    )
    sankakkeiObject_9 = makeSannkakuNikunukiObject(
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_d7_Kouenn, 0.30),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u8_Kouenn, -0.50),
        convertYokugennRateGaishuuyohakuToZahyou(nikunukiBasePoint_u7_Kouenn, -0.25),
    )
    makeSannkakuNinuki(file, sankakkeiObject_1)
    makeSannkakuNinuki(file, sankakkeiObject_2)
    makeSannkakuNinuki(file, sankakkeiObject_3)
    makeSannkakuNinuki(file, sankakkeiObject_4)
    makeSannkakuNinuki(file, sankakkeiObject_5)
    makeSannkakuNinuki(file, sankakkeiObject_6)
    makeSannkakuNinuki(file, sankakkeiObject_7)
    makeSannkakuNinuki(file, sankakkeiObject_8)
    makeSannkakuNinuki(file, sankakkeiObject_9)

    # 現在のリブの図面を出力 要精度-黒 作成時に使う線-青 補助線-ピンク
    # # 翼型 切らないのでピンク
    color(file, 255, 0, 255)
    spline(file, FoilPs, O)
    # 中心線 アセンブリで見るので青
    color(file, 0, 0, 255)
    spline(file, CamberPs, O)
    # プランク 切るので黒
    color(file, 0, 0, 0)
    spline(file, PlankPs, O)
    # リブキャップ切るので黒
    color(file, 0, 0, 0)
    spline(file, RibCap_uPs, O)
    spline(file, RibCap_dPs, O)
    # ストリンガー出力 切るので黒
    color(file, 0, 0, 0)
    WriteStringer(file, StringerDT, O)
    WriteStringer(file, stringerU1ToVec, O)
    WriteStringer(file, stringerU2ToVec, O)
    WriteStringer(file, stringerU3ToVec, O)
    WriteStringer(file, stringerD1ToVec, O)
    WriteStringer(file, stringerD2ToVec, O)
    WriteStringer(file, stringerD3ToVec, O)
    # WriteStringer(file, stringer(vector(xsl, 0), vector(0, 0), e, True), O)

    # プランク、リブキャップ境目出力 切るので黒
    color(file, 0, 0, 0)
    line(file, StringerU.A + O, div_P2(StringerU.D, StringerU.A, 1 + tp / e) + O)
    line(file, StringerDL.A + O, div_P2(StringerDL.D, StringerDL.A, 1 + tp / e) + O)
    # 桁穴出力切るので黒
    color(file, 0, 0, 0)
    WriteEllipse(file, Pipe, O)
    # アセンブリ棒穴　切るので黒
    color(file, 0, 0, 0)
    WriteCircle(file, Assembly, O)
    # 後縁材の前縁側の一辺を出力 切ると思うので黒
    color(file, 0, 0, 0)
    line(file, TrailU, TrailD, O)
    # 前縁材の出力 切るが、黒だと図面が汚いので赤
    if use_l:
        color(file, 255, 0, 0)
        spline(file, LeadPs, O)
        if use_la:
            # 前縁材の端線の出力
            line(file, LeadPs[0], LeadEndP2U, O)
            line(file, LeadPs[-1], LeadEndP2D, O)
            # 前縁材の水平線を出力
            line(file, LeadPs[0], LeadPs[0] - vector(lo, 0), O)
            line(file, LeadPs[-1], LeadPs[-1] - vector(lo, 0), O)
            spline(file, offset(LeadPs, offset_l, 0, 1), O)
    # 水平、鉛直線 特別に緑
    color(file, 0, 170, 0)
    line(file, hlineP1, hlineP2, O)
    line(file, vlineP1, vlineP2, O)

    # # ここから後縁肉抜きへ
    # # 丸肉抜き出力 前縁から
    # # 最前縁の丸の中心の座標
    # x_cir = Pipe.C.x + (d + dd) / 2
    # x_cir += (f_u(x_cir) - f_d(x_cir)) / 2
    # light_Cs = [
    #     circle((f_u(x_cir) - f_d(x_cir)) / 2 - w_circle, vector(x_cir, f_camber(x_cir)))
    # ]
    # i = 1
    # while True:
    #     x_cir = light_Cs[i - 1].O.x + light_Cs[i - 1].r
    #     x_cir += (f_u(x_cir) - f_d(x_cir)) / 2
    #     light_Cs += [
    #         circle(
    #             (f_u(x_cir) - f_d(x_cir)) / 2 - w_circle, vector(x_cir, f_camber(x_cir))
    #         )
    #     ]
    #     # Assembly棒より前縁側にあるとき
    #     if not light_Cs[i].O.x + light_Cs[i].r < Assembly.O.x - Assembly.r - w_circle:
    #         light_Cs = light_Cs[:-1]  # 被ったのはとりのぞく
    #         break
    #     i += 1
    # for C in light_Cs:
    #     print("circle")
    #     WriteCircle(file, C, O, WriteCenter=True)

    # 番号出力 切らないのでピンク
    color(file, 255, 0, 255)
    WriteText(
        file, vector(c * 0.05, O.y + f_camber(c * 0.05)), f"{PlaneNumber}-{k}", height=7
    )

# 設定出力 切らないのでピンク
color(file, 255, 0, 255)
WriteText(
    file,
    vector(RootChord * 1.05, 0),
    f"""根翼弦 : {RootChord} mm
端翼弦 : {EndChord} mm
根ねじり上げ : {RootDelta} °
端ねじり上げ : {EndDelta} °
根の桁位置 : {RootR} %
端の桁位置 : {EndR} %
根の翼型 : {RootFoilName}
端の翼型 : {EndFoilName}
半リブがあるか : {use_half}
プランク厚さ : {tp} mm
ストリンガー断面の一辺 : {e} mm
リブキャップ厚さ : {t} mm
桁長軸径 : {d+dd} mm
桁短軸径 : {d} mm
アセンブリ棒径 : {da} mm
アセンブリ棒余白 : {h} mm
前縁がある : {str(use_l)}
前縁材の前縁からのずれ : {lo} mm
肉抜き最小骨格幅 : {w_tri} mm
三角肉抜き端半径 : {r_tri} mm
前縁-肉抜き 長さ : {first_light_r} mm
丸肉抜き 最小骨格幅 : {w_circle} mm
プランク上開始位置 : {rpu:.1f} %
プランク下開始位置 : {rpd:.1f} %
ストリンガー下後縁位置 : {rsdt} %
ストリンガー前縁は前縁から : {xsl} mm
後退角 : {sweep*180/numpy.pi} °


""",
)


file.close
print("completed")
