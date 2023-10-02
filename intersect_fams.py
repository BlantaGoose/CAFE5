import pandas as pd
import re
import os
import collections

##PLEASE summaryファイルが入っているディレクトリの指定
path = "0510"
##PLEASE ENTER THE NUMBER OF THE INTERESTED EDGE
edge = 6

###Step1. データ整形
print("===================================================")
print("Step1. data preparation")
p = pd.read_table(path + "/" + path + "_fams.txt")	#summaryで要約したfamsファイルの読み取り 
p1 = p.set_axis(["Species", "OG"], axis = "columns")	#列名変更
bunkatsu = p1['OG'].str.split(',', expand = True)	#２列目以降のOGをコンマで分けて区切る
dftrue = pd.concat([p1['Species'], bunkatsu], axis = 1)	#区切ったやつとくっつける
print("Step1. finished")
print("==================================================")

###Step2. 都市鳥以外の外群のデータ作成
print("Step2. create dataframe")
outgroup = pd.DataFrame()
for line in dftrue.itertuples():
	s = pd.Series(line)
	outgroup = pd.concat([outgroup, s], axis = 1)
outgroup = outgroup.T						#縦長になっているので転置
print("Step2. finished")
print("==================================================")

###Step3.　Overallを取り除き、都市鳥(Urban_lineage)と非都市鳥(outgf)を作成
print("Step3. make outgroup and specific lineage")

##PLEASE 興味ある都市鳥Nodeの指定
#Urbanleaves = "<0>|<4>|<6>|<8>|<24>|<20>|<22>|<16>"
#Urbanbranches = "<28>|<26>|<30>|<24>|<16>|<14>|<6>|<27>|<29>|<15>"
Urbanleaves="<0>|<2>|<4>|<6>|<8>|<10>"

Urbanspecies = outgroup[outgroup[1].str.contains(Urbanleaves)].dropna(how = 'all', axis = 1).drop(0, axis = 1)			#.iloc[0]は"Overall rapid"だからいらない
#NonUrbanspecies = outgroup[~outgroup[1].str.contains(Urbanleaves)].iloc[1:].dropna(how = 'all', axis = 1).drop(0, axis = 1)	#how='all'とすると、全ての値がNAの行をdrop。axis=1で列。
#print(Urbanspecies)

print("Step3. finished")
print("===============================================")
print(type(Urbanspecies))


###Step4.　要素における遺伝子ファミリーの増減値を消去([+24*]ってやつ)
print("Step4. youso modifying")
Urbanspecies = Urbanspecies.replace('OG(\d+)(\[\W\d+\*\])', r'OG\1', regex = True)	###regex=Trueで正規表現の使用を許可。'OGxxxxxx[+xx*]'となっている要素を、'OGxxxxxx'に置換
#NonUrbanspecies = NonUrbanspecies.replace('OG(\d+)(\[\W\d+\*\])', r'OG\1', regex = True)
##注意！ここでそれぞれのGF数の変動を消去した。後の解析で拡大したものを使うのか、縮小したものを使うのかによって手法は変わる。
#print(Urbanspecies)
print("Step4. finished")
print("==============================================")


##Step5 得られたSpecific_edgeで共有されているOGを確認。
print("Step5. Confirm the description of common OGs in interested edge.")
count = []
for line in Urbanspecies.itertuples():
	line = pd.Series(line)
	line = line.values.tolist()
	count.extend(line)
c = collections.Counter(count)
print(c.items())

print("the OG whose the number is equal to the number of interested edges is the OGs intersect in interested edges")

##edgeの数と辞書型（c）のvalues（1~edge数）が一致するキー（OGXXX）を取り出す。これが全Interested speciesでIntersectなOGになる

keys = [k for k, v in c.items() if v == edge]
with open(path + "/intersectGF.txt", "w") as f:	#ファイルに書き込みモード"w"で、以下のことをする
	for line in keys:
		if type(line) == str:	##最初の行数(type == int)を省く
			print(line, file = f)
print("intersectGF.txt is in summary directory")

