import pandas as pd

# 各定数を以下で設定する（試作）
ribFixKetaanaDensity = 0.0070  # 桁穴周りの接着剤の密度（g/(桁穴1mm)
tannribuHokyouDensity = 0.00078  # 端リブ補強材（バルサ＋ボンド）の密度（g / mm²）
ribCapDensity = 0.00074  # リブキャップの密度（g/リブキャップ１mm²）
densityOfKouennzai = 0.0001800  # 後縁材の値を求める（g/mm³） つまり、2024的にはバルサの密度を書けばよい
densityOfStringer = 0.0001800  # ストリンガーの密度（ｇ/mm³） つまり、2024的にはバルサの密度を書けばよい
densityOfRyoumennteap = 0.000033  # 両面テープの密度（g/mm2）

# １次構造
weightOfketa = 516  # 桁の重量(g)
weightOfFrange = 131  # フランジの重量
weightOfKannzashi = 0  # かんざしの重量

# 既知の値
lengthOfKeta = 2433  # 桁の長さ
numberOfRyoumennteapForVerticalForYokugenn = 7  # 翼弦に対して垂直な方向の両面テープ数
sutairoDensity = 0.000030  # スタイロの密度(g/mm3)
ketaLengthFrangeinsideToFrangeInside = 2433  # 桁長さ
NumberOfStringer = 6  # ストリンガーの本数
lengthOfstringerSide1 = 5  # ストリンガーの一辺の長さ
lengthOFStringerSide2 = 5  # ストリンガーの一辺の長さ
densityOfFilm = 0.0000002  # フィルムの密度（ｇ/mm³）
crosSectionalAreaKouennzai = 200  # 後縁材の断面積（mm²）

##両面テープに関する設定
# 翼弦平行成分
NumberOfRyoumennTeapForYokugenn = 20  # 翼弦方向の両面テープの本数を入力する
averageWidesOfRyoumennTeapForYokugenn = 7  # 翼弦方向の両面テープの平均幅(mm)を入力する
# 翼弦垂直成分
NumberOfRyoumennTeapForKeta = 6  # 桁方向の両面テープの本数を入力する
averageWidesOfRyoumennTeapForKeta = 10  # 桁方向の両面テープの平均幅(mm)を入力する

# 読み取りファイルと書き出しファイルの設定a
yokuNumber = "16期1yoku"  # 条件を記入
readingFilePath = r"C:\Users\ryota2002\Documents\libu\16期1翼重量9月.xlsx"

# リブ枚数
numberOfRib = 16


# Excelファイルの取り込み
filename = readingFilePath
xlsdata = pd.read_excel(filename, sheet_name=0)
data = xlsdata
print(data)
ribuTotalData = []
for row in data.itertuples():
    if row == 0:
        break
    ribuDataPartial = []
    for k in range(2, 14):
        ribuDataPartial.append(row[k])
    ribuTotalData.append(ribuDataPartial)
print(ribuTotalData)
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
    return kouennHokyouArea * tannribuHokyouDensity


def ribCapWeight():
    ribCapArea = 0  # リブキャップの面積を保持
    for ribData in ribuTotalData:  # リブキャップの面積を求める
        areaRibCap = ribData[4] * ribData[8]  # リブキャップの長さ＊リブの厚み
        if ribData[7] != 2:
            ribCapArea += areaRibCap
    return ribCapArea * ribCapDensity


def weightOfPlank():  # プランクの重量を求めるための関数　端リブのプランク長さを上辺、底辺、桁長さを高さ、厚みを持つ台形立体形として考える
    plankVolume = (ribuTotalData[0][5] + ribuTotalData[0][9] / 2) + (
        ribuTotalData[-1][5] + ribuTotalData[0][9] / 2
    ) * ketaLengthFrangeinsideToFrangeInside * (1 / 2)
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
    areaOfYoku = (
        (
            (ribuTotalData[0][4] + ribuTotalData[0][5])
            + (ribuTotalData[-1][5] + ribuTotalData[-1][4])
        )
        * ketaLengthFrangeinsideToFrangeInside
        / 2
    )  # 翼表面積
    return areaOfYoku * densityOfFilm


def weightOfKoennzai():  # 後縁材の重量を求める
    return (
        densityOfKouennzai
        * ketaLengthFrangeinsideToFrangeInside
        * crosSectionalAreaKouennzai
    )


