#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 12st, 2020
# This script compares classification in each classification system
# Second level matches specifications of Nemet and Johnson 2012


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

from classification import preprocessing

citation='data/cleanuspatentcitation.csv'

usecols=['uuid', 'patent_id', 'citation_id']
df=pd.read_csv(citation, usecols=usecols)


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


sns.set()


# In[5]:


# class_systems=['wipo']
class_systems=['ipcr', 'cpc', 'nber']


# In[6]:


#create classes dataset
class_df=pd.read_csv('data/wipo.csv', dtype=object, usecols=[0,1,2])
class_df=class_df.astype(str)
class_df=class_df.set_index('id')

for class_system in class_systems:
    classification = 'data/'+class_system+'.csv'
    class_x=pd.read_csv(classification, dtype=object, usecols=[0,1,2])
    class_x=class_x.astype(str)
    class_x=class_x.set_index('id')
    class_df=class_df.join(class_x)


# In[7]:


class_df.dtypes


# In[8]:


df=df.astype(str)
df=df.set_index('patent_id')


# In[9]:


df.dtypes


# In[10]:


df=df.join(class_df)


# In[11]:


print(df.head())
dimensions=list(df.columns)
dimensions.remove('uuid')
dimensions.remove('citation_id')
dimensions = [sub.replace('_id', '') for sub in dimensions] 


# In[12]:


ext_list = [sub + '_ext' for sub in dimensions] 


# In[13]:


ext_list


# In[14]:


df = df.add_suffix('_pat')
df.rename(columns={'uuid_pat':'uuid', 'citation_id_pat':'citation_id'}, inplace=True)


# In[15]:


df.columns


# In[16]:


df=df.set_index('citation_id')
df=df.join(class_df)


# In[17]:


x_1=2
x_2=10
for dimension in ext_list:
    print(list(df.columns)[x_1],list(df.columns)[x_2])
    df[dimension]=np.where(df.iloc[:,x_1] != df.iloc[:,x_2], 1, 0)
    df.loc[df.iloc[:,x_1].isnull(), dimension] = np.nan
    df.loc[df.iloc[:,x_2].isnull(), dimension] = np.nan 
    x_1+=1
    x_2+=1


# In[18]:


df.isnull().sum()


# In[19]:


df.head()


# In[20]:


df.info()


# In[21]:


df.describe()


# In[22]:


df.set_index('uuid', inplace=True)
df.select_dtypes(include=[np.number]).to_csv('data/int_ext_cit_v2.csv')

