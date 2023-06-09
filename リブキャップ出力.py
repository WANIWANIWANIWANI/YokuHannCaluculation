# 設定

lengthOfRibCap = 7
directory = r"C:\Users\ryota2002\Documents\libu"  # 出力先のディレクトリー
projectName = "リブキャップtest1"  # 出力ファイル名
verticalLength = 297  # バルサ材の縦の長さ（A4：297mm）
horizonalLengt = 210  # バルサ材の横の長さ（A4:210mm）

# 以下、出力用のファイルを作成する
import os

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
line(file, [0, 0], [horizonalLengt, 0])
line(file, [horizonalLengt, 0], [horizonalLengt, verticalLength])
line(file, [horizonalLengt, verticalLength], [0, verticalLength])
line(file, [0, verticalLength], [0, 0])

# バルサ板にとる余白の大きさを指定する
marginhorizonal = 10
marginvertical = 10

# バルサ材の余白部分を出力
line(
    file,
    [marginhorizonal, marginvertical],
    [marginhorizonal, verticalLength - marginhorizonal],
)
line(
    file,
    [marginhorizonal, verticalLength - marginhorizonal],
    [horizonalLengt - marginhorizonal, verticalLength - marginvertical],
)

line(
    file,
    [horizonalLengt - marginhorizonal, marginvertical],
    [marginhorizonal, marginvertical],
)

xAllForthisProgram = marginhorizonal  # プログラムを制御するための変数(x軸) 初期値は、ｘ軸の余白分だけ移動した点
while xAllForthisProgram + lengthOfRibCap <= horizonalLengt - marginhorizonal:
    line(
        file,
        [xAllForthisProgram, marginvertical],
        [xAllForthisProgram, verticalLength - marginvertical],
    )
    xAllForthisProgram += lengthOfRibCap
    line(
        file,
        [xAllForthisProgram, marginvertical],
        [xAllForthisProgram, verticalLength - marginvertical],
    )


file.close
print("completed")
