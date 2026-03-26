#!/bin/bash
####Rachael DeTar 2024 Ver. 3####
####arg 1 is file with query seq_ids, arg 2 is .fa file for query, arg 3 is .fa file for ortholog db, arg 4 is ortholog db name, arg 5 is query db name file####

###first make (or replace) some blank temporary files
echo -n > query.temp
echo -n > blast1.temp
echo -n > blast2.temp
echo -n > queryortho.temp


###extract sequences from our query species .fa file###
lines=$(cat $1)
for line in $lines
do 
	chmp=$(sed "s/\s*//g" <<<"${line}")
	sed -n "/$chmp/,/>/p" $2| sed '$d' >> query.temp
done

###Do a blast+ search for query sequences in database with potential orthologs###
if [ -s query.temp ]
then
	blastp -query query.temp -db $4 -num_threads 2 -outfmt '6 qacc sacc evalue pident' -max_target_seqs 1 > blast1.temp
else
	echo "No sequences found for terms provided"
fi


###extract sequences from our potential ortholog species .fa file and run a blast against our query species database###
if [ -s blast1.temp ]
then
	linesortho=$(awk '{print $2}' blast1.temp| uniq)
	for line in $linesortho
	do 
		echo $line
		chmp=$(sed "s/\s*//g" <<<"${line}")
		sed -n "/$chmp/,/>/p" $3| sed '$d' >> queryortho.temp
	done
	blastp -query queryortho.temp -db $5 -num_threads 2 -outfmt '6 qacc sacc evalue pident' -max_target_seqs 1 > blast2.temp
else
	echo "No BLAST hits for your query"
fi

###mash tables of blast results together
if [ -s blast2.temp ]
then
	tablemash_blast_RBH.py blast1.temp blast2.temp
	
else
	echo "No reciprocal BLAST hits for your query"
fi


#rm *.temp
