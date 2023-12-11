import numpy as np


##ファイル関連
# 翼型を保管しておき、コマンドファイルを出力するディレクトリのPath
Directory = r"C:\Users\ryota2002\Documents\その他"

##計算条件の設定
maxLibKannkaku = 160
minLibKannaku = 120
maxPLankAtumi = 2.5
minPLankAtumi = 1.5
bunnkatu = 100

##計算を行うパターン数
caluculatePattern = 100

## 計算を行う全翼の2次構造を定義する
# 翼型
wing_shape = [
    ["dae21.dat", "dae21.dat"],
    ["dae21.dat", "dae21.dat"],
    ["dae21.dat", "dae21.dat"],
    ["dae21.dat", "dae21.dat"],
    ["dae21.dat", "dae21.dat"],
    ["dae21.dat", "dae21.dat"],
]
# 翼弦[[0Root,0End],[],[]]の形式で記述
wing_chood = [
    [1200, 1200],
    [1200, 1200],
    [1100, 1100],
    [1000, 1000],
    [900, 900],
    [800, 800],
]
# 桁長さ
wing_pipe_length = [3000, 3000, 3000, 3000, 3000, 3000]
# 桁径
wing_pipe = [100, 100, 100, 100, 100, 100]

##複数の重量推定を行うためにリブ間とプランク厚みを変化させる
LibSpanList = np.arange(minLibKannaku, maxLibKannkaku, 0.1)
plankAtumiList = np.arange(minPLankAtumi, maxPLankAtumi, 0.01)

##計算式中で固定すべき設定値
##計算に絡む値
# halfRibの切り取り線
halfRibLine_d = 0.375
# 肉抜き量
# トラス肉抜きを行うための基準点を指定する(翼現に対する％表示で設定を行う)
# 翼弦方向の座標指定
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

# y軸方向に対する座標指定(あるx座標に対応する翼厚に対する割合を入力（＋方向の移動は、＋０．＠＠、ー方向の移動は、ー０．＠＠で入力）)
# 前縁側上面
nikunukiBasePoint_u1_Zenenn_YokuatuRate = -0.50
nikunukiBasePoint_u2_Zenenn_YokuatuRate = -0.20
nikunukiBasePoint_u3_Zenenn_YokuatuRate = -0.20
nikunukiBasePoint_u4_Zenenn_YokuatuRate = -0.20
nikunukiBasePoint_u5_Zenenn_YokuatuRate = -0.20
nikunukiBasePoint_u6_Zenenn_YokuatuRate = -0.20
##前縁側下面
nikunukiBasePoint_d1_Zenenn_YokuatuRate = 0.20
nikunukiBasePoint_d2_Zenenn_YokuatuRate = 0.20
nikunukiBasePoint_d3_Zenenn_YokuatuRate = 0.20
nikunukiBasePoint_d4_Zenenn_YokuatuRate = 0.20
nikunukiBasePoint_d5_Zenenn_YokuatuRate = 0.20
nikunukiBasePoint_d6_Zenenn_YokuatuRate = 0.20
# 後縁側上面
nikunukiBasePoint_u1_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u2_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u3_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u4_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u5_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u6_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u7_Kouenn_YokuatuRate = -0.25
nikunukiBasePoint_u8_Kouenn_YokuatuRate = -0.50
# 後縁側下面
nikunukiBasePoint_d1_Kouenn_YokuatuRate = 0.30
nikunukiBasePoint_d2_Kouenn_YokuatuRate = 0.30
nikunukiBasePoint_d3_Kouenn_YokuatuRate = 0.30
nikunukiBasePoint_d4_Kouenn_YokuatuRate = 0.30
nikunukiBasePoint_d5_Kouenn_YokuatuRate = 0.30
nikunukiBasePoint_d6_Kouenn_YokuatuRate = 0.30
nikunukiBasePoint_d7_Kouenn_YokuatuRate = 0.30

##各材料の密度情報
# 各定数を以下で設定する（試作）
ribFixKetaanaDensity = 0.007  # 桁穴周りの接着剤の密度（g/(桁穴1mm)
tannribuHokyouDensity = 0.00038  # 端リブ補強材（バルサ＋ボンド）の密度（g / mm²）
ribCapDensity = 0.00038  # リブキャップの密度（g/リブキャップ１mm²）
densityOfKouennzai = 0.0001294  # 後縁材の値を求める（g/mm³） つまり、2024的にはバルサの密度を書けばよい
densityOfStringer = 0.0001294  # ストリンガーの密度（ｇ/mm³） つまり、2024的にはバルサの密度を書けばよい
densityOfRyoumennteap = 0.00040  # 両面テープの密度（g/mm2）

# １次構造
weightOfketa = 0  # 桁の重量(g)
weightOfFrange = 0  # フランジの重量
weightOfKannzashi = 0  # かんざしの重量

# 既知の値
lengthOfKeta = 3400  # 桁の長さ
numberOfRyoumennteapForVerticalForYokugenn = 7  # 翼弦に対して垂直な方向の両面テープ数
sutairoDensity = 0.000031  # スタイロの密度(g/mm3)
ketaLengthFrangeinsideToFrangeInside = 3400  # 桁長さ
NumberOfStringer = 7  # ストリンガーの本数
lengthOfstringerSide1 = 5  # ストリンガーの一辺の長さ
lengthOFStringerSide2 = 5  # ストリンガーの一辺の長さ
densityOfFilm = 0.000011  # フィルムの密度（ｇ/mm³）
crosSectionalAreaKouennzai = 200  # 後縁材の断面積（mm²）(スタイロコア材推定)
kouennzaihokyouCarbonwidth = 10  # 後縁材に貼り付けるカーボン補強の厚み(mm)
kouennzaihokyouCarbondencity = 0.0020  # 後縁材に貼り付けるカーボン補強の密度（g/mm）


