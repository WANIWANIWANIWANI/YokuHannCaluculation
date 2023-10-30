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


# ファイル関連
# 出力するテキストファイルの名前。拡張子は不要
ProjectName = "1012"
# 翼型を保管しておき、コマンドファイルを出力するディレクトリのPath
Directory = r"C:\Users\ryota2002\Documents\三面図"


##三面図の情報
# 主翼の情報
KetaFutosa = [120, 110, 100, 89.75, 55, 30]
KetaNagasa = [1488, 2432, 3276, 2015, 3221, 3236]
KetaChuushin = [[37, 37], [37, 37], [37, 37], [37, 37], [37, 37], [37, 37]]
kouennzai = [[20, 20], [20, 20], [20, 20], [20, 20], [20, 20], [20, 20]]
Yokugenn = [1488, 1488, 1248, 1124, 1016, 743, 526]
Bunnkatu = 6
shuyokuKetugou = 100
plankStart = 60
Yokukann = 10

# 尾翼へと延びる桁
tailKetaLength_Zenenn = 1100
tailKetaLength_Kouenn = 4500
tailFutosa_Zenenn = 60
tailFutosa_Kouenn = 60

# 尾翼
# 尾翼のテール最後縁からの距離を入力する
biyokuIchi = 600
biyokuYokuGennRoot = 850
biyokuYokuGennEnd = 850
ketaLength_Biyoku = 2000
ketaana_Biyoku = 35
ketaFutosa_Biyoku = 60
plankStart_tail = 60
kouennzai_tail = 20
tailsetugou_Biyoku = 65

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


def lineRibu(
    Ribu_list,
    Keatfutosa,
    x_root_yoku,
    x_end_yoku,
    Root_Yokugenn,
    End_Yokugenn,
    kouenn,
    ketaIchi,
):
    ribu_counter = 0
    while ribu_counter < len(Ribu_list):
        r = 1 - ribu_counter / len(Ribu_list)
        c = Root_Yokugenn + (End_Yokugenn - Root_Yokugenn) * r
        print(c)
        Kouenn_c = c * (1 - ketaIchi / 100)
        print(Kouenn_c)
        if Ribu_list[ribu_counter] == 0:
            ribuZenenn_vec = vector(
                x_root_yoku + (x_end_yoku - x_root_yoku) * r, Kouenn_c - kouenn
            )
            ribuKouenn_vec = vector(
                x_root_yoku + (x_end_yoku - x_root_yoku) * r, -Keatfutosa / 2
            )
            line(file, ribuZenenn_vec, ribuKouenn_vec)
        ribu_counter += 1


os.chdir(Directory)  # ディレクトリ移動
file = open(f"{ProjectName}.txt", "w")

x = 0

x += shuyokuKetugou

