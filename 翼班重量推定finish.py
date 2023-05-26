import pandas as pd
#各定数を以下で設定する（試作）
ribFixKetaanaDensity=100 #桁穴周りの接着剤の密度（g/(桁穴1mm)
tannribuHokyouDensity=50#端リブ補強材（バルサ＋ボンド）の密度（g / mm²）
ribCapDensity=50 #リブキャップの密度（g/リブキャップ１mm²）

#既知の値
weightOfketa=1000   #桁の重量(g)
weightOfFrange=200 #フランジの重量
weightOfKannzashi=200 #かんざしの重量
sutairoDensity=1.8 #スタイロの密度
densityOfKouennzai=1.9   #後縁材の値を求める（g/mm³） つまり、2024的にはバルサの密度を書けばよい
densityOfStringer    =2.0       #ストリンガーの密度（ｇ/mm³） つまり、2024的にはバルサの密度を書けばよい
ketaLengthFrangeinsideToFrangeInside=20000 #桁長さ
NumberOfStringer=6                 #ストリンガーの本数
lengthOfstringerSide1=5       #ストリンガーの一辺の長さ
lengthOFStringerSide2=5      #ストリンガーの一辺の長さ
densityOfFilm    =2   #フィルムの密度（ｇ/mm³）
crosSectionalAreaKouennzai=100#後縁材の断面積（mm²）

#読み取りファイルと書き出しファイルの設定
yokuNumber="2翼" #何翼？（数字＋翼）
readingFilePath=r"C:\Users\ryota2002\Documents\libu\development_test_data.xlsx"
exportReadingFilepath='./development_test_output5.xlsx'

#Excelファイルの取り込み
filename = readingFilePath
xlsdata = pd.read_excel(filename, sheet_name=0)
data = xlsdata
print(data)
ribuTotalData=[]
for row in data.itertuples():
    if(row==0):
        break
    ribuDataPartial=[]
    for k in range(2,12):
        ribuDataPartial.append(row[k])
    ribuTotalData.append(ribuDataPartial)
print(ribuTotalData)
#ribuTotalData[]にexcelから読みっとたデータが２次元配列で保持
# 具体的には,
# 肉抜き前リブ面積、肉抜き面積の合計、最終的なリブ面積、桁穴周、リブキャップ長さ、プランク長さ、テーパー比、肉抜きの有無（1;肉抜き、2:肉抜きなし）、リブの厚み、プランク厚みの順

def ribuWeight():#リブのスタイロの部分の重量
    totalVolumeOfRib=0 #リブの体積を保持する
    for ribData in ribuTotalData:#リブの体積を計算する
        if(ribData[7]==1):#肉抜きを行う場合
            volumeOfRib=ribData[2]*ribData[8]#リブ面積＊リブ厚み
            totalVolumeOfRib+=volumeOfRib
        else:
            volumeOfRib=ribData[0]*ribData[8]
            totalVolumeOfRib+=totalVolumeOfRib
    return totalVolumeOfRib*sutairoDensity
def ribuFixWeight():#桁穴周りのリブ接着材重量
        totalLengthOfKetaanaMawari=0 #桁穴周の接着長さを保持する
        for ribData in ribuTotalData:#桁穴に対する接着長さを求める
             lengthOfkentaanaMawari=ribData[4]*2
             totalLengthOfKetaanaMawari+=lengthOfkentaanaMawari
        return totalLengthOfKetaanaMawari*ribFixKetaanaDensity
