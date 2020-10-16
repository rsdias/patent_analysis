#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 11st, 2020
# Script to draw Originality and generality from different Classification systems


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


# In[3]:


pat='data/cleanpatent.csv'
cit='data/cleanuspatentcitation.csv'
int_ext='data/int_ext_cit_v2.csv'

usecols=['uuid','citation_id']

df=pd.read_csv(int_ext, index_col='uuid')

df_cit=pd.read_csv(cit, usecols=usecols, index_col='uuid')

df_pat=pd.read_csv(pat, usecols=['id', 'date'], parse_dates=['date'], index_col='id')


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[5]:


sns.set()


# In[6]:


df=df_cit.join(df)


# In[7]:


df.info()


# In[8]:


df.head()


# In[9]:


# df=df.groupby('citation_id').agg(['count', 'sum'])
df=df.groupby('citation_id').mean()


# In[10]:


df.info()


# In[11]:


df.head()


# In[12]:


df=df_pat.join(df)


# In[13]:


df.info()


# In[14]:


df.head()


# In[15]:


df.describe().transpose()


# In[16]:


df.set_index('date', inplace=True)


# In[17]:


cols=list(df.columns)


# In[18]:


far_ext=cols[0::2]


# In[ ]:


far_ext


# In[19]:


ext=cols[1::2]


# In[ ]:


ext


# In[20]:


ax = plt.gca()

for element in far_ext:
    df.resample('A').mean().plot(y=element, kind='line', ax=ax)

plt.show()


# In[21]:


ax = plt.gca()

for element in ext:
    df.resample('A').mean().plot(y=element, kind='line', ax=ax)

plt.show()


# In[22]:




