#!/usr/bin/env python
# coding: utf-8

# In[2]:


#!/usr/bin/env python3
"""
Created on 20220713

@author: Rachael
"""


# In[3]:


#%%import modules
#import modules needed
import sys
import pandas as pd
import re
from datetime import datetime


# In[4]:


#%%functions


# In[18]:


#%%load command line args
def main():
    today=datetime.now()
    args=sys.argv[1:]
    infile=args[0]
    spltname= infile.split("_")
    
    header=['ID','Algorithm','Chloroplast','Mitochondria']
    predictions= pd.read_csv(infile, sep="\t", header=None,names=header)
    predictions = pd.melt(predictions, id_vars=['ID','Algorithm'], value_vars=['Chloroplast', 'Mitochondria']).rename(columns={'variable':'Organelle'})

    newfile= "".join([spltname[0],"_",spltname[1],"_","tidypredictionsalltrans.txt"])
    predictions.to_csv(newfile, sep="\t",index=False)
    exit(0)


# In[36]:


#Python boilerplate
if __name__=='__main__':
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




