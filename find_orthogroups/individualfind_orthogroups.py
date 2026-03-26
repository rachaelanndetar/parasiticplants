#!/usr/bin/env python3
"""
Created 20220325
Updated 20240604
@author: Rachael
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
	aas=pd.concat([aas.loc[:,'ID':'description'], aas['orthogroup'].str.split("\t", expand=True)], axis=1)
	aas = aas.map(lambda x:fuckdatchar(x,'"')) #getting rid of f#cking quotes

	hits = aas.loc[:,1:].map(liststringcnter)
	hits = pd.concat([aas,hits], axis=1)
	hits.to_excel(outfile,index = False )

	return 0

#Python boilerplate
if __name__=='__main__':
    main()
  


