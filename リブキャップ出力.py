# 設定

lengthOfRibCap = 7
directory = r"C:\Users\ryota2002\Documents\libu"  # 出力先のディレクトリー
projectName = "リブキャップtest1"  # 出力ファイル名
y_length = 297  # バルサ材の縦の長さ（A4：297mm）
x_length = 210  # バルサ材の横の長さ（A4:210mm）

# バルサ板にとる余白の大きさを指定する
x_margin_length = 10
y_margin_length = 10

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
line(file, [0, 0], [x_length, 0])
line(file, [x_length, 0], [x_length, y_length])
line(file, [x_length, y_length], [0, y_length])
line(file, [0, y_length], [0, 0])


# バルサ材の余白部分を出力
line(
    file,
    [x_margin_length, y_margin_length],
    [x_margin_length, y_length - x_margin_length],
)
line(
    file,
    [x_margin_length, y_length - x_margin_length],
    [x_length - x_margin_length, y_length - y_margin_length],
)

line(
    file,
    [x_length - x_margin_length, y_margin_length],
    [x_margin_length, y_margin_length],
)

xAllForthisProgram = x_margin_length  # プログラムを制御するための変数(x軸) 初期値は、ｘ軸の余白分だけ移動した点
while xAllForthisProgram + lengthOfRibCap <= x_length - x_margin_length:
    line(
        file,
        [xAllForthisProgram, y_margin_length],
        [xAllForthisProgram, y_length - y_margin_length],
    )
    xAllForthisProgram += lengthOfRibCap
    line(
        file,
        [xAllForthisProgram, y_margin_length],
        [xAllForthisProgram, y_length - y_margin_length],
    )


file.close
print("completed")
