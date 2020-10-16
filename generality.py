#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to calculate generality and  application data
# Generality: how diverse is the impact of a patent
# This is done by calculating the herfindal index of citing patents


# In[2]:


# Feb 7th, 2020
# While the previous version is already up, I want to improve the script
# I want to make calculations with only one script
# Also, I want to compare different class systems
# this version took 10 minutes - i am moving the old version away

# Jan 16th, 2020
# Due to performance problems in the HPC, this script was divided in two, the script following this is generality_2
# generality > 1 is not an error, but a consequence of adopting WIPO
# it seems that the original calculation had only one class per patent
# WIPO provides multiple classes - so when you divide by the total number of citations, 
#  you do not have the proportion of classes cited anymore
# to correct this issue, I can calculate Generality and Originality based only on the first WIPO class

# Jan 13th, 2020
# Script is running but there are two major issues
# - there should not exist generality > 1 , so there is an error in calculation
# - too many NANs (about 400k), but I will tackle this issue in 'too_many_nans.ipynb'

# to tackle the first problem, I'll begin by creating a subset of the database
# to do that, I'll use USPTO classification system


# In[3]:


# Trying to save memory is leading to a small nightmare 
# I am postponing the use of dask modules


# In[4]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd
import numpy as np
import re

import dask.dataframe as dd

import gzip


# In[5]:


citation= '/home/rkogeyam/PATENT_CITATION/data/cleanuspatentcitation.csv.gz'
classification = '/home/rkogeyam/PATENT_CITATION/data/wipo.csv.gz' #avoid multiple classes

dst= '/home/rkogeyam/PATENT_CITATION/data/generality_temp.csv.gz'


# In[6]:


get_ipython().run_cell_magic('time', '', "file_cit=gzip.open(citation, 'r')\ncitation_df=pd.read_csv(file_cit, sep=',', usecols=['patent_id', 'citation_id'])\n\nfile_class=gzip.open(classification, 'r')\nclass_df=pd.read_csv(file_class)")


# In[7]:


#to guarantee same format for the merge
class_df['id']=class_df['id'].astype(str)
citation_df=citation_df.astype(str)


# In[8]:


#join on index is faster
class_df.set_index('id', inplace=True)
citation_df.set_index('patent_id', inplace=True)


# In[9]:


citation_df.shape


# In[10]:


get_ipython().run_cell_magic('time', '', "#citation level dataset\n#join is faster than merge\ndf=citation_df.join(class_df, how='inner')  \n\n#the left dataframe is citation df, which is indexed by patent_id\n#when later on I group by citation_id is very possible that NaNs appear")


# In[11]:


# df.to_csv(dst)


# In[12]:


df = pd.get_dummies(df, columns=['wipo_sector_id'])


# In[13]:


df.head()


# In[14]:


get_ipython().run_line_magic('time', '')
total_citation=df.groupby('citation_id').count().iloc[:,0]
total_citation=np.square(total_citation)
total_citation.head()


# In[15]:


get_ipython().run_line_magic('time', '')
# df.drop('citation_id', inplace=True, axis=1)
df=df.groupby('citation_id').sum().fillna(0)
df.head()


# In[16]:


get_ipython().run_line_magic('time', '')
df_squared=np.square(df) #element-wise squaring
df_squared=df_squared.sum(axis='columns') #sum all columns, per row
df_squared.head()


# In[17]:


get_ipython().run_line_magic('time', '')
df2=pd.concat([df_squared, total_citation], axis=1)
df2.columns=['df_squared', 'total_citation']
df2.head()


# In[18]:


get_ipython().run_line_magic('time', '')
df2['herfindal']=df2['df_squared']/df2['total_citation'] #its a measure of concentration


# In[19]:


get_ipython().run_line_magic('time', '')
df2['generality']=1-df2['herfindal'] # as defined in Hall et al, 2001
df2['generality'].hist()


# In[20]:


df2.info()


# In[21]:


df2.head()


# In[22]:


df2.describe()


# In[23]:


df2.to_csv(dst, compression='gzip')


# In[24]:


# %time
# df2=df_squared.to_frame().join(total_citation.to_frame())
# df2.head()

