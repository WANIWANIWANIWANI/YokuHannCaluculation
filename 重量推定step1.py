# -------------------------------------------------------------------------
# 使いかた
# 下記Directoryに翼型をすべていれておく。必要に応じて変える。
# 翼型は 後縁->上->前縁->下->後縁 の順になっていることを確認
# 翼弦長などの定義に注意(特にこれ大事)
# 三角肉抜きが変な形になるときは、w_triやr_triを小さく調整するとよい
# ただし、小さくしすぎるとリブが折れるかもしれないので気を付ける

# 使いかたおわり
# ----------------------------------------------------------------------------------------
# 設定

# ファイル関連
# 翼型を保管しておき、コマンドファイルを出力するディレクトリのPath
Directory = r"C:\Users\ryota2002\Documents\libu"
ProjectName = "aaa"

# 翼関連
# 端、根の翼弦長(流れ方向)[mm]
RootChord = 1288
EndChord = 1288
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
PlaneNumber = "0"
# 半リブあり?
use_half = False

# リブ以外の要素関連
# プランク厚さ[mm]
tp = 2
# ストリンガー断面の一辺[mm]
e = 5
# リブキャップ厚さ[mm]
t = 1
# 桁径[mm]	楕円の短軸方向
# 49.5
d = 132.52
# 桁径		楕円の長軸-短軸 円なら0
dd = 133.59 - d
# アセンブリ棒径[mm]
da = 30
# アセンブリ棒余白[mm]
h = 7
# 後縁材の前縁側の辺の長さ[mm]
ht = 8
# 前縁材があるか boolean
use_l = False
# 前縁材の端線、水平線,offset線の出力
use_la = False
# 前縁材と翼型の前縁のずれ[mm]
lo = 10
# 前縁材のoffset[mm]
offset_l = 1
# 三角肉抜き最小骨格幅[mm]
w_tri = 13
# 三角肉抜き端半径[mm]
r_tri = 4
# 前縁-肉抜き 長さ[%]
first_light_r = 8
# 丸肉抜き 最小骨格幅[mm]
w_circle = 20


##適当に入力してもOK数値計算には関係ない
# 位置関連
# プランク上開始位置[%]
rpu = 60
# プランク下開始位置[%] r plank downside
rpd = EndR - 100 * (d / 2 + 30) / EndChord
# ストリンガー下後縁側位置[%] r stringer downside trailing edge
rsdt = rpd + 20
# ストリンガー前縁[mm] x stringer leading edge
xsl = 20 + e

# 機体諸元
# 0翼取り付け角[°](定常飛行迎角)
alpha = 0
# 後退角(リブ厚みの修正用)[°]
sweep = 0


# 設定おわり
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
    file.write(
        """line
{ax},{ay}
{bx},{by}
{cx},{cy}
{dx},{dy}
{ax},{ay}

line
{ax},{ay}
{cx},{cy}

line
{bx},{by}
{dx},{dy}

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
    print(str(FoilPs[0][0]) + str(FoilPs[1][0]))
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

# excel出力用のリスト
excelareayokuGata = []
excelareatotalAreaOfNikunuki = []
excelareaTotalRibu = []
excellengthOfKetaanaMawari = []
excelLengthOfRibCapTotal = []
excelLengthOfPlankTotal = []
excelTeaperRatio = []
excelLengthOfKetaCenterToKouenn = []


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

    # 中心線の関数、点のリスト
    s = numpy.linspace(0, x_d[-1], 50)  # 端で定義域を狭くするのは計算誤差でf_uの定義域を超えないため。
    f_camber = inter(s, (f_u(s) + f_d(s)) / 2)  # 上下の翼型の関数の平均であると近似 特に前縁付近は信用できない
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

    # 桁穴の出力 y座標は25%のcamber位置で固定
    delta = RootDelta + (EndDelta - RootDelta) * r
    RibAngle = math.atan(tan((alpha + delta) * numpy.pi / 180) * cos(sweep))
    Pipe_C = vector(x_pipe, f_camber(x_25pc))
    Pipe = ellipse(
        Pipe_C, Pipe_C + vector(0, 1).rotate(RibAngle, "radian") * (d + dd) / 2, d / 2
    )

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

    # 三角肉抜き出力
    # 三角形の頂点の円
    x_tri_lead = c * cos(sweep) * first_light_r / 100  # 最外
    x_tri_trail = Pipe_C.x - Pipe.b - w_tri
    # 三角形の頂点の中心のx,y座標のリスト
    # 前縁側 左下、右下、上の順
    x_tl = [x_tri_lead, (x_tri_lead + x_tri_trail) / 2]  # 2つ目まで
    y_tl = [
        f_d(x_tl[0]) + w_tri + r_tri,
        f_d(x_tl[1]) + w_tri + r_tri,
        f_u(x_tl[1]) - w_tri - r_tri,
    ]
    x_tl = x_tl + [
        x_tl[1] - (y_tl[2] - y_tl[1]) * tan((2 * r_tri + w_tri) / (y_tl[2] - y_tl[1]))
    ]
    y_tl[2] = f_u(x_tl[2]) - w_tri - r_tri
    tri_lead_circles = [circle(r_tri, vector(x_tl[i], y_tl[i])) for i in range(3)]
    tri_lead_lines = [
        offset([tri_lead_circles[i - 1].O, tri_lead_circles[i].O], r_tri, 1, 1)
        for i in range(3)
    ]
    # 前縁側 右上、左上、下の順
    x_tt = [x_tri_trail, x_tl[1]]
    y_tt = [
        f_u(x_tt[0]) - w_tri - r_tri,
        f_u(x_tt[1]) - w_tri - r_tri,
        f_u((x_tri_lead + x_tri_trail) / 2) - w_tri - r_tri,
    ]
    x_tt = x_tt + [
        x_tt[1] + (y_tl[2] - y_tl[1]) * tan((2 * r_tri + w_tri) / (y_tl[2] - y_tl[1]))
    ]
    y_tt[2] = f_d(x_tt[2]) + w_tri + r_tri
    tri_trail_circles = [circle(r_tri, vector(x_tt[i], y_tt[i])) for i in range(3)]
    tri_trail_lines = [
        offset([tri_trail_circles[i - 1].O, tri_trail_circles[i].O], r_tri, 1, 1)
        for i in range(3)
    ]

    # 丸肉抜き出力 前縁から
    # 最前縁の丸の中心の座標
    x_cir = Pipe.C.x + (d + dd) / 2
    x_cir += (f_u(x_cir) - f_d(x_cir)) / 2
    light_Cs = [
        circle((f_u(x_cir) - f_d(x_cir)) / 2 - w_circle, vector(x_cir, f_camber(x_cir)))
    ]
    i = 1
    while True:
        x_cir = light_Cs[i - 1].O.x + light_Cs[i - 1].r
        x_cir += (f_u(x_cir) - f_d(x_cir)) / 2
        light_Cs += [
            circle(
                (f_u(x_cir) - f_d(x_cir)) / 2 - w_circle, vector(x_cir, f_camber(x_cir))
            )
        ]
        # Assembly棒より前縁側にあるとき
        if not light_Cs[i].O.x + light_Cs[i].r < Assembly.O.x - Assembly.r - w_circle:
            light_Cs = light_Cs[:-1]  # 被ったのはとりのぞく
            break
        i += 1

    # リブのデータ書き出しおわり
    # 以下では、リブの面積を計算する
    # 計算式の定義
    def caluculateOfareaYokugata():
        areaYokugataUpper = -integrate.trapz(y_u, x_u)
        areaYokugataDown = -integrate.trapz(y_d, x_d)
        return areaYokugataUpper + areaYokugataDown

    def caluculateOfAreaSankakuNikunuki():
        (ax1, ay1) = (x_tl[0], y_tl[0])
        (bx1, by1) = (x_tl[1], y_tl[1])
        (cx1, cy1) = (x_tl[2], y_tl[2])  # 1つ目の三角肉抜きの面積
        (ax2, ay2) = (x_tt[0], y_tt[0])
        (bx2, by2) = (x_tt[1], y_tt[1])
        (cx2, cy2) = (x_tt[2], y_tt[2])  # 2つ目の三角肉抜きの面積
        return (
            abs((ax1 - cx1) * (by1 - ay1) - (ax1 - bx1) * (cy1 - ay1)) / 2
            + abs((ax2 - cx2) * (by2 - ay2) - (ax2 - bx2) * (cy2 - ay2)) / 2
        )

    def caluculationOfAreaMaruNikunuki():
        x_cir = Pipe.C.x + (d + dd) / 2
        x_cir += (f_u(x_cir) - f_d(x_cir)) / 2
        light_Cs = [
            circle(
                (f_u(x_cir) - f_d(x_cir)) / 2 - w_circle, vector(x_cir, f_camber(x_cir))
            )
        ]
        areaCirculeNikunuki = 3.14 * (light_Cs[0].r) * (light_Cs[0].r)
        i = 1
        while True:
            x_cir = light_Cs[i - 1].O.x + light_Cs[i - 1].r
            x_cir += (f_u(x_cir) - f_d(x_cir)) / 2
            light_Cs += [
                circle(
                    (f_u(x_cir) - f_d(x_cir)) / 2 - w_circle,
                    vector(x_cir, f_camber(x_cir)),
                )
            ]
            areaCirculeNikunuki += 3.14 * (light_Cs[i].r) * (light_Cs[i].r)
            # アセンブリ棒よりも前縁にある時
            if (
                not light_Cs[i].O.x + light_Cs[i].r
                < Assembly.O.x - Assembly.r - w_circle
            ):
                light_Cs = light_Cs[-1]
                break
            i += 1
        return areaCirculeNikunuki

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

    # 計算値まとめ
    areayokuGata = caluculateOfareaYokugata()  # 肉抜きをしないときのリブ面積
    areaSankakuNikunuki = caluculateOfAreaSankakuNikunuki()  # リブの三角抜き面積
    areaMaruNikunuki = caluculationOfAreaMaruNikunuki()  # リブの円形肉抜き面積
    totalAreaOfNikunuki = areaSankakuNikunuki + areaMaruNikunuki  # 肉抜き面積の合計
    areaKetaana = areaKetaana()  # 桁穴の面積
    areaTotalRibu = areayokuGata - totalAreaOfNikunuki - areaKetaana  # 最終的なリブ面積
    lengthOfKetaanaMawari = lengthOfketaanaShu()  # 桁穴周
    lengthOfRibCaptotal = lehgthOfRibCap()  # リブキャップの長さ
    lengthOfPlanktotal = lengthOfPlank()
    teaperRatio = teaperRation()

    # excel出力用リストにまとめる
    excelareayokuGata.append(areayokuGata)
    excelareatotalAreaOfNikunuki.append(totalAreaOfNikunuki)
    excelareaTotalRibu.append(areaTotalRibu)
    excellengthOfKetaanaMawari.append(lengthOfKetaanaMawari)
    excelLengthOfRibCapTotal.append(lengthOfRibCaptotal)
    excelLengthOfPlankTotal.append(lengthOfPlanktotal)
    excelTeaperRatio.append(teaperRatio)
    excelLengthOfKetaCenterToKouenn.append(excelLengthOfKetaCenterToKouenn)

# excelファイルへの書き出し
import pandas as pd

df = pd.DataFrame(
    {
        "肉抜き前リブ面積(mm2)": excelareayokuGata,
        "肉抜き面積の合計(mm2)": excelareatotalAreaOfNikunuki,
        "最終的なリブ面積（桁穴面積考慮済み）(mm2)": excelareaTotalRibu,
        "桁穴周(mm)": excellengthOfKetaanaMawari,
        "リブキャップ長さ(mm)": excelLengthOfRibCapTotal,
        "プランク長さ(mm)": excelLengthOfPlankTotal,
        "テーパー比": excelTeaperRatio,
    }
)
df.to_excel("./0530test2.xlsx")  # ここに出力したいファイル名を設定する

print("completed")
