#!/usr/bin/env python
# coding: utf-8

# In[22]:


#!/usr/bin/env python3
"""
Created August 2022
Updated August 2024
This script is intended for processing mafft alignments for targeting analysis. See MAFFTparse2.0.py for processing for presence/absence

@author: Rachael

command-line args
1)Directory with files named very specifically
2) Name of outfile as .xlsx

"""
#%% import packages
import sys
import os
import pandas as pd
import re
from Bio import SeqIO


# In[16]:


#%% user-defined functions

def alignmentstats(testdata):
    orthogroup=[]
    species=[]
    identifier=[]
    alignlen=[]
    gaps=[]
    totallen=[]
    seqs=[]
    for record in SeqIO.parse(testdata, "fasta"):
        print(testdata,record.name," is being parsed")
        orthogroup.append(re.split("_",testdata)[1])
        species.append(re.split("_",record.name)[0])
        identifier.append(record.name)
        alignlen.append(len(re.findall('[A-Z]',str(record.seq))))
        gaps.append(record.seq.count('-'))
        totallen.append(len(record.seq))
        for index, letter in enumerate(record.seq):
            if letter != "-" and index < len(record.seq)-1:
                if "--" not in record.seq[index:index + 15]:
                    print(record.seq[index:index+15])
                    seqs.append(index)
                    break
                else:
                    continue
            elif index < len(record.seq)-1: 
                continue
            else:
                seqs.append(len(record.seq))
    print(len(identifier), len(seqs))
    df = pd.DataFrame({
        "Orthogroup": re.split("_",os.path.basename(testdata))[0],
        "Species" : species,
        "Gene" : identifier,
        "Aligned" : alignlen,
        "Gaps": gaps,
        "Total" : totallen,
        "Seqstart":seqs
                })
    maxs = df.groupby('Species')["Aligned"].max()
    starts = df.groupby('Species')["Seqstart"].max()
    #df["Percent_Longest_Athal"]= df["Aligned"].astype(float)/float(maxs['Athal'])
    startthreshold = starts["Athal"] + 100
    out = df.loc[df['Seqstart'] <= startthreshold,'Gene']
    return df,out


# In[21]:


#%% main
def main():
    args=sys.argv[1:]
    directory=args[0]
    for file in os.listdir(directory):
        if 'msa.fa' in file:
            output1,output2=alignmentstats("".join([directory,file]))
            outfile1=file.replace('msa.fa', 'alignmentstats.tab')
            outfile2=file.replace('msa.fa', 'fortargeting.txt')
            output1.to_csv(outfile1,index = False, sep='\t' )
            output2.to_csv(outfile2,index = False, sep='\t' )
    return 0
            

#%% Boilerplate
if __name__=='__main__':
    main()


# In[ ]:




