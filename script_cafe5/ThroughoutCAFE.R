##This script is for perfoming cafe
library(tidyverse)
library(ape)

##Did you get OrthoFinder data from DDBJ?
path = "telluraves"

Orthologs_raw <- read_tsv(paste("input", path, "Orthogroups/Orthogroups.GeneCount.tsv", sep = "/"))

##Enzanはorthogroupのなかで遺伝子数が変なやつを検出するためのmatrix
Enzan <- Orthologs_raw %>%
  select(!c(Orthogroup, Total)) %>%
  t()

##saidai, saisyouは各Orthogroupの中で、各種が持っているコピー数の最大値及び最小値を記したdf
saidai <- Enzan %>% 
  apply(2, max) %>%
  as.data.frame() %>%
  rename(max_real = ".")
saisyou <- Enzan %>% 
  apply(2, min) %>%
  as.data.frame() %>%
  rename(min_real = ".")

##Orthologs_1は各Orthogroupsの最大値、最小値もくっつけたdf
Orthologs_1 <- Orthologs_raw %>% select(!c(Total)) %>%
  bind_cols(saidai, saisyou)

##最大値と最小値の差
Orthologs_2 <-Orthologs_1 %>% 
  mutate(sa = max_real - min_real) %>%
  filter(max_real != min_real) %>%
  filter(sa < 50)


##外れ値と遺伝子ファミリー数が全種で共通の行を省いた。最後に1列目を複製し列名をいじって、CAFEへのインプットデータの出来上がり。
Orthologs_3 <- Orthologs_2 %>% 
  mutate(Description = Orthogroup, ID = Orthogroup) %>%
  relocate(Description, ID) %>%
  select(!c(Orthogroup, max_real, min_real, sa))

date = "0822"
dir = paste("input/", date, sep = "")
dir.create(dir)
Orthologs_3 %>% 
  write_tsv(paste(dir, "/Orthogroups.GeneCount2.tsv", sep = ""))#, quote = FALSE) #,row.names = FALSE)
##Did you finish creating ultrametric tree with makeultrametric.R?