def tannRibuHokyou():
     totalWeightOfEndRibHokyou=0
     if(ribuTotalData[0][7]==1):
           areaHokyouArea=ribuTotalData[0][2]*2
           weightOfRibuHokyouTannribu=areaHokyouArea*tannribuHokyouDensity
     if(ribuTotalData[0][7]==0):
           areaHokyouArea=ribuTotalData[0][0]*2
           weightOfRibuHokyouTannribu=areaHokyouArea*tannribuHokyouDensity
           totalWeightOfEndRibHokyou +=weightOfRibuHokyouTannribu
     if(ribuTotalData[-1][7]==1):
           areaHokyouArea=ribuTotalData[0][2]*2
           weightOfRibuHokyouTannribu=areaHokyouArea*tannribuHokyouDensity
           totalWeightOfEndRibHokyou +=weightOfRibuHokyouTannribu
     if(ribuTotalData[-1][7]==0):
           areaHokyouArea=ribuTotalData[0][0]*2
           weightOfRibuHokyouTannribu=areaHokyouArea*tannribuHokyouDensity
           totalWeightOfEndRibHokyou +=weightOfRibuHokyouTannribu
     return totalWeightOfEndRibHokyou
def ribCapWeight():
     ribCapArea=0 #リブキャップの面積を保持
     for ribData in ribuTotalData:#リブキャップの面積を求める
             areaRibCap=ribData[4]*ribData[8] #リブキャップの長さ＊リブの厚み
             ribCapArea+=areaRibCap
     return ribCapArea*ribCapDensity

def weightOfPlank():#プランクの重量を求めるための関数　端リブのプランク長さを上辺、底辺、桁長さを高さ、厚みを持つ台形立体形として考える
     plankVolume=(ribuTotalData[0][5]+ribuTotalData[0][9]/2)+(ribuTotalData[-1][5]+ribuTotalData[0][9]/2)*ketaLengthFrangeinsideToFrangeInside
     return plankVolume*sutairoDensity
def weightOfStringer():#ストリンガーの重量を計算する
     stringerVolume=lengthOfstringerSide1*lengthOFStringerSide2*ketaLengthFrangeinsideToFrangeInside*NumberOfStringer
     stringerWeight=stringerVolume*densityOfStringer
     return stringerWeight
def filmWeight(): #フィルムの重量を計算する 端リブのプランク長さ＋リブキャップ長さを上辺と底辺に設定して、桁の長さを高さとする台形で近似
     areaOfYoku=((ribuTotalData[0][9]+ribuTotalData[0][4])+(ribuTotalData[-1][9]+ribuTotalData[-1][4]))*ketaLengthFrangeinsideToFrangeInside/2 #翼表面積
     return areaOfYoku*densityOfFilm
def weightOfKoennzai(): #後縁材の重量を求める
     return densityOfKouennzai*ketaLengthFrangeinsideToFrangeInside*crosSectionalAreaKouennzai
def weightOf1Dstructure():
     return weightOfketa+weightOfFrange+weightOfKannzashi
#excelファイル出力用の値が保持される変数
totalWeightOfRib=ribuWeight()
totalWeightOfRibFixingAroundKetaMawari=ribuFixWeight()
totalWeightOfRibTannribuHokyou=tannRibuHokyou()
totalWeightOfRibCap=ribCapWeight()
totalWeightOfPlank=weightOfPlank()
totalWeightOfStringer=weightOfStringer()
totalWeightOfFilm=filmWeight()
totalWeightOfKouennzai=weightOfKoennzai()
totalWeightOf1Dstructure=weightOf1Dstructure()

#excelファイルへの書き出し
df = pd.DataFrame({
     '翼番号':[yokuNumber],
    'スタイロ重量': [totalWeightOfRib], 
    'リブ接着剤の重量': [totalWeightOfRibFixingAroundKetaMawari],
    '端リブ補強材の重量':[totalWeightOfRibTannribuHokyou],
    'リブキャップの重量':[totalWeightOfRibCap],
    'ストリンガーの重量':[totalWeightOfStringer],
    'プランクの重量':[totalWeightOfPlank],
    'フィルムの重量':[totalWeightOfFilm],
    '後縁材の重量':[totalWeightOfKouennzai],
    '1次構造の重量':[totalWeightOf1Dstructure]
})
df.to_excel(exportReadingFilepath) 

print("completed")