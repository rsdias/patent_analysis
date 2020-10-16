#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 11st, 2020
# Analysis of the centrality output
# Requires eigen.csv from graph_tool-v2


# In[2]:


import pandas as pd
import numpy as np
import csv


# In[3]:


usecols=['id', 'date', 'eigen','cit_received','cit_received_delay','parent_citation', 'pagerank', 'katz']
dtypes={'id':object,'date':object, 'cit_received':float, 'cit_received_delay':float, 'parent_citation':float,
        'eigen':float, 'pagerank':float, 'katz':float}


# In[4]:


file='data/dataset.csv'
# df=pd.read_csv(file, chunksize=100, engine='c', lineterminator='\n', index_col='id')
df=pd.read_csv(file, engine='c', lineterminator='\n', index_col='id', usecols=usecols)


# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[6]:


# df.get_chunk()


# In[7]:


# df=df.get_chunk()


# In[8]:


df.describe()


# In[9]:


df.eigen.hist()


# In[10]:


df.pagerank.hist()


# In[11]:


df.katz.hist()


# In[12]:


df.corr()


# In[13]:


df.nlargest(15, ['cit_received']) 


# In[14]:


df.nlargest(15, ['parent_citation']) 


# In[15]:


df.nlargest(15, ['pagerank']) 


# In[16]:


df.nlargest(15, ['katz']) 


# In[17]:


df.nlargest(15, ['eigen']) 

