#/bin/bash

#20220104 predictions
#Updated on 20240417 to use mafftparse4.0.py, which only counts start as first locus with 15+ amino acids aligned with only single AA isnertions (-) 
#make relevent directories
mkdir MAFFT/

#Run MAFFT:
for file in *blast.fa; do mafft --auto $file > MAFFT/${file%_blast.fa}_msa.fa; done

#Clean up names for S. album, S himilayana:
sed -i '/>Shim/ s/\-RA//1' MAFFT/*
sed -i '/>Rphallo/ s/\-R1//1' MAFFT/*

#parse mafft MSA:
../mafftparse4.0.py MAFFT/

mv *alignmentstats.tab MAFFT/
mv *fortargeting.txt MAFFT/

