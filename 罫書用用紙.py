# 設定
# 印刷時にA4でコピーすることを想定

lengthOfInterval = 50  # 4分割を行う際の１区間の長さ
numberOfPart = 4  # １枚のA4用紙から何枚の用紙が欲しいか？
directory = r"C:\Users\ryota2002\Documents\libu"  # 出力先のディレクトリー
projectName = "罫書用紙test1"  # 出力ファイル名
y_length = 297  # 用紙の縦の長さ（A4：297mm）
x_length = 210  # 用紙の横の長さ（A4:210mm）
marginRight = 10  # 余白設定
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

# １枚から取り出す罫書用紙の枚数を基に長さを計算
wideOfUseableLength = x_length - 10  # 余白右除いた長さ
lengthOfOnePart = wideOfUseableLength / numberOfPart  # １区間（左側の余白＋罫書用紙１枚の横幅）
lengthOfLightMargin = lengthOfOnePart * 0.20  # 20％分を余白へ
lengthOfKegaki = lengthOfOnePart * 0.80  # 80%分を余白へ

xAllForthisProgram = 0  # プログラムを制御するための変数(x軸)
while xAllForthisProgram <= x_length:
    xAllForthisProgram += lengthOfLightMargin
    line(file, [xAllForthisProgram, 0], [xAllForthisProgram, 297])
    xAllForthisProgram += lengthOfKegaki
    line(file, [xAllForthisProgram, 0], [xAllForthisProgram, 297])

yAllForThisProgram = 0
while yAllForThisProgram <= y_length:
    yAllForThisProgram += lengthOfInterval
    line(file, [0, yAllForThisProgram], [210, yAllForThisProgram])

file.close
print("completed")
