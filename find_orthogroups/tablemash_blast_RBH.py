#!/usr/bin/env python3
"""
Created on Thu Jan 27 11:14:17 2022
Updated on Tue June 11 2024
@author: Rachael
"""

#%%
#import modules needed
import sys
import pandas as pd
import re
from datetime import datetime
import numpy as np

#%%
#load command line args
"""
    arg1= blasthits1
    arg2= blasthits2
    arg3= name for output file
"""
def main():
    today=datetime.now()
    args=sys.argv[1:]
    b1= pd.read_table(args[0], header=None)
    b2=pd.read_table(args[1], header=None)

    b1=b1.groupby([b1.columns[0],b1.columns[1]], as_index=False).agg({
        b1.columns[2]:lambda x:', '.join(map(str,x)),
        b1.columns[3]:lambda x:', '.join(map(str,x))})

    b1.columns=['query', 'hit','evalue_hit', 'identity_hit']



    b2=b2.groupby([b2.columns[0],b2.columns[1]], as_index=False).agg({
        b2.columns[2]:lambda x:', '.join(map(str,x)),
        b2.columns[3]:lambda x:', '.join(map(str,x))})
    b2.columns=['hit', 'RBH','evalue_RBH', 'identity_RBH']


    merged=pd.merge(b1,b2, how='left').sort_values('hit').reset_index(drop=True)
    merged["query_RBH_match"]=np.where(merged["query"] == merged["RBH"], "*", "")
    print(args[2])
    filename="".join(["blast_RBH_",args[2],today.strftime("%Y%m%d_%H_%M_%S"),".xlsx"])

    merged.to_excel(str(filename), index=False)
    return 0

#%%
#Python boilerplate
if __name__=='__main__':
    main()