##主翼を出力する部分
shuyokuCounter = 0
while shuyokuCounter < Bunnkatu:
    # 翼弦を出力する座標を計算
    RootYokuGenn = Yokugenn[shuyokuCounter]
    EndYokuGenn = Yokugenn[shuyokuCounter + 1]
    ZennennYokuGennRoot = RootYokuGenn * KetaChuushin[shuyokuCounter][0] / 100
    KouennYokuGennRoot = RootYokuGenn - ZennennYokuGennRoot
    ZennennYokuGennEnd = EndYokuGenn * KetaChuushin[shuyokuCounter][1] / 100
    KouennYokuGennEnd = EndYokuGenn - ZennennYokuGennEnd

    # x方向の座標移動を制御
    x_root = x
    x_end = x + KetaNagasa[shuyokuCounter]

    # 翼弦座標をベクトル変換
    RootZenenn_vec = vector(x_root, -ZennennYokuGennRoot)
    RootKouenn_vec = vector(x_root, +KouennYokuGennRoot)
    EndZenennn_vec = vector(x_end, -ZennennYokuGennEnd)
    EndKouenn_vec = vector(x_end, +KouennYokuGennEnd)
    # 桁の座標をベクトル変換
    RootZenenn_Keta_vec = vector(x_root, -KetaFutosa[shuyokuCounter] / 2)
    RootKouenn_Keta_vec = vector(x_root, KetaFutosa[shuyokuCounter] / 2)
    EndZenenn_keta_vec = vector(x_end, -KetaFutosa[shuyokuCounter] / 2)
    EndKouenn_keta_vec = vector(x_end, KetaFutosa[shuyokuCounter] / 2)

    print(
        vector(x_root, -KetaFutosa[shuyokuCounter] / 2),
        vector(x_root, KetaFutosa[shuyokuCounter] / 2),
        vector(x_end, -KetaFutosa[shuyokuCounter] / 2),
        vector(x_end, KetaFutosa[shuyokuCounter] / 2),
    )

    # プランクの座標を計算
    PlankRoot_y = RootYokuGenn * plankStart / 100 - ZennennYokuGennRoot
    PlankEnd_y = EndYokuGenn * plankStart / 100 - ZennennYokuGennEnd

    # 後縁材の座標を計算
    kouennzaiRoot_y = KouennYokuGennRoot - kouennzai[shuyokuCounter][0]
    kouennzaiEnd_y = KouennYokuGennEnd - kouennzai[shuyokuCounter][1]

    # プランクの座標をベクトルへ変換
    PlankRoot_vec = vector(x_root, PlankRoot_y)
    PlankEnd_vec = vector(x_end, PlankEnd_y)

    # 後縁材の座標をベクトルへ変換
    kouennzaiRoot_vec = vector(x_root, kouennzaiRoot_y)
    kouennzaiEnd_y_vec = vector(x_end, kouennzaiEnd_y)

    line(file, RootZenenn_vec, RootKouenn_vec)
    line(file, RootKouenn_vec, EndKouenn_vec)
    line(file, EndKouenn_vec, EndZenennn_vec)
    line(file, EndZenennn_vec, RootZenenn_vec)
    line(file, RootZenenn_Keta_vec, RootKouenn_Keta_vec)
    line(file, RootKouenn_Keta_vec, EndKouenn_keta_vec)
    line(file, EndKouenn_keta_vec, EndZenenn_keta_vec)
    line(file, EndZenenn_keta_vec, RootZenenn_Keta_vec)
    line(file, kouennzaiRoot_vec, kouennzaiEnd_y_vec)
    line(file, PlankRoot_vec, PlankEnd_vec)

    RibuList = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    lineRibu(
        RibuList,
        -KetaFutosa[shuyokuCounter],
        x,
        x + KetaNagasa[shuyokuCounter],
        RootYokuGenn,
        EndYokuGenn,
        kouennzai[shuyokuCounter][0],
        KetaChuushin[shuyokuCounter][0],
    )
    print(x, "x")
    print(x + KetaNagasa[shuyokuCounter] + Yokukann, "next")

    x += KetaNagasa[shuyokuCounter] + Yokukann
    shuyokuCounter += 1


##テールへと伸びる桁
# テール前縁側
line(file, vector(-tailFutosa_Zenenn / 2, 0), vector(tailFutosa_Zenenn / 2, 0))
line(
    file,
    vector(tailFutosa_Zenenn / 2, 0),
    vector(tailFutosa_Zenenn / 2, -tailKetaLength_Zenenn),
)
line(
    file,
    vector(tailFutosa_Zenenn / 2, -tailKetaLength_Zenenn),
    vector(-tailFutosa_Zenenn / 2, -tailKetaLength_Zenenn),
)
line(
    file,
    vector(-tailFutosa_Zenenn / 2, -tailKetaLength_Zenenn),
    vector(-tailFutosa_Zenenn / 2, 0),
)
# テール後縁部
line(file, vector(-tailFutosa_Kouenn / 2, 0), vector(tailFutosa_Kouenn / 2, 0))
line(
    file,
    vector(tailFutosa_Kouenn / 2, 0),
    vector(tailFutosa_Kouenn / 2, tailKetaLength_Kouenn),
)
line(
    file,
    vector(tailFutosa_Kouenn / 2, tailKetaLength_Kouenn),
    vector(-tailFutosa_Kouenn / 2, tailKetaLength_Kouenn),
)
line(
    file,
    vector(-tailFutosa_Kouenn / 2, tailKetaLength_Kouenn),
    vector(-tailFutosa_Kouenn / 2, 0),
)

