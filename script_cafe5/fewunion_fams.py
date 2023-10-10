import pandas as pd
import re
import os
import collections

##PLEASE enter the path having summary files
path = "5000_Paleognate3_28"

###Step1. データ整形
print("===================================================")
print("Step1. data preparation")
p = pd.read_table(path + "/" + path + "_fams.txt")	#summaryで要約したfamsファイルの読み取り 
p1 = p.set_axis(["Species", "OG"], axis = "columns")	#列名変更
bunkatsu = p1['OG'].str.split(',', expand = True)	#２列目以降のOGをコンマで分けて区切る
dftrue = pd.concat([p1['Species'], bunkatsu], axis = 1)	#区切ったやつとくっつける
print("Step1. finished")
print("==================================================")

###Step2. Corvidae以外の外群のデータ作成
print("Step2. create dataframe")
outgroup = pd.DataFrame()
for line in dftrue.itertuples():
	s = pd.Series(line)
	outgroup = pd.concat([outgroup, s], axis = 1)
outgroup = outgroup.T						#縦長になっているので転置
print("Step2. finished")
print("==================================================")


###Step3.　Overallを取り除き、カラスノードデータ(Corvidae_lineage)と外群(outgf)を作成
print("Step3. make outgroup and specific lineage")
Urbanleaves = "<6>|<0>|<20>"
#Urbanbranches = "<28>|<26>|<30>|<24>|<16>|<14>|<6>|<27>|<29>|<15>"

Urbanspecies = outgroup[outgroup[1].str.contains(Urbanleaves)].dropna(how = 'all', axis = 1).drop(0, axis = 1)	#外群にしたいのをIcytreeなどから慎重に選び、ノード番号を書く
NonUrbanspecies = outgroup[~outgroup[1].str.contains(Urbanleaves)].iloc[1:].dropna(how = 'all', axis = 1).drop(0, axis = 1)

print("Step3. finished")
print("===============================================")


###Step4.　要素における遺伝子ファミリーの増減値を消去([+24*]ってやつ)
print("Step4. youso modifying")
Urbanspecies = Urbanspecies.replace('OG(\d+)(\[\W\d+\*\])', r'OG\1', regex = True) 	###regex=Trueで正規表現の使用を許可。'OGxxxxxx[+xx*]'となっている要素を、'OGxxxxxx'に置換
NonUrbanspecies = NonUrbanspecies.replace('OG(\d+)(\[\W\d+\*\])', r'OG\1', regex = True)	
##注意！ここでそれぞれのGF数の変動を消去した。後の解析で拡大したものを使うのか、縮小したものを使うのかによって手法は変わる。
print("Step4. finished")
print("==============================================")



##共通抽出
##Step5 得られたSpecific_edgeで共有されているOGを確認。
print("Step5. Confirm the description of common OGs in interested edge.")
count = []
for line in Urbanspecies.itertuples():
        line = pd.Series(line)
        line = line.values.tolist()
        count.extend(line)
c = collections.Counter(count)

##とりあえずvalues（カウント数）が1以上の要素を取り出し、リスト化する。これが全Interested speciesでUnionなOGになる
keys = [k for k, v in c.items() if v >= 1]
with open(path + "/unionGF_3sp.txt", "w") as f: #ファイルに書き込みモード"w"で、以下のことをする
	for line in keys:
		li = str(line)
		if li.startswith("OG"):
			print(li, file = f)
print("unionGF.txt is in summary directory")
