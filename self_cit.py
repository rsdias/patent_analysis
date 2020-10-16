#!/usr/bin/env python
# coding: utf-8

# In[1]:


""""
Aug 18st, 2020
convert to gzip input and output

# February 12st, 2020
# Renato Kogeyama

# Script to calculate self citations (assignee level)
# the script find the assignee for patent_id and citation_id
# then compare to verify if they are the same
# it probably can be rewritten to improve performance

# produces a citation level dataset with citation identifier plus a dummy indicating self citation
"""


# In[2]:


import pandas as pd
import numpy as np
# import itertools
# import seaborn as sns
# import networkx as nx
# import csv
# from graphviz import Digraph
# import igraph
# import matplotlib.pyplot as plt
# import datetime


# import sys
# sys.path.append('/home/rkogeyam/scripts/')
# sys.path.append('scripts/')

# from determinants_scripts import classes, dtypes
import gzip


# In[3]:


asg='data/patent_assignee.tsv.gz'
cit='data/cleanuspatentcitation.csv.gz'

dst='data/self_cit.csv.gz'

# names=['index', 'id', 'cit_received']
# usecols=['id', 'cit_received']
# dtype={'main_group':'int64', 'subgroup':'int64'}
# cols=['patent_id','citation_id', 'cit_delay']

usecols=['patent_id', 'assignee_id']
file_asg=gzip.open(asg, 'r')
df_asg=pd.read_csv(file_asg, sep='\t', usecols=usecols)

usecols=['uuid','patent_id', 'citation_id']
file_cit=gzip.open(cit, 'r')
df_cit=pd.read_csv(file_cit, usecols=usecols)

# df=pd.read_csv(src, chunksize=10000)

# df=pd.read_csv(src, dtype=dtypes, usecols=usecols, parse_dates=['date'], index_col='id', chunksize=10000)
# df = pd.read_csv(src, chunksize=1000, usecols=usecols, dtypes=dtypes, parse_dates=['date'])

# df = pd.read_csv(src, chunksize=1000,  parse_dates=['date'], error_bad_lines=False)
# df = pd.read_csv(src, usecols=usecols, names=names, chunksize=1000, dtype=dtype, index_col='id')
# df=pd.read_csv(src, usecols=[0, 1, 3], dtype={0:object}, index_col=0, chunksize=1000)


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


df_asg['patent_id']=df_asg['patent_id'].astype(str)
df_asg.info


# In[6]:


df_asg.set_index('patent_id', inplace=True)


# In[7]:


df_cit['patent_id']=df_cit['patent_id'].astype(str)
df_cit.info()


# In[8]:


df_cit.set_index('patent_id', inplace=True)


# In[9]:


df_cit=df_cit.join(df_asg)
df_cit.head()


# In[ ]:


df_cit.info()


# In[10]:


df_cit.rename(columns={'assignee_id': 'pat_asg'}, inplace=True)


# In[11]:


df_cit.reset_index(inplace=True)


# In[12]:


df_cit=df_cit.set_index('citation_id')


# In[13]:


get_ipython().run_cell_magic('time', '', 'df_cit=df_cit.join(df_asg)')


# In[ ]:


df_cit.info()


# In[14]:


df_cit.head()


# In[15]:


df_cit.rename(columns={'assignee_id':'cit_asg'}, inplace=True)

df_cit['self_cit']=np.where(df_cit['cit_asg'] == df_cit['pat_asg'], 1, 0)


# In[16]:


df_cit.head()


# In[17]:


df_cit.info()


# In[18]:


# df_cit[['patent_id', 'self_cit']].to_csv(dst, index_label='citation_id')
df_cit[['uuid','self_cit']].to_csv(dst, index=False, compression='gzip')

