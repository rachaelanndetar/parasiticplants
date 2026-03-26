#!/usr/bin/env python3
"""
Created 20220325
@author: Rachael

command line arguments:
argument 1: a two-column tab-deliminated .txt file with an "ID" column with gene names and a "description" column with detials about the gene, for example:

ID      description
AT1G70980       cytosolic Asn aaRS
AT5G56680       cytosolic Asn aaRS
AT4G17300       organellar Asn aaRS
AT4G26870       cytosolic Asp aaRS
AT4G31180       cytosolic Asp aaRS
  
argument 2: the Orthogroups.tsv file output from Orthofinder. FOr example: Results_X/Orthogroups/Orthogroups.tsv
argument 3: the name of your output file in excel format. For example: favoriteorthogroups.xlsx
"""

#%% import packages
import sys
import math
import os
import numpy as np
import pandas as pd
import re

#%% Functions
def grablines(txt, term):
    with open(txt) as temp_f:
        for line in temp_f:
            if term in line:
                return line.rstrip()
            else:
                continue
            
def fillempty(df,fill):
    for i in df.columns:
        cleandf = df[i][df[i].apply(lambda i: True if re.search('^\s*$', str(i)) else False)]= fill
        return(cleandf)
    
    
def liststringcnter(string):
    if isinstance(string, str):
        if not string:
            hits = 0
        else:
            slist = string.split(',')
            hits = len(slist)
    elif string == None:
        hits = 0
    else:
        hits = "Something jank"
    return(hits)

def fuckdatchar(string,char):
    if isinstance(string, str):
        cleanstring = string.replace(char,'')
    else:
        cleanstring = string
    return(cleanstring)

#%% Pull out orthogroups with A. thal genes of interest
def main():
	aas = pd.DataFrame(pd.read_table(sys.argv[1]))
	txt = sys.argv[2]
	outfile = sys.argv[3]
	
	aas['orthogroup']=aas.loc[:,'ID'].apply(lambda x:grablines(txt,x))
	null= aas.loc[pd.isnull(aas['orthogroup'])]
	aas = aas.loc[pd.notnull(aas['orthogroup'])]
	aas = aas.groupby('orthogroup').agg({
    		'ID':', '.join,
    		'description':', '.join}).reset_index()
	aas = pd.merge(aas,null, how= 'outer')
	aas=pd.concat([aas.loc[:,'ID':'description'], aas['orthogroup'].str.split("\t", expand=True)], axis=1)
	aas = aas.applymap(lambda x:fuckdatchar(x,'"')) #getting rid of f#cking quotes

	hits = aas.loc[:,1:].applymap(liststringcnter)
	hits = pd.concat([aas,hits], axis=1)
	hits.to_excel(outfile,index = False )

	return 0

#Python boilerplate
if __name__=='__main__':
    main()
  


