library(tidyverse)

##REGfamsignificance.pyで得たbinaryデータを組み合わせ
path = "230904"
p = read_csv(paste("output/", path, "/Prob_bin.csv", sep = "")) %>%
select(!1) %>% 
rename(FamilyID = '#FamilyID')

p2 = p %>% pivot_longer(2:ncol(p), names_to = "LatenName", values_to = "prob")
print(p2)

##p[1]のGenefamilyが残るように、qを整理
q = read_table(paste("output/", path, "/Base_count.tab", sep = ""))
print(q)

q2 = q %>% right_join(p[1]) %>%
pivot_longer(2:ncol(q), names_to = "LatenName", values_to = "values")
print(q2)

##これでp2とq2でpivot_longer状態にできた。さらにp2とq2を結合して一つのdfにする
pq = left_join(p2, q2, by = c("FamilyID", "LatenName"))
print(pq)

##uniteしよう
pq2 = pq %>% unite(Node, values, prob, sep = "_")
print(pq2)

##あとは、無印CAFEのsummary output(fams.txt)になるように改造
##joinの前にprobを「Trueだけ*にする」コマンド。*だけ取り出すコマンド
##Zo.alb<X>: OGXXXXXX[+10*], OGXXXXII[-2*]などとするコマンド