##不要な設定値
# 機体諸元
# 0翼取り付け角[°](定常飛行迎角)
alpha = 0
# 後退角(リブ厚みの修正用)[°]
sweep = 0
# 端、根のねじり上げ(流れ方向)[°]
RootDelta = 0
EndDelta = 0
# 端、根の桁位置[%]
RootR = 37
EndR = 37
# アセンブリ棒径[mm]
da = 30
# アセンブリ棒余白[mm]
h = 7
# 後縁材の前縁側の辺の長さ[mm]
ht = 11
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


# ------------------------------------------------------------------------------------------
# 準備

import os
import numpy
from scipy import integrate

# import matplotlib.pyplot as pyplot
import scipy.interpolate as interp
import scipy.optimize as optimize

inter = interp.Akima1DInterpolator
import math

sin, cos, tan, atan2 = (math.sin, math.cos, math.tan, math.atan2)
from scipy.optimize import fsolve
import numpy as np

os.chdir(Directory)  # ディレクトリ移動

# ライブラリおわり
# ----------------------------------------------------------------------------------------

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
        if not self.R:
            return self.A + self.AB.i
        else:
            return self.A - self.AB.i

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


# ２点を通る方程式
# (y=数値) or (x=数値) or (y=mx+n)　#line[傾きm、ｙ切片n]
def makeLinearEquation(x1, y1, x2, y2):
    line = []
    if y1 == y2:
        # y軸に平行な直線
        line["y"] = y1
    elif x1 == x2:
        # x軸に平行な直線
        line["x"] = x1
    else:
        # y = mx + n
        line.append((y1 - y2) / (x1 - x2))
        line.append(y1 - (line[0] * x1))
    return line


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
            print("距離が" + str(abs(O - P)))
            return "Downside"
        else:
            print("距離が" + str(abs(O - P)))
            return "Upside"
    return "Separated"


def find_nearest(array, value):  # 配列の中身の内最もvalueの値に近いものを取り出す
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    index = array.__index__
    return array[idx]


# リブ枚数を渡すことで、リブの厚みリスト（翼の重量計算に使うを生成する）
def generateRibuAtuiList(numberOfrib):
    atumiList = []
    for i in range(0, numberOfRib):
        if i == 0 or i == numberOfRib - 1:
            atumiList.append(15)
        else:
            atumiList.append(7)
    return atumiList


# リブの種類を設定する関数
def generateRibuPatternList(numberOfRib):
    ribPatternList = []
    for i in range(0, numberOfRib):
        if i == 0 or i == numberOfRib - 1:
            ribPatternList.append(0)
        else:
            if i % 2 == 0:
                ribPatternList.append(1)
            else:
                ribPatternList.append(2)
    return ribPatternList


# プランクの厚みを保持する関数
def generataPlankAtumiList(numberOfRib, plankAtumi):
    plankAtumi = []
    for i in range(0, numberOfRib):
        plankAtumi.append(tp)
    return plankAtumi


# 翼表面の変形を計算するための関数
def caluculateYokuSurfaceDeviation(ribuInterval, plankAtumi):
    # リブ間とプランク厚みを0-1の数字へと変換する
    standardizedRibKann = (ribuInterval - minLibKannaku) / (
        maxLibKannkaku - minLibKannaku
    )
    standardizedPlank = (tp - minPLankAtumi) / (maxPLankAtumi - minPLankAtumi)

    # 翼表面の変形量定数（(リブ間)^4/(プランク厚み)^3）
    return standardizedRibKann**4 / standardizedPlank**3


# 関数、クラス定義おわ り
# ------------------------------------------------------------------------------------------------

# 各パターンごとに機体重量と翼表面変形定数を収めたリストを作る
# [[機体重量,翼表面の変形定数],[,]...]
outPutList = []

