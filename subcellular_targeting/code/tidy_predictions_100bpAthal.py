#!/usr/bin/env python
#import modules needed
import sys
import pandas as pd
import re
from datetime import datetime



#%%load command line args
def main():
    today=datetime.now()
    args=sys.argv[1:]
    infile=args[0]
    spltname= infile.split("_")
    
    header=["ID","Algorithm","Organelle","value"]
    predictions= pd.read_csv(infile, sep="\t", header=None,names=header)
    predictions['ID'] = predictions['ID'].apply(lambda i: re.sub('_i[0-9]*.*','',i)).apply(lambda i: re.sub('\..*','',i))
    predictions2 = predictions.groupby(['ID', 'Algorithm', 'Organelle'])['value'].max()

    newfile= "".join([spltname[0],"_",spltname[1],"_","100bpAthalmostretargeted.txt"])
    predictions2.to_csv(newfile, sep="\t")
    return 0



#Python boilerplate
if __name__=='__main__':
    main()







# In[ ]:





# In[ ]:




