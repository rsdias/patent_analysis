#!/usr/bin/env python
# coding: utf-8

# In[1]:


#sampler for citation merges
#Renato Kogeyama

#Miami, Jan 13 2020
# this script filters by kind (this version is filtering by b1 - utility patent grant)
# at this point is matching wipo with patent - but in reality, only patent is necessary

#Miami, Jan 11 2020
#original sampler cannot group citations 
#this way, in case of mergers, there is no way that merged patents are related 
# - ie, allow for the calculation of variables that require a relevant number of successful mergers

#i initially planned to do this by using the classification system
#however, to guarantee citation, i can use the citation list and generate wipo from that original list


# In[ ]:





# In[2]:


import pandas as pd
import numpy as np


# In[3]:


wipo = '/home/rkogeyam/PATENT_CITATION/data/wipo_horiz.csv'
patent = '/home/rkogeyam/PATENT_CITATION/data/patent.csv'
dst = '/home/rkogeyam/PATENT_CITATION/data/wipo_kind_b1.csv'


# In[4]:


wipo_df = pd.read_csv(wipo, index_col='patent_id', dtype={'patent_id':object})
cols=['id', 'type', 'date', 'kind']
patent_df = pd.read_csv(patent, sep='\t', na_values='-', usecols=cols , error_bad_lines=False, index_col=0)


# In[5]:


wipo_df.sample(n=10)


# In[6]:


patent_df.sample(n=10)


# In[7]:


patent_df.dtypes


# In[8]:


patent_df.index=patent_df.index.astype('str')


# In[9]:


wipo_df.index=wipo_df.index.astype('str')


# In[10]:


patent_df.index.dtype


# In[11]:


wipo_df.index.dtype


# In[12]:


# df=patent_df.join(wipo_df, how='inner')  
df=patent_df.merge(wipo_df, how='inner', right_index=True, left_index=True)


# In[13]:


df.isnull().sum()


# In[14]:


df.head()


# In[15]:


df.describe()


# In[16]:





# In[16]:


# for chunk in pd.read_csv(wipo, sep=',', chunksize=10000, dtype={'patent_id': 'str'}):
# #     output=[ i for item in chunk if conditional ]

# # This is equivalent to:
#     test=chunk[chunk['patent_id'].any()=='8393846']
#     if test:
#         print(test)
#     else:
#         continue
# #     for row in chunk:
# #         print(row)
# #         if row['patent_id']=='8393846':
# #             print(row)
# #     else:
# #         continue


# In[17]:


# df.get_chunk().dtypes


# In[18]:


df[df['kind']=='B1'].to_csv(dst)

