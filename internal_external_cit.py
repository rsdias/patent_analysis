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

# from determinants_scripts import classes, dtypes

from classification import preprocessing

import gzip

citation='data/cleanuspatentcitation.csv.gz'

usecols=['uuid', 'patent_id', 'citation_id']

file_cit=gzip.open(citation, 'rt')
# citation_df=pd.read_csv(file_cit, usecols=usecols, nrows=100000)
citation_df=pd.read_csv(file_cit, usecols=usecols)


# In[3]:


# class_systems=['wipo']
# class_systems=['wipo', 'ipcr', 'cpc', 'nber']


# In[4]:


get_ipython().run_cell_magic('time', '', "# This approach uses too much memory\n# Try something else\n\nclass_system='wipo'\n    \nclassification = 'data/'+class_system+'.csv.gz'\nfile_class=gzip.open(classification, 'rt')\nclass_df=pd.read_csv(file_class, dtype=object, usecols=[0,1,2])\n\n#join class to patent_id\ndf=preprocessing(class_df, citation_df)\ndf.rename(columns={df.columns[2]:'level1_pat', df.columns[3]:'level2_pat'}, inplace=True)")


# In[5]:


class_df.reset_index(inplace=True)


# In[6]:


#join class to citation_id
df=preprocessing(class_df, df, generality=False)


# In[7]:


#classify far external 
far_ext=class_system+'_far_ext'
df[far_ext]=np.where(df['level1_pat'] != df[df.columns[3]], 1, 0)

#classify external
ext=class_system+'_ext'
df[ext]=np.where(df['level2_pat'] != df[df.columns[4]], 1, 0)


# In[8]:


df.reset_index(inplace=True)
df.info()


# In[9]:


df=df.groupby(['index'])['wipo_far_ext','wipo_ext'].sum()
# df=df[['uuid', far_ext, ext]].set_index('uuid')
# print(df.head())

# #generate the output df if wipo, join if others
# if class_system=='wipo':
#     output=df
# else:
#     output=output.join(df)
        


# In[10]:


# %%time
# # This approach uses too much memory
# # Try something else

# for class_system in class_systems:
    
#     classification = 'data/'+class_system+'.csv.gz'
#     file_class=gzip.open(classification, 'rt')
#     class_df=pd.read_csv(file_class, dtype=object, usecols=[0,1,2])
    
#     #join class to patent_id
#     df=preprocessing(class_df, citation_df)
#     df.rename(columns={df.columns[2]:'level1_pat', df.columns[3]:'level2_pat'}, inplace=True)
    
#     #join class to citation_id
#     df=preprocessing(class_df, df, generality=False)
    
    
#     #classify far external 
#     far_ext=class_system+'_far_ext'
#     df[far_ext]=np.where(df['level1_pat'] != df[df.columns[3]], 1, 0)
    
#     #classify external
#     ext=class_system+'_ext'
#     df[ext]=np.where(df['level2_pat'] != df[df.columns[4]], 1, 0)
    
#     df=df[['uuid', far_ext, ext]].set_index('uuid')
#     print(df.head())

#     #generate the output df if wipo, join if others
#     if class_system=='wipo':
#         output=df
#     else:
#         output=output.join(df)
        


# In[11]:


# output.info()
df.info()


# In[12]:


# output.describe()


# In[13]:


df.to_csv('data/internal_external_citation.csv.gz', compression='gzip')

