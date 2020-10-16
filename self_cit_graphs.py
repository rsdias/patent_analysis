#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 11st, 2020
# Script to draw Originality and generality from different Classification systems

# improve graph: x-axis label and dimensions


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

self_cit='data/self_cit.csv'
patent='data/cleanpatent.csv'
df_self=pd.read_csv(self_cit, index_col='uuid')

usecols=['id', 'date']
df=pd.read_csv(patent, usecols=usecols, parse_dates=['date'], index_col='id')


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()
get_ipython().run_line_magic('config', "InlineBackend.figure_format = 'retina'")


# In[4]:


df.index = df.index.map(str)
df_self.index = df_self.index.map(str)
df_self=df_self.join(df)
df_self.info()


# In[5]:


df_self.head()


# In[6]:


df_self.describe()


# In[7]:


fig, ax=plt.subplots(figsize=(12,8))
ax=df_self.groupby(pd.Grouper(key='date', freq="A")).mean().plot(ax=ax)
ax.set_title('Self Citation Average Trend - Firm level', fontsize=20)
plt.savefig('img/trend_self_cit.png') 
plt.show()               

