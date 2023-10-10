##CAFE5のBase_branch_probabilities.tabで、任意の閾値と各ファミリーの各ブランチにおける値を比較し有意さを確認
import pandas as pd

##This script is in the cafe5/script_cafe5/
##The output of cafe5 is in the cafe5/output/"path"/
path = "230904"
pvalue = 0.01

p = pd.read_table("output/" + path + "/Base_branch_probabilities.tab")
p = p.drop(p.columns[[112]], axis = 1)

colnames = p.columns.values
print(len(colnames))

##繰り返し処理で、各行からp < pvalueの要素を抽出
newOG = pd.DataFrame()
newprob = pd.DataFrame()

##dataframeを0,1列目のOGと、2~len(p)列目のprobに分ける
for line in p.itertuples():
    s = pd.Series(line)
    
    OG = s[[0,1]]
    newOG = pd.concat([newOG, s[[0,1]]], axis = 1)
    
    prob = s[2:len(s)]
    cond = prob < pvalue
    newprob = pd.concat([newprob, cond], axis = 1)
    
    new = pd.concat([newOG, newprob])
    new = new.drop(new.index[[0]])

new = new.T
new = new.reset_index(drop = True)
print(new)

##列名も変更
new.columns = colnames

print(new)
##できたYES/NOファイルとcount.tabをくっつける→YESの場合はアスタリスクをつけ、中括弧で囲む
##→一列目のOGを2列目以降に接続（各要素をOG00000006[+10*]みたいにする）→各行を種名で整理。

new.to_csv("output/" + path + "/Prob_bin.csv")