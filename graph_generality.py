#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 11st, 2020
# Script to draw Originality and generality graphs from different Classification systems


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns

import sys
sys.path.append('/home/rkogeyam/scripts/')
sys.path.append('scripts/')

from determinants_scripts import classes, dtypes

originality='data/originality_classes.csv'
generality='data/generality_classes.csv'
patent='data/cleanpatent.csv'


usecols=['id', 'date']
df=pd.read_csv(patent, usecols=usecols, parse_dates=['date'], index_col='id')
df_orig=pd.read_csv(originality, index_col='patent_id')


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[4]:


df.index = df.index.map(str)
df_orig.index = df_orig.index.map(str)
df_orig=df_orig.join(df)
df_orig.info()


# In[5]:


df_orig.head()


# In[6]:


df_orig.describe()


# In[7]:


fig, ax=plt.subplots(figsize=(12,8))
ax=df_orig.groupby(pd.Grouper(key='date', freq="A")).mean().plot(ax=ax)
ax.set_title('Originality Trend')
plt.savefig('img/trend_originality.png') 
plt.show()               


# In[8]:


df_gener=pd.read_csv(generality, index_col='citation_id')


# In[9]:


df_gener.index = df_gener.index.map(str)
df_gener=df_gener.join(df)
df_gener.info()


# In[10]:


fig, ax=plt.subplots(figsize=(12,8))
ax=df_gener.groupby(pd.Grouper(key='date', freq="A")).mean().plot(ax=ax)
ax.set_title('Generality Trend')
plt.savefig('img/trend_generality.png') 
plt.show()               

