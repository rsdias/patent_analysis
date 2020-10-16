#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to calculate originality and  application data
# This script prepares the classification data before merging
# Jan 16th, 2020
# Multiple classifications generate an error into the Generality calculation
# I am creating a version with the first class only 

# Jan 7th, 2020


# In[2]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd
import numpy as np
import re

import zipfile as zip
import gzip


# In[3]:


# from the data dictionary

# patent_id: patent number
# field_id:  WIPO technology field ID as derived from crosswalk 
#            http://www.wipo.int/export/sites/www/ipstats/en/statistics/patents/xls/ipc_technology.xls
# sequence:  order in which WIPO technology field appears on patent


# In[4]:


wipo = 'data/wipo.tsv.zip'
dst= 'data/wipo.csv.gz'


# In[5]:


# 
zf = zip.ZipFile(wipo)
df=pd.read_csv(zf.open('wipo.tsv'), sep='\t', dtype='object')

# sample_size=1000
# wipo_df=sampler(wipo, sample_size, sep='\t')


# In[6]:


# # # Keep this for reference!
# # # As of Dec 31st, 2019, I compared the clean to the raw version of citation and patent ids

# # #stripping non-desired characters but keeping the originals for later check - only three changes in citation_id

# wipo_df['patent_id_raw']=wipo_df['patent_id']

# cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
# wipo_df['patent_id']=wipo_df['patent_id'].apply(cleaning_patent)


# In[7]:


#first, construct a table with wipo categories in columns, patent level
#second, 


# In[8]:


df.dtypes


# In[9]:


df.groupby('sequence').patent_id.count()


# In[10]:


df=df[df['sequence']=='0'][['patent_id', 'field_id']]


# In[11]:


df.field_id.value_counts()


# In[12]:


df=df.add_prefix('wipo_')


# In[13]:


df['wipo_field_id']=df['wipo_field_id'].apply('{:0>2}'.format)


# In[14]:


df.rename(columns={ df.columns[0]: "id" }, inplace = True)


# In[15]:


df.head()


# In[16]:


class_system='wipo_field_id'

file_classes=gzip.open('data/classes.csv.gz', 'r')
df_classes=pd.read_csv(file_classes)

df_classes.rename(columns={'id': 'class_id'}, inplace=True)
df_classes=df_classes[df_classes['system']==class_system]

df_classes['class_id']=df_classes['class_id'].apply('{:0>2}'.format)
# df_classes=df_classes.reset_index()

df=df.merge(df_classes, left_on='wipo_field_id', right_on='class_id')


# rank=df.reset_index().groupby(class_system).count()['id'].reset_index()
# rank.rename(columns={class_system: 'id', 'id':class_system}, inplace=True)

# df_classes=df_classes[df_classes['system']==class_system]

# rank=rank.merge(df_classes, left_on='id', right_on='id')
# display.display(rank.groupby('sector_title').sum().sort_values(by=class_system, ascending=False))


# In[17]:


sector_id=df_classes.groupby('sector_title').count().reset_index().iloc[:,:1].reset_index()


# In[18]:


df.head()


# In[19]:


sector_id


# In[20]:


df=df.merge(sector_id, left_on='sector_title', right_on='sector_title')


# In[21]:


df=df[['id','index', 'wipo_field_id']]


# In[22]:


df.rename(columns={'index': 'wipo_sector_id'}, inplace=True)


# In[23]:


#df_classes['wipo_field_id']=df_classes['wipo_field_id'].apply('{:0>2}'.format)


# In[24]:


df.head()


# In[25]:


df.set_index('id').to_csv(dst, compression='gzip')

