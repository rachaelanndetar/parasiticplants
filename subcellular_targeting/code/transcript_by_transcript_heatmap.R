###R code from Jess to make tree figure with targeting heat map
###OG author: Jessica Warren
###Modified by Shady Kuster
###Modified by Rachael DeTar
###2040826

## Generate trees of aaRSs with targeting predictions ## 

#Load required packages
#if (!requireNamespace("BiocManager", quietly = TRUE))
#install.packages("BiocManager")

#BiocManager::install("ggtree")

library (tidyverse)
library(aplot)
library(dplyr)



#setwd
#setwd("~/OneDrive - Colostate/CSU_Sloan/Mitotrna/2023_redo/subcellular_targeting/input_prot_fasta_new/Shimalayana_invivo2/PLOTTING")
#OGkey <-read.csv("../20240417_orthogroups_geneID.csv", header=TRUE)
#setwd("~/OneDrive - Colostate/CSU_Sloan/Mitotrna/2024_subcellular_targeting/August2024_input_prot_fasta/PLOTTING/first100bpAthal_predictions/")
#OGkey <-read.csv("Rheatmaps/targeting_orthogroups_Rheatmaps.csv", header=TRUE)
setwd("~/OneDrive - Colostate/CSU_Sloan/Mitotrna/2024_subcellular_targeting/August2024_input_prot_fasta/PLOTTING/first100bpAthal_predictions/")
OGkey <-read.csv("Rheatmaps_tetrapyrole/targeting_orthogroups_Rheatmaps_tetrapyrole.csv", header=TRUE)

#ofinterest = c("cytosolic")
#OGkey= OGkey[OGkey$targeting %in%  ofinterest,]

strsplitcol = function(x){
  y = strsplit(x,split="_")[[1]][1]
  return(y)
  }

#predictionfile <- "rosids/OG0002145_rosids_20220720_tidypredictionsalltrans.txt"
plotpreds <- function(predictionfile, levelslist){
  #import data; prepare name of output file
  target_dat = read.table(predictionfile, header=FALSE, sep = "\t")
  colnames(target_dat)= c("ID","Algorithm","Organelle","value")
  target <- levelslist
  dir = paste(dirname(predictionfile), "/", sep="")
  OG = strsplitcol(basename(predictionfile))
  key = paste(OG,OGkey[OGkey$group == OG,]$targeting, OGkey[OGkey$group == OG,]$description,sep= "_")
  short_key = paste(OGkey[OGkey$group == OG,]$targeting, OGkey[OGkey$group == OG,]$description,sep= "_")
  print(short_key)
  title = paste(OGkey[OGkey$group == OG,]$targeting, OGkey[OGkey$group == OG,]$description)
  target_dat$spp <- lapply(target_dat$ID, strsplitcol)
  target_dat <- target_dat %>% arrange(factor(spp, levels = levelslist))
  
  #subset tables
  mito = target_dat %>% filter(Organelle=="Mitochondria")
  mito[,4] <- round(mito[,4], 2)

  chloro = target_dat %>% filter(Organelle=="Chloroplast")
  chloro[,4] <- round(chloro[,4], 2)
  #make the mt plot
  mplot = ggplot(mito, aes(x=Algorithm, y=ID, fill=value)) +
    geom_tile(width=0.95, height=0.95, color="gray", size = 0.5) + 
    scale_fill_gradient(limits=c(0,1), low="white", high="chocolate4", name="Mitochon. Targeting") +
    theme(legend.position = "right", legend.direction = "horizontal") +
    geom_text(aes(label=value), size = 2) +
    ggtitle(OG, subtitle = short_key)
  
  #make the plastid plot
  cplot = ggplot(chloro, aes(x=Algorithm, y=ID, fill=value)) +
    geom_tile(width=0.95, height=0.95, color="gray", size = 0.25) + 
    scale_fill_gradient(limits=c(0,1), low="white", high="darkolivegreen4", name = "Plastid Targeting") +
    theme(legend.position = "right", legend.direction = "horizontal") +
    geom_text(aes(label=value), size = 2) +
    theme(axis.ticks.y =  element_blank(),
    axis.text.y = element_blank(),
    axis.title.y = element_blank())

  #combine the plots and make pdf
  plot<-mplot %>% insert_right(cplot)
  pdf(file= paste(dir,key,"_matchingfirst100AA_Arabidopsis.pdf",sep=""),width=10, height=6, title = title) # remove "alltrans" if doing main trans only
 # pdf(file= paste(basename(predictionfile,".pdf",sep=""),width=10, height=6, title = title) # remove "alltrans" if doing main trans only
  print(plot)
  dev.off()
  graphics.off()
}




files <- list.files("Rheatmaps_tetrapyrole/", full.names = TRUE, pattern="first100bpAthal.txt")
levelslist <- c("Eaphy","Eroseum","Pequestris","Rcantleyi", "Shimalayana","Mesc","Bfungosa","Rphallo","Valbum", "Dcari","Moleifera","Salbum","Hmono", "Rwill")

for (file in files){
  plotpreds(file,levelslist)
}