def weightOf1Dstructure():
    return weightOfketa + weightOfFrange + weightOfKannzashi


def weightOfRyoumennTeap():  # 両面テープの重量 ここについては、両面テープをはる位置によって要修正
    areaRyoumennTeap = 0  # 両面テープの面積を保持する

    # 翼弦成分に関して計算
    ribLengthTotal = 0
    for ribDate in ribuTotalData:  # リブの側面の長さを計算（各リブの側面長さを平均）
        ribRyoumennTeapArea = ribDate[4] + ribDate[5]
        ribLengthTotal += ribRyoumennTeapArea
    averageLengthOfYokugenn = ribLengthTotal / len(ribuTotalData)
    areaRyoumennTeap += (
        averageLengthOfYokugenn
        * NumberOfRyoumennTeapForYokugenn
        * averageWidesOfRyoumennTeapForYokugenn
    )
    # 桁平行成分に関して計算
    areaRyoumennTeap += (
        ketaLengthFrangeinsideToFrangeInside
        * NumberOfRyoumennTeapForKeta
        * averageWidesOfRyoumennTeapForKeta
    )
    return areaRyoumennTeap * densityOfRyoumennteap


def weightOfPlankEndHokyou():
    areaPlankHokyou = 0  # プランク端補強材の面積を保持する変数
    for ribDate in ribuTotalData:
        addPlankHokyou = ribDate[11]
        areaPlankHokyou += addPlankHokyou
    return areaPlankHokyou * tannribuHokyouDensity


# excelファイル出力用の値が保持される変数
totalWeightOfRib = ribuWeight()
totalWeightOfRibFixingAroundKetaMawari = ribuFixWeight()
totalWeightOfRibTannribuHokyou = tannRibuHokyou()
totalWeightOfRibCap = ribCapWeight()
totalWeightOfKouennHokyou = KouennHokyou()
totalWeightOfPlank = weightOfPlank()
totalWeightOfStringer = weightOfStringer()
totalWeightOfFilm = filmWeight()
totalWeightOfKouennzai = weightOfKoennzai()
totalWeightOfRyoumennTeap = weightOfRyoumennTeap()
totalweightOfPlnkEnd = weightOfPlankEndHokyou()
totalWeightOf1Dstructure = weightOf1Dstructure()
totalWeightOf2Dstructure = (
    totalWeightOfRib
    + totalWeightOfRibFixingAroundKetaMawari
    + totalWeightOfRibTannribuHokyou
    + totalWeightOfRibCap
    + totalWeightOfStringer
    + totalWeightOfPlank
    + totalWeightOfFilm
    + totalWeightOfKouennzai
    + totalWeightOfRyoumennTeap
    + totalweightOfPlnkEnd
)
totalWeightOfYoku = totalWeightOf1Dstructure + totalWeightOf2Dstructure
rateOfNikunuki = 1 - ribuTotalData[0][2] / ribuTotalData[0][0]
# excelファイルへの書き出し
df = pd.DataFrame(
    {
        "翼番号": [yokuNumber],
        "スタイロ重量(g)": [totalWeightOfRib],
        "アセンブリ接着剤の重量(g)": [totalWeightOfRibFixingAroundKetaMawari],
        "端リブ補強材の重量(g)": [totalWeightOfRibTannribuHokyou],
        "後縁補強材の重量(g)": [totalWeightOfKouennHokyou],
        "リブキャップの重量(g)": [totalWeightOfRibCap],
        "ストリンガーの重量(g)": [totalWeightOfStringer],
        "プランクの重量(g)": [totalWeightOfPlank],
        "フィルムの重量(g)": [totalWeightOfFilm],
        "後縁材の重量(g)": [totalWeightOfKouennzai],
        "両面テープの重量(g)": [totalWeightOfRyoumennTeap],
        "プランク端補強材の重量": [totalweightOfPlnkEnd],
        "2次構造の重量(g)": [totalWeightOf2Dstructure],
        "1次構造の重量(g)": [totalWeightOf1Dstructure],
        "翼の総重量(g)": [totalWeightOfYoku],
        "リブ枚数": [numberOfRib],
        "肉抜き率": [rateOfNikunuki],
    }
)
with pd.ExcelWriter(
    readingFilePath, engine="openpyxl", mode="a", if_sheet_exists="new"
) as writer:
    df.to_excel(writer, sheet_name=yokuNumber, index=False)

print("completed")
