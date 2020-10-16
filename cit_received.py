#!/usr/bin/env python
# coding: utf-8

# In[1]:


#This script opens the citation dataset and perform calculations in patent level
#Renato Kogeyama

#Miami, Jan 28, 2020
#Script to calculate citations received by a patent
#citation_id with less than 3 characters have no meaning
#they are causing problems moving forward
#so here I drop them


# In[2]:


import pandas as pd
import numpy as np
import re

import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import gzip


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


src = r'/home/rkogeyam/PATENT_CITATION/data/cleanuspatentcitation.csv.gz'
dst = '/home/rkogeyam/PATENT_CITATION/data/cit_received.csv.gz'


# In[5]:


get_ipython().run_cell_magic('time', '', "file_citation=gzip.open(src, 'r')\ndf=pd.read_csv(file_citation, usecols=['patent_id','citation_id','date'], dtype=object)\n\n# sample_size=100\n# df=sampler(fname, sample_size, sep='\\t')")


# In[6]:


df.info()


# In[7]:


df.head()


# In[8]:


get_ipython().run_cell_magic('time', '', "#cited patents registers total citations received \n\ndf=df.groupby(['citation_id']).count().iloc[:,0].reset_index() #Series, patent-level\n# cited_patents.dropna(0, inplace=True) #Series, '0' implies that rows are dropped\n\n#I should check this, because later I make citation back as index for merging purposes\n# cited_patents=cited_patents.reset_index() #Dataframe")


# In[9]:


df.rename(columns={'patent_id': 'cit_received'}, inplace=True)


# In[10]:


df.head()


# In[11]:


df.info()


# In[12]:


np.log(df['cit_received']).hist()


# In[13]:


df['citation_id'].str.len().value_counts().sort_index()


# In[14]:


df=df[
df['citation_id'].apply(lambda x: len(x)>4)
  ]


# In[15]:


df.info()


# In[16]:


get_ipython().run_cell_magic('time', '', "df.dropna().to_csv(dst, compression='gzip')")

