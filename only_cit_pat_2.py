#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 11st, 2020
# This script generates a list of patent cited and citing from the original USPTO patent file

# August 12th, 2020
# Small change to include uuid (for joining to self_cit)


# In[2]:


import pandas as pd
import numpy as np
import csv


# In[3]:


cit='data/uspatclean_joinselfcit.csv'

# file=gzip.open(cit, 'r')
usecols=['patent_id', 'citation_id']
df_cit=pd.read_csv(cit, usecols=usecols, index_col='patent_id', chunksize=1000, iterator=True)


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


for chunk in df_cit:
    chunk.dropna().to_csv('data/patcitonly_self_cit.csv', mode='a', header=False)


# In[ ]:




