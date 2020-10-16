#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to calculate originality and  application data
# This script prepares the classification data before merging
# Jan 16th, 2020
# Multiple classifications generate an error into the Generality calculation
# I am creating a version with the first class only 

# Jan 7th, 2020


# In[2]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd
import numpy as np
import re


# In[3]:


# from the data dictionary

# patent_id: patent number
# field_id:  WIPO technology field ID as derived from crosswalk 
#            http://www.wipo.int/export/sites/www/ipstats/en/statistics/patents/xls/ipc_technology.xls
# sequence:  order in which WIPO technology field appears on patent


# In[4]:


wipo = 'data/wipo.tsv'
dst= 'data/wipo.csv'


# In[5]:


# 
df=pd.read_csv(wipo, sep='\t', dtype='object')

# sample_size=1000
# wipo_df=sampler(wipo, sample_size, sep='\t')


# In[6]:


# # # Keep this for reference!
# # # As of Dec 31st, 2019, I compared the clean to the raw version of citation and patent ids

# # #stripping non-desired characters but keeping the originals for later check - only three changes in citation_id

# wipo_df['patent_id_raw']=wipo_df['patent_id']

# cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
# wipo_df['patent_id']=wipo_df['patent_id'].apply(cleaning_patent)


# In[7]:


#first, construct a table with wipo categories in columns, patent level
#second, 


# In[8]:


df.dtypes


# In[9]:


df.groupby('sequence').patent_id.count()


# In[10]:


df=df[df['sequence']=='0'][['patent_id', 'field_id']]


# In[11]:


df.field_id.value_counts()


# In[12]:


df=df.add_prefix('wipo_')


# In[13]:


df.rename(columns={ df.columns[0]: "id" }, inplace = True)


# In[14]:


df.head()


# In[15]:


df.set_index('id').to_csv(dst)