# 各パターンごとに重量推定
counter = 0
while counter < caluculatePattern:
    counter = counter + 1
    libSpan = np.random.choice(LibSpanList, 1)
    plankAtumi = np.random.choice(plankAtumiList, 1)
    # 各翼別の重量を保持するリスト
    wingWeightList = []
    # ここで各翼の重量計算を行う（0-5翼）
    for yokuNumber in range(0, 6):
        caluculate2DStructureOfWingObject = {}
        ####翼の座標計算を行う#####
        ##乱数計算により決まる値を計算
        # リブ枚数の計算
        n = round(wing_pipe_length[yokuNumber] / libSpan[0])
        numberOfRib = n
        #
        # 指定した翼の2次構造情報を設定する
        # 翼関連
        # 端、根の翼弦長(流れ方向)[mm]
        RootChord = wing_chood[yokuNumber][0]
        EndChord = wing_chood[yokuNumber][1]
        # 端、根の翼型のファイル名 datファイルを入れる
        RootFoilName = wing_shape[yokuNumber][0]
        EndFoilName = wing_shape[yokuNumber][1]
        # リブ以外の要素関連
        # プランク厚さ[mm]
        tp = plankAtumi
        # ストリンガー断面の一辺[mm]
        e = 5
        # リブキャップ厚さ[mm]
        t = 1
        # 桁径[mm]	楕円の短軸方向
        d = wing_pipe[yokuNumber]
        # 桁径		楕円の長軸-短軸 円なら0
        dd = wing_pipe[yokuNumber] - d

        # 上面下面で同じ値を指定することは不可
        # 後縁補強材上辺開始点(翼弦に対する％)
        startPointOfKouennHokyou_U = 80
        # 後縁補強材下辺開始点(翼弦に対する％)
        startPointOfKouennHokyou_D = 80

        # 上面下面で同じ値を指定することは不可
        # 端リブ補強材上辺開始点(翼弦に対する％)
        startPointOfendRibHokyou_U = 0.01
        # 端リブ強材下辺開始点(翼弦に対する％)
        startPointOfendRibHokyou_D = 0.02

        # 位置関連
        # プランク上開始位置[%]
        rpu = 60
        # プランク下開始位置[%] r plank downside
        rpd = EndR - 100 * (d / 2 + 30) / EndChord
        # ストリンガー下後縁側位置[%] r stringer downside trailing edge
        rsdt = rpd + 20
        # ストリンガー前縁[mm] x stringer leading edge
        xsl = 20 + e

        # プランク端補強材の導入位置の設定
        # プランク端補強開始位置(翼弦に対する％)(上面最後縁のストリンガー位置を設定)
        plankHokyouStartRate_U = 57
        # プランク端補強終了位置（翼弦に対する％）
        plankHokyouEndPoint_U = rpu + 0.01  # 値を小さくしすぎるとエラーになる
        # プランク補強材の厚み(最大翼厚にたいする％で表示)
        plankHokyouStringerPlusA = 3

        ####ここから各翼の重量を計算する####

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
            EndFoilDataU_x[::-1] * EndChord * cos(sweep),
            EndFoilDataU_y[::-1] * EndChord,
        )
        f_dEnd = inter(
            EndFoilDataD_x * EndChord * cos(sweep), EndFoilDataD_y * EndChord
        )
        f_uRoot = inter(
            RootFoilDataU_x[::-1] * RootChord * cos(sweep),
            RootFoilDataU_y[::-1] * RootChord,
        )
        f_dRoot = inter(
            RootFoilDataD_x * RootChord * cos(sweep), RootFoilDataD_y * RootChord
        )
        EndFoilPs = [
            vector(P.x * EndChord * cos(sweep), P.y * EndChord) for P in EndFoilData
        ]
        RootFoilPs = [
            vector(P.x * RootChord * cos(sweep), P.y * RootChord) for P in RootFoilData
        ]
        # パイプの中心
        EndPipeO = vector(
            EndR * EndChord / 100,
            f_uEnd(0.25 * EndChord) / 2 + f_dEnd(0.25 * EndChord) / 2,
        )
        RootPipeO = vector(
            RootR * RootChord / 100,
            f_uRoot(0.25 * RootChord) / 2 + f_dRoot(0.25 * RootChord) / 2,
        )

        # excel出力用のリスト
        excelareayokuGata = []
        excelareatotalAreaOfNikunuki = []
        excelareaTotalRibu = []
        excellengthOfKetaanaMawari = []
        excelLengthOfRibCapTotal = []
        excelLengthOfPlankTotal = []
        excelKouennHokyou = []
        excelareaHalfRib = []
        excelEndRibHokyou = []
        excelPlankEndHokyou = []

        O = vector(0, 0)  # それぞれのリブの前縁のy座標
        y_u, y_d = [], []  # 定義前に使うと誤解されないように
        for k in range(1, n + 1):  # range(1,n+1):				 	#根から k 枚目のリブ
            # y座標の設定 かぶらないようにするため。1cmの隙間もあける
            if k > 1:  # k=1のときO=(0,0)にしている
                O.y -= numpy.max(y_u) - numpy.min(y_d) + 10

            # 翼型の点のリストの出力。 上下の翼型を関数として作成。
            # 混ぜる割合。　根で0、端で1。
            r = (k - 1) / (n - 1)
            # 翼弦 流れ方向
            c = RootChord + (EndChord - RootChord) * r
            # 翼型を上下別に関数に近似。 上下一緒に近似する方法は思いつかなかった。 fはfunctionの略
            f_uEnd = inter(
                EndFoilDataU_x[::-1] * c * cos(sweep), EndFoilDataU_y[::-1] * c
            )
            f_dEnd = inter(EndFoilDataD_x * c * cos(sweep), EndFoilDataD_y * c)
            f_uRoot = inter(
                RootFoilDataU_x[::-1] * c * cos(sweep), RootFoilDataU_y[::-1] * c
            )
            f_dRoot = inter(RootFoilDataD_x * c * cos(sweep), RootFoilDataD_y * c)
            # x座標の列を端と同じにする
            s = numpy.linspace(0, 1, bunnkatu)
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
            f_camber = inter(
                s, (f_u(s) + f_d(s)) / 2
            )  # 上下の翼型の関数の平均であると近似 特に前縁付近は信用できない
            CamberPs = to_vectors2(s, f_camber(s))
            del s

            # 境目になるようなx座標を定義する
            x_plank_u = c * (rpu / 100) * cos(sweep)
            x_plank_d = c * (rpd / 100) * cos(sweep)
            x_stringer_dt = c * rsdt / 100 * cos(sweep)
            x_pipe = c * (RootR + (EndR - RootR) * r) / 100 * cos(sweep)
            x_25pc = c * cos(sweep) * 0.25

            # プランクの点のリストの出力
            PlankPs = offset(
                [FoilU[i] for i in range(len(FoilU) - 2) if FoilU[i + 2].x <= x_plank_u]
                + [FoilU[-2], FoilD[0], FoilD[1]]
                + [
                    FoilD[i]
                    for i in range(2, len(FoilD))
                    if FoilD[i - 2].x <= x_plank_d
                ],
                tp,
                0,
            )
            PlankPsU = [P for P in PlankPs if P.y >= 0][::-1]
            PlankPsD = [P for P in PlankPs if P.y <= 0]
            # リブキャップの点のリストの出力 プランクの開始点より後縁側であることを利用
            RibCap_uPs = offset(
                [FoilU[i] for i in range(2, len(FoilU)) if FoilU[i - 2].x >= x_plank_u],
                t,
                0,
            )
            RibCap_dPs = offset(
                [
                    FoilD[i]
                    for i in range(len(FoilD) - 2)
                    if FoilD[i + 2].x >= x_plank_d
                ],
                t,
                0,
            )
            # 後縁材の出力
            # 後縁材の上側の一点を求める。下をoffsetした関数と上の関数の交点とする。
            FoilD_offsetPs = offset(FoilD[5:], ht, 0)
            s = numpy.linspace(FoilD_offsetPs[0].x, FoilD_offsetPs[-1].x)
            f_dOffset = inter(to_numpy_x(FoilD_offsetPs), to_numpy_y(FoilD_offsetPs))
            TrailU_x = optimize.newton(
                lambda x: f_dOffset(x) - f_u(x), c * cos(sweep) * 0.95
            )
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

            # 後縁補強材を構成する点のリストを出六
            x_stratPointOfKouennzai_U = (
                c * (startPointOfKouennHokyou_U / 100) * cos(sweep)
            )
            x_stratPointOfKouennzai_D = (
                c * (startPointOfKouennHokyou_D / 100) * cos(sweep)
            )

            KouennHokyou_U_X = []  # 後縁補強材上側のｘ座標を保持する配列
            KouennHokyou_U_Y = []  # 後縁補強材上側のｙ座標を保持する配列
            KouennHokyou_D_X = []  # 後縁補強材下側のｘ座標を保持する配列
            KouennHokyou_D_Y = []  # 後縁補強材下側のｙ座標を保持する配列
            for i in range(len(x_u)):  # 上記のリストへ
                if x_u[i] >= x_stratPointOfKouennzai_U:
                    KouennHokyou_U_X.append(x_u[i])
                    KouennHokyou_U_Y.append(y_u[i])
                if x_d[i] >= x_stratPointOfKouennzai_D:
                    KouennHokyou_D_X.append(x_d[i])
                    KouennHokyou_D_Y.append(y_d[i])

            # 端リブ補強材を構成する点のリストを出六
            x_stratPointOfEndRib_U = c * (startPointOfendRibHokyou_U / 100) * cos(sweep)
            x_stratPointOfEndRib_D = c * (startPointOfendRibHokyou_D / 100) * cos(sweep)

            endRibHokyou_U_X = []  # 後縁補強材上側のｘ座標を保持する配列
            endRibHokyou_U_Y = []  # 後縁補強材上側のｙ座標を保持する配列
            endRibHokyou_D_X = []  # 後縁補強材下側のｘ座標を保持する配列
            endRibHokyou_D_Y = []  # 後縁補強材下側のｙ座標を保持する配列
            for i in range(len(x_u)):  # 上記のリストへ
                if x_u[i] >= x_stratPointOfEndRib_U:
                    endRibHokyou_U_X.append(x_u[i])
                    endRibHokyou_U_Y.append(y_u[i])
                if x_d[i] >= x_stratPointOfEndRib_D:
                    endRibHokyou_D_X.append(x_d[i])
                    endRibHokyou_D_Y.append(y_d[i])

            # リブのデータ書き出しおわり
            # 以下では、リブの面積を計算する
            # 計算式の定義
            def caluculateOfareaYokugata():
                areaYokugataUpper = -integrate.trapz(y_u, x_u)
                areaYokugataDown = -integrate.trapz(y_d, x_d)
                return areaYokugataUpper + areaYokugataDown

            def caluculationOfareaKouennHokyou():
                areaKouennHokyouUpper = -integrate.trapz(
                    KouennHokyou_U_Y, KouennHokyou_U_X
                )
                areaKouennHokyouDown = integrate.trapz(
                    KouennHokyou_D_Y, KouennHokyou_D_X
                )
                # 積分した面積から一部を引く
                # 引く面積をざっくりと近似（翼弦長の差分＊上下の後縁開始点のｙ座標の差分＊0.50）
                subtractionArea = (
                    abs(x_stratPointOfKouennzai_U - x_stratPointOfKouennzai_D)
                    * abs(KouennHokyou_U_Y[0] - KouennHokyou_D_Y[0])
                    * 0.50
                )
                return areaKouennHokyouUpper + areaKouennHokyouDown - subtractionArea

            def areaKetaana():
                return 3.14 * d / 2 * (dd + d) / 2

            def lengthOfketaanaShu():
                # 桁の短軸ｄ、桁の長軸ｄｄ＋ｄ
                a = d / 2
                b = dd / 2
                X = 2 * a + b  # 短軸＋長軸
                Y = b  # 短軸ー長軸
                Z = (Y / X) ** 2
                W1 = 3 * Z
                W2 = 10 + (4 - 3 * Z) ** (1 / 2)
                return 3.14 * X * (1 + W1 / W2)

            def lengthOfPlank():
                plank_u_ToNonVec = []  # リブキャップ上の点の集合のベクトルを外したリスト保持
                plank_d_ToNonVec = []  # リブキャップ下の点の集合のベクトルを外したリスト保持
                plankLength_u = 0  # リブキャップ上面の長さを保持
                plankLength_d = 0  # リブっキャプ下面の長さを保持
                for i in range(len(x_u)):  # 上記のリストへ
                    addition_array_PlankU_nonVec = [x_u[i], y_u[i]]
                    additional_array_PlankD_nonVec = [x_d[i], y_d[i]]
                    if addition_array_PlankU_nonVec[0] <= x_plank_u:
                        plank_u_ToNonVec.append(addition_array_PlankU_nonVec)
                    if additional_array_PlankD_nonVec[0] <= x_plank_d:
                        plank_d_ToNonVec.append(additional_array_PlankD_nonVec)
                for i in range(len(plank_u_ToNonVec) - 1):  # 隣り合う２点間の距離を足し合わせて曲線の長さとした
                    discussP1_u = plank_u_ToNonVec[i]
                    discussP2_u = plank_u_ToNonVec[i + 1]
                    lengthOfP1P2_u = (
                        (discussP1_u[0] - discussP2_u[0]) ** 2
                        + (discussP1_u[1] - discussP2_u[1]) ** 2
                    ) ** (1 / 2)
                    plankLength_u += lengthOfP1P2_u
                for i in range(len(plank_d_ToNonVec) - 1):
                    discussP1_d = plank_d_ToNonVec[i]
                    discussP2_d = plank_d_ToNonVec[i + 1]
                    lengthOfP1P2_d = (
                        (discussP1_d[0] - discussP2_d[0]) ** 2
                        + (discussP1_d[1] - discussP2_d[1]) ** 2
                    ) ** (1 / 2)
                    plankLength_d += lengthOfP1P2_d
                Plank_total_Length = plankLength_u + plankLength_d
                return Plank_total_Length

            def caluculationOfAreaEndRibHokyou():
                ##積分面積を保持(翼弦を積分軸にして積分の実行)
                areaHalflib_u = -integrate.trapz(endRibHokyou_U_Y, endRibHokyou_U_X)
                areaHalflib_d = integrate.trapz(endRibHokyou_D_Y, endRibHokyou_D_X)
                totalAreaIntegrateEndRib = areaHalflib_u + areaHalflib_d
                ##足し引きして調整する部分の面積
                # 翼上面の補強開始点と下面の補強開始点を結ぶ１次関数を求める
                linearObject = makeLinearEquation(
                    x_stratPointOfEndRib_U,
                    x_stratPointOfEndRib_D,
                    endRibHokyou_U_X[0],
                    endRibHokyou_U_Y[0],
                )
                # 端リブの切り取り線と中心線の接点のｘ座標を求める
                crossingCenterAndHalfRibCutline_x = -linearObject[1] / linearObject[0]
                # 足し引きを行う面積を求める
                subtrackAreaU = (
                    abs(endRibHokyou_U_X[-1] - crossingCenterAndHalfRibCutline_x)
                    * abs(endRibHokyou_U_Y[-1])
                    * (1 / 2)
                )
                addAreaD = abs(
                    endRibHokyou_U_X[0] - crossingCenterAndHalfRibCutline_x
                ) * abs(endRibHokyou_U_Y[0])
                # 端リブ補強材の面積
                areaEndRibHokyou = totalAreaIntegrateEndRib - subtrackAreaU + addAreaD
                return [areaEndRibHokyou, crossingCenterAndHalfRibCutline_x]

            def caluculationOfAreaHalfRib():
                # halfRib切り取り線を決める２点を出力
                # 上面に関してはプランク端、下面は、stringerDTの出力位置
                # stringerDtのｘ座標を求める
                placeStartPointOfHalfRib_D = c * halfRibLine_d * cos(sweep)
                # この値に最も近いリブキャップ上の位置をリブ下面の切り取り点とする
                nearestPointOfHalfRibCut_d_x = find_nearest(
                    x_d, placeStartPointOfHalfRib_D
                )  # x座標
                # x座標の配列内でのindexからｙ座標を配列から引き出す(indexが[]で出力される)
                crossingCenterAndHalfRibCutline_x_index_array_in_x_d = numpy.where(
                    x_d == nearestPointOfHalfRibCut_d_x
                )
                if len(crossingCenterAndHalfRibCutline_x_index_array_in_x_d) > 2:
                    print("error;halfRibの切り取り線が1つに決まりません.errorを解消してください")
                # リブ下面切り取り点のｙ座標
                nearestPointOfHalfRibCut_d_y = y_d[
                    crossingCenterAndHalfRibCutline_x_index_array_in_x_d[0]
                ]
                ##翼弦に対して積分を行う
                plank_u_ToNonVec_x = []  # プランク上のx座標の集合 xの値が大きいものから順番に配列の中に存在
                plank_u_ToNonVec_y = []  # プランク上のｙ座標の集合
                plank_d_ToNonVec_x = []  # プランク下のx座標の集合　ｘの値が小さいモノから順の配列に存在
                plank_d_ToNonVec_y = []  # 　プランク下のy座標の集合
                for i in range(len(x_u)):  # 上記のリストへ
                    if x_u[i] < x_plank_u:
                        addition_array_PlankU_x = x_u[i]
                        addition_array_PlankU_y = y_u[i]
                        plank_u_ToNonVec_x.append(addition_array_PlankU_x)
                        plank_u_ToNonVec_y.append(addition_array_PlankU_y)
                for i in range(len(x_d)):
                    if x_d[i] < nearestPointOfHalfRibCut_d_x:
                        addition_array_PlankD_x = x_d[i]
                        addition_array_PlankD_y = y_d[i]
                        plank_d_ToNonVec_x.append(addition_array_PlankD_x)
                        plank_d_ToNonVec_y.append(addition_array_PlankD_y)
                areaHalflib_u = -integrate.trapz(plank_u_ToNonVec_y, plank_u_ToNonVec_x)
                areaHalflib_d = -integrate.trapz(plank_d_ToNonVec_y, plank_d_ToNonVec_x)
                totalAreaIntegrate = areaHalflib_u + areaHalflib_d  # 翼弦を積分軸にして積分

                # 積分値から引き去る部分
                # halfribの切り取る１次関数を定義
                linearObject = makeLinearEquation(
                    nearestPointOfHalfRibCut_d_x,
                    nearestPointOfHalfRibCut_d_y,
                    plank_u_ToNonVec_x[0],
                    plank_u_ToNonVec_y[0],
                )
                # halfRibの切り取り線と中心線の接点のｘ座標を求める
                crossingCenterAndHalfRibCutline_x = -linearObject[1] / linearObject[0]

                # 積分の値から足し引く部分の面積を計算する
                # 下側については加える、上側に関しては引く
                subtrackAreaU = (
                    abs(plank_u_ToNonVec_x[0] - crossingCenterAndHalfRibCutline_x)
                    * plank_u_ToNonVec_y[0]
                    * (1 / 2)
                )
                addAreaD = (
                    abs(plank_d_ToNonVec_x[-1] - crossingCenterAndHalfRibCutline_x)
                    * -plank_d_ToNonVec_y[-1]
                    * (1 / 2)
                )
                # halfRibの面積
                areaHalfRib = totalAreaIntegrate - subtrackAreaU[0] + addAreaD[0]
                return areaHalfRib

            def lehgthOfRibCap():
                ribCap_u_ToNonVec = []  # リブキャップ上の点の集合のベクトルを外したリスト保持
                ribCap_d_ToNonVec = []  # リブキャップ下の点の集合のベクトルを外したリスト保持
                ribCapLength_u = 0  # リブキャップ上面の長さを保持
                ribCapLength_d = 0  # リブっキャプ下面の長さを保持
                for i in range(len(x_u)):  # 上記のリストへ
                    addition_array_ribCapU_nonVec = [x_u[i], y_u[i]]
                    additional_array_ribCapD_nonVec = [x_d[i], y_d[i]]
                    if addition_array_ribCapU_nonVec[0] >= x_plank_u:
                        ribCap_u_ToNonVec.append(addition_array_ribCapU_nonVec)
                    if additional_array_ribCapD_nonVec[0] >= x_plank_d:
                        ribCap_d_ToNonVec.append(additional_array_ribCapD_nonVec)
                for i in range(len(ribCap_u_ToNonVec) - 1):  # 隣り合う２点間の距離を足し合わせて曲線の長さとした
                    discussP1_u = ribCap_u_ToNonVec[i]
                    discussP2_u = ribCap_u_ToNonVec[i + 1]
                    lengthOfP1P2_u = (
                        (discussP1_u[0] - discussP2_u[0]) ** 2
                        + (discussP1_u[1] - discussP2_u[1]) ** 2
                    ) ** (1 / 2)
                    ribCapLength_u += lengthOfP1P2_u
                for k in range(len(ribCap_d_ToNonVec) - 1):
                    discussP1_d = ribCap_d_ToNonVec[k]
                    discussP2_d = ribCap_d_ToNonVec[k + 1]
                    lengthOfP1P2_d = (
                        (discussP1_d[0] - discussP2_d[0]) ** 2
                        + (discussP1_d[1] - discussP2_d[1]) ** 2
                    ) ** (1 / 2)
                    ribCapLength_d += lengthOfP1P2_d
                ribCap_total_Length = ribCapLength_u + ribCapLength_d
                return ribCap_total_Length

            def teaperRation():
                return EndChord / RootChord

            def caluculationOfPlankEndHokyou():
                #####長方形部分と三角形部分の面積に分割して考える
                ####翼の最大厚み
                y_maxU = numpy.amax(y_u)
                y_maxD = numpy.amin(y_d)
                maxThicknessOfYoku = y_maxU - y_maxD
                #####該当リブの翼弦を保持
                x_max = numpy.amax(x_u)

                # 長方形部分
                # 桁に対して垂直な方向の長さ
                lengthOfY = maxThicknessOfYoku * (plankHokyouStringerPlusA / 100) + e
                # 桁に対して平行な方向の長さ
                lengthOfX_chouhoukei = x_max * (rpu - plankHokyouStartRate_U) / 100
                areaChouhoukei = lengthOfX_chouhoukei * lengthOfY

                # 三角形部分
                lengthOfX_square = x_max * (plankHokyouEndPoint_U - rpu) / 100
                areaSquare = lengthOfX_square * lengthOfY * (1 / 2)

                # プランク端補強の面積
                areaPlankEndHokyou = areaChouhoukei + areaSquare

                return areaPlankEndHokyou

            ##肉抜きを行う
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

            # トラス肉抜きobjectを作る
            sannkakuObjectList = [
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u1_Zenenn,
                        nikunukiBasePoint_u1_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u2_Zenenn,
                        nikunukiBasePoint_u2_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d1_Zenenn,
                        nikunukiBasePoint_d1_Zenenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u3_Zenenn,
                        nikunukiBasePoint_u3_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d2_Zenenn,
                        nikunukiBasePoint_d2_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d3_Zenenn,
                        nikunukiBasePoint_d3_Zenenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u4_Zenenn,
                        nikunukiBasePoint_u4_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u5_Zenenn,
                        nikunukiBasePoint_u5_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d4_Zenenn,
                        nikunukiBasePoint_d4_Zenenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u6_Zenenn,
                        nikunukiBasePoint_u6_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d5_Zenenn,
                        nikunukiBasePoint_d5_Zenenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d6_Zenenn,
                        nikunukiBasePoint_d5_Zenenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u1_Kouenn,
                        nikunukiBasePoint_u1_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u2_Kouenn,
                        nikunukiBasePoint_u2_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d1_Kouenn,
                        nikunukiBasePoint_d1_Kouenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u3_Kouenn,
                        nikunukiBasePoint_u3_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d2_Kouenn,
                        nikunukiBasePoint_d2_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d3_Kouenn,
                        nikunukiBasePoint_d3_Kouenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u4_Kouenn,
                        nikunukiBasePoint_u4_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u5_Kouenn,
                        nikunukiBasePoint_u5_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d4_Kouenn,
                        nikunukiBasePoint_d4_Kouenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d6_Kouenn,
                        nikunukiBasePoint_d6_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d5_Kouenn,
                        nikunukiBasePoint_d5_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u6_Kouenn,
                        nikunukiBasePoint_u6_Kouenn_YokuatuRate,
                    ),
                ),
                makeSannkakuNikunukiObject(
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_d7_Kouenn,
                        nikunukiBasePoint_d7_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u8_Kouenn,
                        nikunukiBasePoint_u8_Kouenn_YokuatuRate,
                    ),
                    convertYokugennRateGaishuuyohakuToZahyou(
                        nikunukiBasePoint_u7_Kouenn,
                        nikunukiBasePoint_u7_Kouenn_YokuatuRate,
                    ),
                ),
            ]

            def caluculateOfAreaSankakuNikunuki(sankakkeiObject):
                (ax1, ay1) = (
                    sankakkeiObject["basepoint_1_vec"].x,
                    sankakkeiObject["basepoint_1_vec"].y,
                )
                (bx1, by1) = (
                    sankakkeiObject["basepoint_2_vec"].x,
                    sankakkeiObject["basepoint_2_vec"].y,
                )
                (cx1, cy1) = (
                    sankakkeiObject["basepoint_3_vec"].x,
                    sankakkeiObject["basepoint_3_vec"].y,
                )  # 1つ目の三角肉抜きの面積
                return abs((ax1 - cx1) * (by1 - ay1) - (ax1 - bx1) * (cy1 - ay1)) / 2

            def caluculateTorasuNikunuki(sannkakuObjectList):
                areaNikunuki = 0
                for object in sannkakuObjectList:
                    areaNikunuki += caluculateOfAreaSankakuNikunuki(object)
                return areaNikunuki

            # 計算値まとめ
            areayokuGata = caluculateOfareaYokugata()  # 肉抜きをしないときのリブ面積
            totalAreaOfNikunuki = caluculateTorasuNikunuki(
                sannkakuObjectList
            )  # 肉抜き面積の合計
            areaHalfRib = caluculationOfAreaHalfRib()  # halfRibの面積
            areaKetaana = areaKetaana()  # 桁穴の面積
            areaTotalRibu = areayokuGata - totalAreaOfNikunuki - areaKetaana  # 最終的なリブ面積
            lengthOfKetaanaMawari = lengthOfketaanaShu()  # 桁穴周
            lengthOfRibCaptotal = lehgthOfRibCap()  # リブキャップの長さ
            lengthOfPlanktotal = lengthOfPlank()  # プランク部分の長さ
            areaKouennHokyou = caluculationOfareaKouennHokyou()  # 後縁補強材の面積
            if k == 1 or k == n:
                areaEndRibHokyou = caluculationOfAreaEndRibHokyou()[0]
            else:
                areaEndRibHokyou = 0
            areaPlankTannArea = caluculationOfPlankEndHokyou()  # プランク端補強材の面積

            # excel出力用リストにまとめる
            excelareayokuGata.append(areayokuGata)
            excelareatotalAreaOfNikunuki.append(totalAreaOfNikunuki)
            excelareaHalfRib.append(areaHalfRib)
            excelareaTotalRibu.append(areaTotalRibu)
            excellengthOfKetaanaMawari.append(lengthOfKetaanaMawari)
            excelLengthOfRibCapTotal.append(lengthOfRibCaptotal)
            excelLengthOfPlankTotal.append(lengthOfPlanktotal)
            excelKouennHokyou.append(areaKouennHokyou)
            excelEndRibHokyou.append(areaEndRibHokyou)
            excelPlankEndHokyou.append(areaPlankTannArea)

        ####翼の重量計算を行う#####
        ribuTotalData = []  ##ここで翼の座標計算で求めた値を全翼に対してリストへ変換する
        for ribuNumber in range(0, numberOfRib):
            ribuData = [
                excelareayokuGata[ribuNumber],
                excelareaHalfRib[ribuNumber],
                excelareaTotalRibu[ribuNumber][0],
                excellengthOfKetaanaMawari[ribuNumber],
                excelLengthOfRibCapTotal[ribuNumber],
                excelLengthOfPlankTotal[ribuNumber],
                excelKouennHokyou[ribuNumber],
                generateRibuPatternList(numberOfRib)[ribuNumber],
                generateRibuAtuiList(numberOfRib)[ribuNumber],
                generataPlankAtumiList(numberOfRib, plankAtumi)[ribuNumber][0],
                excelEndRibHokyou[ribuNumber],
                excelPlankEndHokyou[ribuNumber],
            ]
            ribuTotalData.append(ribuData)

        # ribuTotalData[]にexcelから読みっとたデータが２次元配列で保持
        # 具体的には,
        # 肉抜き前リブ面積、半リブ面積の合計、最終的なリブ面積、桁穴周、リブキャップ長さ、プランク長さ、後縁補強材の面積、リブの種類（0:肉抜き無、１肉抜きアリ、２半リブ）、リブの厚み、プランク厚み,端リブ補強材面積(肉抜き無),プランク端補強材の面積の順

        def ribuWeight():  # リブのスタイロの部分の重量
            totalVolumeOfRib = 0  # リブの体積を保持する
            for ribData in ribuTotalData:  # リブの体積を計算する
                if ribData[7] == 1:  # 肉抜きを行う場合
                    volumeOfRib = ribData[2] * ribData[8]  # リブ面積＊リブ厚み
                    totalVolumeOfRib += volumeOfRib
                elif ribData[7] == 2:  # 半リブの場合
                    volumeOfRib = ribData[1] * ribData[8]
                    totalVolumeOfRib += volumeOfRib
                else:  # フルリブの場合
                    volumeOfRib = ribData[0] * ribData[8]
                    totalVolumeOfRib += volumeOfRib
            return totalVolumeOfRib * sutairoDensity

        def ribuFixWeight():  # 桁穴周りのリブ接着材重量
            totalLengthOfKetaanaMawari = 0  # 桁穴周の接着長さを保持する
            for ribData in ribuTotalData:  # 桁穴に対する接着長さを求める
                lengthOfkentaanaMawari = ribData[3] * 2
                totalLengthOfKetaanaMawari += lengthOfkentaanaMawari
            return totalLengthOfKetaanaMawari * ribFixKetaanaDensity

        # 端リブ補強材の肉抜きを行う場合は未考慮
        # 肉抜きアリで設定しても、肉抜きをしていない状態で出力される
        def tannRibuHokyou():
            totalWeightOfEndRibHokyou = 0
            if ribuTotalData[0][7] == 1:
                areaHokyouArea = ribuTotalData[0][10] * 2
                weightOfRibuHokyouTannribu = areaHokyouArea * tannribuHokyouDensity
                totalWeightOfEndRibHokyou += weightOfRibuHokyouTannribu
            if ribuTotalData[0][7] == 0:
                areaHokyouArea = ribuTotalData[0][10] * 2
                weightOfRibuHokyouTannribu = areaHokyouArea * tannribuHokyouDensity
                totalWeightOfEndRibHokyou += weightOfRibuHokyouTannribu
            if ribuTotalData[-1][7] == 1:
                areaHokyouArea = ribuTotalData[-1][10] * 2
                weightOfRibuHokyouTannribu = areaHokyouArea * tannribuHokyouDensity
                totalWeightOfEndRibHokyou += weightOfRibuHokyouTannribu
            if ribuTotalData[-1][7] == 0:
                areaHokyouArea = ribuTotalData[-1][10] * 2
                weightOfRibuHokyouTannribu = areaHokyouArea * tannribuHokyouDensity
                totalWeightOfEndRibHokyou += weightOfRibuHokyouTannribu
            return totalWeightOfEndRibHokyou

        def KouennHokyou():
            kouennHokyouArea = 0  # 後縁補強材の面積を保持
            kouennHokyouArea -= ribuTotalData[0][6]
            kouennHokyouArea -= ribuTotalData[-1][6]
            for ribData in ribuTotalData:
                areaKouennHokyou = ribData[6]
                if ribData[7] != 2:
                    kouennHokyouArea += areaKouennHokyou
            return kouennHokyouArea * tannribuHokyouDensity * 2

        def ribCapWeight():
            ribCapArea = 0  # リブキャップの面積を保持
            for ribData in ribuTotalData:  # リブキャップの面積を求める
                areaRibCap = ribData[4] * ribData[8]  # リブキャップの長さ＊リブの厚み
                if ribData[7] != 2:
                    ribCapArea += areaRibCap
            return ribCapArea * ribCapDensity

        def weightOfPlank():  # プランクの重量を求めるための関数　端リブのプランク長さを上辺、底辺、桁長さを高さ、厚みを持つ台形立体形として考える
            plankVolume = 0
            counter = 0
            while counter < numberOfRib:
                plankVolume += (
                    (ribuTotalData[counter][5] + ribuTotalData[counter - 1][5])
                    * (ketaLengthFrangeinsideToFrangeInside / (numberOfRib - 1))
                    * (ribuTotalData[counter][9])
                ) / 2
                counter = counter + 1
            return plankVolume * sutairoDensity

        def weightOfStringer():  # ストリンガーの重量を計算する
            stringerVolume = (
                lengthOfstringerSide1
                * lengthOFStringerSide2
                * ketaLengthFrangeinsideToFrangeInside
                * NumberOfStringer
            )
            stringerWeight = stringerVolume * densityOfStringer
            return stringerWeight

        def filmWeight():  # フィルムの重量を計算する 端リブのプランク長さ＋リブキャップ長さを上辺と底辺に設定して、桁の長さを高さとする台形で近似
            fileArea = 0
            counter = 0
            while counter < numberOfRib:
                fileArea += (
                    (
                        ribuTotalData[counter][4]
                        + ribuTotalData[counter][5]
                        + ribuTotalData[counter - 1][4]
                        + ribuTotalData[counter - 1][5]
                    )
                    * (ketaLengthFrangeinsideToFrangeInside / (numberOfRib - 1))
                ) / 2
                counter = counter + 1
            return fileArea * densityOfFilm

        def weightOfKoennzai():  # 後縁材の重量を求める
            weightOfSutairoCore = (
                densityOfKouennzai
                * ketaLengthFrangeinsideToFrangeInside
                * crosSectionalAreaKouennzai
            )
            weightOfCarbon = (
                kouennzaihokyouCarbondencity
                * ketaLengthFrangeinsideToFrangeInside
                * kouennzaihokyouCarbonwidth
            )
            return weightOfSutairoCore + weightOfCarbon

        def weightOf1Dstructure():
            return weightOfketa + weightOfFrange + weightOfKannzashi

        def weightOfRyoumennTeap():  # 両面テープの重量 ここについては、両面テープをはる位置によって要修正
            areaRyoumennTeap = 0  # 両面テープの面積を保持する変数
            for ribDate in ribuTotalData:
                ribRyoumennTeapArea = (ribDate[4] + ribDate[5]) * ribDate[8]  # リブの側面積
                areaRyoumennTeap += ribRyoumennTeapArea + ribDate[5] * ribDate[8]
            ribteapHorizonalForYokugann = (
                lengthOfKeta
                * numberOfRyoumennteapForVerticalForYokugenn
                * lengthOfstringerSide1
            )  # 桁に対して平行な両面テープ本数
            areaRyoumennTeap += ribteapHorizonalForYokugann
            return areaRyoumennTeap * densityOfRyoumennteap

        def weightOfPlankEndHokyou():
            areaPlankHokyou = 0  # プランク端補強材の面積を保持する変数
            for ribDate in ribuTotalData:
                addPlankHokyou = ribDate[11]
                areaPlankHokyou += addPlankHokyou
            return areaPlankHokyou * tannribuHokyouDensity * 2

        totalWeightOf2Dstructure = (
            ribuWeight()
            + ribuFixWeight()
            + tannRibuHokyou()
            + ribCapWeight()
            + weightOfStringer()
            + weightOfPlank()
            + filmWeight()
            + weightOfKoennzai()
            + weightOfRyoumennTeap()
            + weightOfPlankEndHokyou()
        )
        wingWeightList.append(totalWeightOf2Dstructure)
    yokuHennkei = caluculateYokuSurfaceDeviation(libSpan, tp)
    yoku2DStructureWight = sum(wingWeightList)
    outPutList.append([yoku2DStructureWight, yokuHennkei[0], tp, libSpan[0]])
    print(counter)
    if counter == 20:
        print("20パターン終了")
    elif counter == 40:
        print("40パターン終了")
    elif counter == 60:
        print("60パターン終了")

print("completed")
print("計算結果:", outPutList)
