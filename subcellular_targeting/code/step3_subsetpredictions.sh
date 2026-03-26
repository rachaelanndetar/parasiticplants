#/bin/bash

#20220104 predictions

#make relevent directories
mkdir PLOTTING/first100bpAthal_predictions/

#subset presdictions based on MSA

#get rid of -R1 in Salbum geneids  that is causng problems
for file in MAFFT/*fortargeting.txt; do sed -i 's/\-R.//g' $file ; done

#Extract only proteins which start within 100 AA of A.thal orthologue based on MSA
for file in MAFFT/*fortargeting.txt; do for line in $(cat $file | sort | uniq); do name=$(basename $file); sed -n "/$line\t/p" PLOTTING/alltrans_predictions/${name%_fortargeting.txt}_tidypredictionsalltrans.txt >> PLOTTING/first100bpAthal_predictions/${name%_fortargeting.txt}_first100bpAthal.txt; done; done

#check numbers of gene names in each file
for file in MAFFT/*fortargeting.txt; do name=$(basename $file) count1=$(tail +2 $file |sort | uniq | wc -l); count2=$(awk '{print $1}' PLOTTING/first100bpAthal_predictions/${name%fortargeting.txt}first100bpAthal.txt|sort| uniq | wc -l); [[ $count1 -eq $count2 ]] && mismatch=$( echo "ok") || mismatch=$(echo MISMATCH); echo ${name%_fortargeting.txt} $count1 $count2 $mismatch; done

#Extract most retargeted proteins for each species/Orthogroup:
for file in PLOTTING/first100bpAthal_predictions/*first100bpAthal.txt; do python3 ../tidy_predictions_100bpAthal.py $file; done