# 尾翼の出力
x_Biyoku = 0
y_Biyoku_Keta = tailKetaLength_Kouenn - biyokuIchi
# 翼弦を出力する座標を計算
ZennennYokuGennRoot_tail = biyokuYokuGennRoot * ketaana_Biyoku / 100
KouennYokuGennRoot_tail = biyokuYokuGennRoot - ZennennYokuGennRoot_tail
ZennennYokuGennEnd_tail = biyokuYokuGennEnd * ketaana_Biyoku / 100
KouennYokuGennEnd_tail = biyokuYokuGennEnd - ZennennYokuGennEnd_tail
# x方向の座標移動を制御
x_Biyoku += tailsetugou_Biyoku / 2
x_root_Biyoku = x_Biyoku
x_end_Biyoku = x_root_Biyoku + ketaLength_Biyoku
# 翼弦座標をベクトル変換
RootZenenn_vec_tail = vector(x_root_Biyoku, y_Biyoku_Keta - ZennennYokuGennRoot_tail)
RootKouenn_vec_tail = vector(x_root_Biyoku, y_Biyoku_Keta + KouennYokuGennRoot_tail)
EndZenennn_vec_tail = vector(x_end_Biyoku, y_Biyoku_Keta - ZennennYokuGennRoot_tail)
EndKouenn_vec_tail = vector(x_end_Biyoku, y_Biyoku_Keta + KouennYokuGennEnd_tail)
# 桁の座標をベクトル変換
RootZenenn_Keta_vec_tail = vector(x_root_Biyoku, y_Biyoku_Keta - ketaFutosa_Biyoku / 2)
RootKouenn_Keta_vec_tail = vector(x_root_Biyoku, y_Biyoku_Keta + ketaFutosa_Biyoku / 2)
EndZenenn_keta_vec_tail = vector(x_end_Biyoku, y_Biyoku_Keta - ketaFutosa_Biyoku / 2)
EndKouenn_keta_vec_tail = vector(x_end_Biyoku, y_Biyoku_Keta + ketaFutosa_Biyoku / 2)
# プランクの座標を計算
PlankRoot_y_tail = biyokuYokuGennRoot * plankStart_tail / 100 - ZennennYokuGennRoot_tail
PlankEnd_y_tail = biyokuYokuGennEnd * plankStart_tail / 100 - ZennennYokuGennEnd_tail
# 後縁材の座標を計算
kouennzaiRoot_y_tail = y_Biyoku_Keta + KouennYokuGennRoot_tail - kouennzai_tail
kouennzaiEnd_y_tail = y_Biyoku_Keta + KouennYokuGennEnd_tail - kouennzai_tail
# プランクの座標をベクトルへ変換
PlankRoot_vec_tail = vector(x_root_Biyoku, PlankRoot_y_tail)
PlankEnd_vec_tail = vector(x_end_Biyoku, PlankEnd_y_tail)
# 後縁材の座標をベクトルへ変換
kouennzaiRoot_vec_tail = vector(x_root_Biyoku, kouennzaiRoot_y_tail)
kouennzaiEnd_vec_tail = vector(x_end_Biyoku, kouennzaiEnd_y_tail)
line(file, RootZenenn_vec_tail, RootKouenn_vec_tail)
line(file, RootKouenn_vec_tail, EndKouenn_vec_tail)
line(file, EndKouenn_vec_tail, EndZenennn_vec_tail)
line(file, EndZenennn_vec_tail, RootZenenn_vec_tail)
line(file, RootZenenn_Keta_vec_tail, RootKouenn_Keta_vec_tail)
line(file, RootKouenn_Keta_vec_tail, EndKouenn_keta_vec_tail)
line(file, EndKouenn_keta_vec_tail, EndZenenn_keta_vec_tail)
line(file, EndZenenn_keta_vec_tail, RootZenenn_Keta_vec_tail)
line(file, kouennzaiRoot_vec_tail, kouennzaiEnd_vec_tail)
line(file, PlankRoot_vec_tail, PlankEnd_vec_tail)


file.write("texted\n1\n")  # textをコマンドで入力できるように設定
file.write("-lweight\n0.001\n")  # 線の太さ設定

file.close
print("completed")
