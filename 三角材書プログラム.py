# 設定
# ファイル設定
directory = r"C:\Users\ryota2002\Documents\libu"  # 出力先のディレクトリー
projectName = "三角材test1"  # 出力ファイル名

## バルサ材の大きさ設定
x_Length = 297  # 用紙の縦の長さ（A4：297mm）
y_Length = 210  # 用紙の横の長さ（A4:210mm）

## 三角材の寸法、枚数の指定を行う
lengthVerticalForRib = 10  # リブに対して垂直な方向の長さを指定
lengthHorizonalForKeta = 10  # 桁に対して平行方向の長さを指定
requiredPart = 30  # 同一テーパーで必要な枚数

##後縁材の傾き導出
# 端、根の桁位置[%]
RootR = 31
EndR = 31
# 端、根の翼弦長(流れ方向)[mm]
RootChord = 1288
EndChord = 700
# 桁の長さ
lengthOfKeta = 2000

##三角補強材について
# 出力したい部品の枚数を指定する
numberOfParts = 30


##出力に設定
margin = 5

# 以下、出力用のファイルを作成する
import os
import numpy

os.chdir(directory)  # ディレクトリ移動

file = open(f"{projectName}.txt", "w")

file.write("texted\n1\n")  # textをコマンドで入力できるように設定
file.write("-lweight\n0.001\n")  # 線の太さ設定


def line(file, P1, P2):
    """
    点P1,P2(vector)を結ぶ線分を描くコマンドをfileに出力
    """
    file.write(f"line\n{P1[0]},{P1[1]}\n{P2[0]},{P2[1]}\n\n")


def color(file, r, g, b):
    """
    r,g,bで次から出力するオブジェクトの色を変えるコマンドをfileに出力
    """
    file.write(f"-color\nt\n{r},{g},{b}\n")


# A4用紙の外形を書く
color(file, 0, 0, 255)
line(file, [0, 0], [x_Length, 0])
line(file, [x_Length, 0], [x_Length, -y_Length])
line(file, [x_Length, -y_Length], [0, -y_Length])
line(file, [0, -y_Length], [0, 0])

## 三角材のリブに接する面の角度を求める（変数名teaperAngleで保持する）
rootLengthOfKetaCenterToendpoint = (
    RootChord * (100 - RootR) / 100
)  # 根のリブに対する桁穴中心からリブ末端までの距離を保持
endLengthOfKetaCenterToendpoint = (
    EndChord * (100 - EndR) / 100
)  # 端のリブに対する桁穴と中心からリブ末端までの距離を保持
teaperAngle_radian = numpy.arctan((RootChord - EndChord) / lengthOfKeta)
teaperAngle_degree = numpy.rad2deg(teaperAngle_radian)  # 三角補強材のテーパー比
sannkakuZaiAngle_degree = 90 + teaperAngle_degree

# ここから繰り返し処理を行い必要枚数分の出力を行う（設定値のrequiredPartsに必要枚数は保持されていた）
counterOfparts = 0
O = [5, -5]  # 各補強材に対して定義を行うための原点(土台の端からはずらしてスタート)
if counterOfparts <= numberOfParts:
    counterOfparts += 1
    if counterOfparts > 1:
        O[1] = -(lengthVerticalForRib + margin)  # 上下方向に空白を空ける この値は自由に設定
    if O[1] + lengthVerticalForRib + margin < y_Length:
        O[0] += margin + lengthHorizonalForKeta
        O[1] = margin  # Y軸方向に対して設定した用紙の大きさに入らなくなったらx軸方向へ出力移動
    P1 = numpy.add(O, [0, lengthVerticalForRib])
    # テーパー比を考慮して、P2座標を求める
    ArrayP1ToP2 = [
        lengthHorizonalForKeta * numpy.cos(sannkakuZaiAngle_degree),
        lengthHorizonalForKeta * numpy.sin(sannkakuZaiAngle_degree),
    ]
    P2 = numpy.add(P1, ArrayP1ToP2)

    if O[0] + margin + lengthHorizonalForKeta < x_Length:
        # AutoCadコマンドを生成する
        line(file, O, P1)
        line(file, P1, P2)
        line(file, P2, O)
file.close
print("completed")
