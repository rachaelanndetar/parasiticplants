#/bin/bash

#20220104 predictions

#make relevent directories
mkdir TARGETP LOCALIZER PLOTTING 
mkdir PLOTTING/alltrans_predictions


# TARGETP
for file in *_blast.fa; do targetp -fasta $file -mature -org pl; done
sed -i 's/\-R.//g' *targetp2
mv *targetp2 TARGETP/
mv *mature* TARGETP/

#LOCALIZER
for file in *_blast.fa; do LOCALIZER.py -p -i $file > LOCALIZER/${file%_blast.fa}_LOCALIZER.txt; done
sed -i 's/\-R.//g' LOCALIZER/*LOCALIZER.txt

#combine prediction files
for file in TARGETP/*summary.targetp2; do name=$(basename $file); tail -n +3 $file | awk '{print $1"\tTargetP\t"$6"\t"$5}'> PLOTTING/alltrans_predictions/${name%%_*}_predictions.txt; done

for file in LOCALIZER/*LOCALIZER.txt; do name=$(basename $file); awk '/Identifier/{flag=1;next}/-------/{flag=0}flag' $file| awk -v FS='\t' '{print $1"\tLOCALIZER\t"$2"\t"$3}' |sed 's/Y (//g;s/ | ....)//g;s/-/0.0/g' | awk '{print$1"\t"$2"\t"$3"\t"$4}'  >> PLOTTING/alltrans_predictions/${name%%_*}_predictions.txt; done

#Clean up predictions a bit
for file in PLOTTING/alltrans_predictions/*predictions.txt; do python3 ~/pythonscripts/tidy_predictionscmd_alltrans.py $file; done
