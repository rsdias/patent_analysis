#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 12st, 2020

# This script compares patent and citing in each classification system
# Second level matches specifications of Nemet and Johnson 2012
# Previous versions are not working and they are difficult to debug


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


# 1-Match class to patent_id and to citation_id
# 2-Create a variable coded with 1 if the classes are different, 0 if they are the same
# 3

# In[5]:




#create classes dataset
class_df=pd.read_csv('data/wipo.csv', dtype=object, usecols=[0,1,2])
class_df=class_df.astype(str)
class_df=class_df.set_index('id')

# for class_system in class_systems:
#     classification = 'data/'+class_system+'.csv'
#     class_x=pd.read_csv(classification, dtype=object, usecols=[0,1,2])
#     class_x=class_x.astype(str)
#     class_x=class_x.set_index('id')
#     class_df=class_df.join(class_x)


# In[6]:


class_df.dtypes


# In[7]:


df=df.astype(str)
df.set_index('patent_id', inplace=True)


# In[8]:


df.dtypes


# In[9]:


df=df.join(class_df)


# In[10]:


df.head()
# dimensions=list(df.columns)
# dimensions.remove('uuid')
# dimensions.remove('citation_id')
# dimensions = [sub.replace('_id', '') for sub in dimensions] 


# In[11]:


# df.describe()


# In[12]:


# df.set_index('uuid', inplace=True)
# df.select_dtypes(include=[np.number]).to_csv('data/int_ext_cit_v2.csv')


# In[13]:


df.set_index('citation_id', inplace=True)
df=df.join(class_df, lsuffix='_pat', rsuffix='_cit')
# df.describe()


# In[14]:


df.set_index('uuid')
df['wipo_sector_ext']=np.where(df.loc[:,'wipo_sector_id_pat'] != df.loc[:,'wipo_sector_id_cit'], 1, 0)
df['wipo_field_ext']=np.where(df.loc[:,'wipo_field_id_pat'] != df.loc[:,'wipo_field_id_cit'], 1, 0)
df.loc[df.loc[:,'wipo_sector_id_pat'].isnull(), 'wipo_sector_ext'] = np.nan
df.loc[df.loc[:,'wipo_field_id_pat'].isnull(), 'wipo_field_ext'] = np.nan 
df.loc[df.loc[:,'wipo_sector_id_cit'].isnull(), 'wipo_sector_ext'] = np.nan
df.loc[df.loc[:,'wipo_field_id_cit'].isnull(), 'wipo_field_ext'] = np.nan 


# In[15]:


df.describe()


# In[16]:


df.sample(n=50)

