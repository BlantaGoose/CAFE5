import pandas as pd
import re
import time
import os
import collections

start = time.time()

##PLEASE summaryファイルが入っているディレクトリの指定
path = "230904"

##Please enter the model name
model = "Base"

###Step1. データ整形
print("===================================================")
print("Step1. data preparation")
p = pd.read_table(path + "/" + model + "_change.tab")      #summaryで要約したfamsファイルの読み取り
print(p)

"""
p1 = p.set_axis(["Species", "OG"], axis = "columns")    #列名変更
bunkatsu = p1['OG'].str.split(',', expand = True)       #２列目以降のOGをコンマで分けて区切る
dftrue = pd.concat([p1['Species'], bunkatsu], axis = 1) #区切ったやつとくっつける
print("Step1. finished")
print("==================================================")
print(dftrue)

###Step2. 都市鳥以外の外群のデータ作成
print("Step2. create dataframe")
outgroup = pd.DataFrame()
for line in dftrue.itertuples():
        s = pd.Series(line)
        outgroup = pd.concat([outgroup, s], axis = 1)
outgroup = outgroup.T                                           #縦長になっているので転置
print("Step2. finished")
print("==================================================")
print(outgroup[:1])



with open(path + "/overallGF.txt", "w") as f:
	for i in range(len(outgroup.columns)):
		if i > 1:
			print(outgroup.iat[0,i], file = f)

"""
"""

###Step3.　Overallを取り除き、都市鳥(Urban_lineage)と非都市鳥(outgf)を作成
print("Step3. make outgroup and specific lineage")

##PLEASE 興味ある都市鳥Nodeの指定
Urbanleaves = "<0>|<2>|<4>|<6>|<8>|<10>"
#Urbanbranches = "<28>|<26>|<30>|<24>|<16>|<14>|<6>|<27>|<29>|<15>"

Urbanspecies = outgroup[outgroup[1].str.contains(Urbanleaves)].dropna(how = 'all', axis = 1).drop(0, axis = 1)                  #.iloc[0]は"Overall rapid"だからいらない
#NonUrbanspecies = outgroup[~outgroup[1].str.contains(Urbanleaves)].iloc[1:].dropna(how = 'all', axis = 1).drop(0, axis = 1)     #how='all'とすると、全ての値がNAの行をdro$
print(Urbanspecies)

print("Step3. finished")
print("===============================================")

with open(path + "/overallGF.txt", "w") as f:
        for i in range(len(Urbanspecies.columns)):
                if i > 1:
                        print(Urbanspecies.iat[0,i], file = f)


###Step4.　要素における遺伝子ファミリーの増減値を消去([+24*]ってやつ)
print("Step4. youso modifying")
Urbanspecies = Urbanspecies.replace('OG(\d+)(\[\W\d+\*\])', r'OG\1', regex = True)      ###regex=Trueで正規表現の使用を許可。'OGxxxxxx[+xx*]'となっている要素を、'OGxxxxx$
NonUrbanspecies = NonUrbanspecies.replace('OG(\d+)(\[\W\d+\*\])', r'OG\1', regex = True)
##注意！ここでそれぞれのGF数の変動を消去した。後の解析で拡大したものを使うのか、縮小したものを使うのかによって手法は変わる。
print("Step4. finished")
print("==============================================")

"""

