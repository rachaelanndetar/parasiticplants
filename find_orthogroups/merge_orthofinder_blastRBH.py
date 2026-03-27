#!/usr/bin/env python3
"""
Updated 20230314- fix bug

@author: Rachael
"""

#%%import modules
#import modules needed
import sys
import pandas as pd
import re
from datetime import datetime

#%%functions

def substr_cols(df,colwsub,colwstring):
    out=[]
    for i in range(0,len(df)): 
        sub=str(df.loc[i,colwsub])
        string=str(df.loc[i,colwstring])
        match=re.search(sub,string)
        if match:
            out.append("*")
        else:
            out.append("")
    return(out)

#%%load command line args
"""
    arg1= orthogroup individual gene output excel file
    arg2= blast RBH excel file
"""
def main():
    today=datetime.now()
    args=sys.argv[1:]
    ORTHO= pd.read_excel(args[0])
    RBH = pd.read_excel(args[1])
    
#%%pull correct columns from orthofinder file
    hit=list(RBH["hit"])
    cols=['ID','description',0,1]
    for (columnName, columnData) in ORTHO.items():
        for items in columnData:
            itemslist = str(items).split(',')
            for i in itemslist:
                if i in hit:
                    cols.append(columnName)
                    name=columnName
                    break
                else:
                    continue
    ORTHOd= ORTHO.drop(columns=[col for col in ORTHO if col not in cols])
    #print(ORTHOd)
    ORTHOd=ORTHOd.rename(columns = {'ID':'query',name:'orthofinder_hits',0:"orthogroup",1:"orthogroup_queryspphit"})
            
#%%merge orthofinder and blast RBH. export excel
    merged=pd.merge(ORTHOd,RBH,on="query",how='left')
    merged["orthofinder_RBH_match"]= substr_cols(merged,'hit','orthofinder_hits')
    merged=merged.sort_values('description')
    filename="".join(["orthofinder_",args[1]])
    merged.to_excel(str(filename), index=False)
    return 0

#%%Python boilerplate
if __name__=='__main__':
    main()

