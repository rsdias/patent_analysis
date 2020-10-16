#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 14st, 2020
# Government patents


# In[2]:


import pandas as pd
import numpy as np
# import itertools
import seaborn as sns
# import networkx as nx
# import csv
# from graphviz import Digraph
# import igraph
import matplotlib.pyplot as plt
# import datetime


# import sys
# sys.path.append('/home/rkogeyam/scripts/')
# sys.path.append('scripts/')

# from determinants_scripts import classes, dtypes


# In[20]:


contract='data/patent_contractawardnumber.tsv'
pat_gov='data/patent_govintorg.tsv'
gov_org='data/government_organization.tsv'

# df_contract=pd.read_csv(contract, sep='\t', chunksize=1000)
# df_pat_govt=pd.read_csv(pat_gov,  sep='\t', chunksize=1000)
# df_gov_org=pd.read_csv(gov_org,  sep='\t', chunksize=1000)
df_contract=pd.read_csv(contract, sep='\t')
df_pat_govt=pd.read_csv(pat_gov,  sep='\t')
df_gov_org=pd.read_csv(gov_org,  sep='\t')

df_class=pd.read_csv('data/wipo.csv')


# In[4]:


patent='data/cleanpatent.csv'
usecols=['id', 'date', 'kind']
# df_pat=pd.read_csv(patent, chunksize=100000, usecols=usecols)
df_pat=pd.read_csv(patent, usecols=usecols, parse_dates=['date'] )


# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[6]:


df=df_pat_govt.groupby('patent_id').count()


# In[7]:


df.info()


# In[8]:


df_pat.describe()


# In[9]:


df=df.merge(df_pat, left_index=True, right_on='id', how='inner')


# In[10]:


df.info()


# In[11]:


df_pat.groupby(pd.Grouper(key='date', freq="A")).count()


# In[12]:


fig, ax=plt.subplots(figsize=(12,8))
df_pat.groupby(pd.Grouper(key='date', freq="A")).count().plot(ax=ax)
ax.set_title('Total Patent Grant', fontsize=20)
plt.legend('')


# In[21]:


df=df.merge(df_class, left_index=True, right_on='id')


# In[22]:


df.info()


# In[23]:


df.groupby(pd.Grouper(key='date', freq="A")).count()


# In[24]:


df[df['date'].dt.year==2017].groupby('wipo_sector_id').count()


# In[ ]:




