#!/usr/bin/env python3
"""
Created on Wed Apr 20 15:52:26 2022
Updated on Fri Aug 2nd 2024
@author: Rachael

command-line args
1)Directory with fasta files.
2) Name of outfile as .xlsx

"""
#%% import packages
import sys
import os
import pandas as pd
import re
from Bio import SeqIO

#%% user-defined functions
#This function can be used to determine the length of a seqeunce in relation to a ref species
def alignmentstats(testdata):
    orthogroup=[]
    species=[]
    identifier=[]
    alignlen=[]
    gaps=[]
    totallen=[]

    for record in SeqIO.parse(testdata, "fasta"):
        print(testdata,record.name," is being parsed")
        orthogroup.append(re.split("_",testdata)[1])
        species.append(re.split("_",record.name)[0])
        identifier.append(record.name)
        alignlen.append(len(re.findall('[A-Z]',str(record.seq))))
        gaps.append(record.seq.count('-'))
        totallen.append(len(record.seq))
        df = pd.DataFrame({
            "Orthogroup": re.split(".fa",os.path.basename(testdata))[0],
            "Species" : species,
            "Gene" : identifier,
            "Aligned" : alignlen,
            "Gaps": gaps,
            "Total" : totallen,
                })

    maxs = df.groupby('Species')["Aligned"].max()
    df["Percent_Longest_Athal"]= df["Aligned"]/maxs['Athal']

    out = df.groupby('Species').agg({
        'Orthogroup':'first',
        'Gene':', '.join,
        'Aligned':lambda x:', '.join(map(str,x)),
        'Gaps':lambda x:', '.join(map(str,x)),
        'Total':'first',
        'Percent_Longest_Athal': 'max'}).reset_index()
    return(out)

#%% main
def main():
    args=sys.argv[1:]
    directory=args[0]
    outfile=args[1]
    moosh = pd.DataFrame({
        "Orthogroup": [],
        "Species" : [],
        "Gene" : [],
        "Aligned" : [],
        "Gaps": [],
        "Total" : [],
        'Percent_Longest_Athal' : []
        })
    for file in os.listdir(directory):
        if '.fa' in file:
            output=alignmentstats("".join([directory,file]))
            moosh = pd.concat([moosh,output],axis=0)
    moosh.to_excel(outfile,index = False )
    return 0
            

#%% Boilerplate
if __name__=='__main__':
    main()
