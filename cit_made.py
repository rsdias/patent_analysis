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


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


src = r'/home/rkogeyam/PATENT_CITATION/data/cleanuspatentcitation.csv.gz'
dst = '/home/rkogeyam/PATENT_CITATION/data/cit_made.csv.gz'


# In[5]:


get_ipython().run_cell_magic('time', '', "file_citation=gzip.open(src, 'r')\ndf=pd.read_csv(file_citation, usecols=['patent_id','citation_id','date'], dtype=object)\n\n# sample_size=100\n# df=sampler(fname, sample_size, sep='\\t')")


# In[6]:


df.info()


# In[7]:


df.head()


# In[8]:


get_ipython().run_cell_magic('time', '', "#cited patents registers total citations received \n\ndf=df.groupby(['patent_id']).count().iloc[:,0].reset_index() #Series, patent-level\n# cited_patents.dropna(0, inplace=True) #Series, '0' implies that rows are dropped\n\n#I should check this, because later I make citation back as index for merging purposes\n# cited_patents=cited_patents.reset_index() #Dataframe")


# In[9]:


df.rename(columns={'citation_id': 'cit_made'}, inplace=True)


# In[10]:


df.head()


# In[11]:


df.info()


# In[12]:


df['cit_made'].value_counts().sort_index()


# In[13]:


np.log(df['cit_made'].apply(lambda x: x+1)).hist()


# In[14]:


df['patent_id'].str.len().value_counts().sort_index()


# In[15]:


df=df[
df['patent_id'].apply(lambda x: len(x)>4)
  ]


# In[16]:


df.info()


# In[17]:


get_ipython().run_cell_magic('time', '', "df.to_csv(dst, compression='gzip')")

