#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 14st, 2020
# Script to examine foreign citations


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
import matplotlib
# import datetime


# import sys
# sys.path.append('/home/rkogeyam/scripts/')
# sys.path.append('scripts/')

# from determinants_scripts import classes, dtypes


# In[3]:


cit='data/foreigncitation.tsv.gz'
file=gzip.open(cit, 'r')
df=pd.read_csv(file, sep='\t', parse_dates=['date'])


# In[4]:


df.info()


# In[5]:


get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[6]:


sns.set()


# In[7]:


df.head()


# In[8]:


df['date']=pd.to_datetime(df['date'], errors='coerce')


# In[9]:


df.shape


# In[10]:


df=df[df['date'].dt.year<2018]


# In[11]:


df.shape


# In[12]:


df=df[df['date'].dt.year>1960]


# In[13]:


df.shape


# In[14]:


fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(14, 6))
ax=df.groupby(pd.Grouper(key='date', freq="A")).count().uuid.plot(ax=ax)
# ax = df.groupby('year').count().plot(y='uuid', ax=ax)
ax.set_title('Foreign Citations', fontsize=14)
ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax.xaxis.label.set_visible(False)


# In[15]:




