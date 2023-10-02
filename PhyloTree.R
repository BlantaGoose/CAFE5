##食性データフレームを、系統樹の隣にプロットしたい


library(ape)
library(tidyverse)
library(ggplot2)
library(ggtree)
library(igraph)

##系統樹と食性データを結合
path = "230904"
phylo <- "telluravestree.newick"
tree <- read.tree(paste("input", path, phylo, sep = "/"))

##Telluraves_connect.Rで結合したEltonとSamplelist
sample <- "telluraves.csv"
diet <- read_csv(paste("input", path, sample, sep = "/"))

##tree$tip.label数とdiet$Scientific数は一致するか？取りこぼされたのは誰
tiplab <- tree$tip.label

diet[[37]] <- diet[[37]] %>% 
  str_replace(" ", "_") 
##dietだけ学名がGallus gallusになっていたので、tree$tip.labelと揃える


Spe <- tiplab %>%
  str_extract_all("\\w+") %>%
  str_sub()
Spe %>% class()

Spe %in% diet[[37]]
##Gallus_gallusがdietに入っていない


diet[[37]] %in% Spe
##Merops_nubicus、Colius striatus、Acanthisitta chlorisが系統樹に入っていない
##→low qualityなので当然

##0904：dietにGallus_gallusをいれ、dietから上の3種を除去する
##→系統樹とdietデータを結合し、ヒートマップ系統樹の作成

##Spe（系統樹）にはいないdiet（サンプルでーた）
diet[[37]][!Spe %in% diet[[37]]]
Spe[!diet[[37]] %in% Spe]

elton <- read_tsv("input/BirdFuncDat.txt")
Spe2 <- tiplab %>% 
  str_extract_all("\\w+") %>%
  str_replace_all("_", " ")

usedSpe <- elton[[8]][elton[[8]] %in% Spe2]
usedSpe2 <- usedSpe %>% 
  as.data.frame()
colnames(usedSpe2) <- c("Scientific")

join <- usedSpe2 %>% left_join(elton)
join2 <- join %>% 
  select(c(1,3,4,5,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23))
##join2 dataは（配列情報>90以上の）使用した種で、食性情報付きのデータ

##tree$tiplabとくっつけるために、書き方を少し変える
join2[[1]] <- join2[[1]] %>%
  str_replace(" ", "_")
join3 <- join2 %>% rename("label" = Scientific)
tree$tip.label <- tiplab %>% 
  str_replace_all("\"(.+_.+)\"", "\\1")
#これで、dataframeの学名書き方と、系統樹のtip.label書き方が一致した
#annotation dataframeとphylo型を結合するには、tree$tip.labelとdataframeの共通列がlabelという列名で揃っていないといけない
tree2 <- full_join(tree, join3, by = "label")
tree2

##可視化
ggtree(tree2, layout = "circular", branch.length = "none") +
  geom_tippoint(aes(shape=`Diet-5Cat`), size = 5)


okabe_ito = palette.colors(9L, "Okabe-Ito")
t <- ggtree(tree2, layout = "circular", branch.length = "none") +
  geom_tiplab(color = "black", 
              offset = 1, 
              size = 3, 
              geom = "text", align = TRUE) + ##geom_tiplabで種名
  geom_tippoint(mapping = aes(color = `Diet-5Cat`), size = 5) +
  theme(legend.position = "bottom")
ggsave("output/230904/ot.png", t, width = 10, height = 10)

"""
  aes(color = I(`Diet-Certainty`)) + ##IOCOrderに応じてbranchの色わけ
  scale_color_manual(
    name = "DietC",
    breaks = c("A", "B", "C", "D2"),
    labels = c("OK", "Good", "Soso", "bad"),
    values = c("red", "orange", "blue", "black")
    )
"""