#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to clean patent.tsv

#Aug 18st, 2020
#convert to gzip input and output

# Jan 20th, 2020
# There are citation_ids larger than 7 characters and smaller than 4
# Larger are usually applications, smallers tend to be errors
# I am keeping than so calculations on forward citations are accurate
# When matching by citation_id, it must be previously filtered

# as of Jan 9th, 2020, there are entries to be evaluated
# for now, error_bad_lines=False skips those entries


# In[2]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
#from sampler import sampler

import pandas as pd
import numpy as np
import re
import gzip
import csv

import zipfile as zip


# In[3]:


# patent.csv
# id:       patent this record corresponds to 
# type:     category of patent. Usually "Design", "reissue", etc.
# number:   patent number
# country:  country in which patent was granted (always US)
# date:     date when patent was granted
# abstract: abstract text of patent
# title:    title of patent
# kind:     WIPO document kind codes (http://www.uspto.gov/learning-and-resources/support-centers/electronic-business-center/kind-codes-included-uspto-patent)
# num_claims:number of claims
# filename: name of the raw data file where patent information is parsed from


# In[4]:


# get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


src= 'data/patent.tsv.zip'
dst= 'data/cleanpatent.csv.gz'


# In[6]:


cols=['id', 'num_claims', 'date', 'type', 'kind']


# In[7]:


file_name = "data/patent.tsv.zip"
f_name = "patent.tsv"
# Selecting the zip file.
zf = zip.ZipFile(file_name)
# Reading the selected file in the zip.
df = pd.read_csv(zf.open(f_name), delimiter="\t", quoting = csv.QUOTE_NONNUMERIC, dtype=object)


# In[8]:


# file_src=gzip.open(src, 'r')
# df = pd.read_csv(file_src, sep='\t', usecols=cols, error_bad_lines=False, dtype=object, quoting = csv.QUOTE_NONNUMERIC)


# In[9]:


df.info()


# In[10]:


df=df.astype(object)


# In[11]:


df.dtypes


# In[12]:


# get_ipython().run_cell_magic('time', '', '# Keep this for reference!\n# As of Dec 31st, 2019, I compared the clean to the raw version of citation and patent ids\n\n# stripping non-desired characters but keeping the originals for later check - only three changes in citation_id\n# df[\'id\']=df[\'id\'].astype(object)\ncleaning_patent=lambda x:re.sub(\'([^a-zA-Z0-9]+)\', "", x)\ndf[\'id\']=df[\'id\'].astype(object).apply(cleaning_patent)')


# In[13]:


df.date.replace({'-00':'-01'}, regex=True, inplace=True)
#ideally, I would control the modification here


# In[14]:


df.id.str.len().value_counts()


# In[15]:


df[df['id'].apply(lambda x: len(x)>13)]


# In[16]:


# drop five rows with error
df=df[df['id'].apply(lambda x: len(x)<13)]


# In[17]:


df['num_claims']=pd.to_numeric(df['num_claims'], errors='coerce')


# In[18]:


df[df['kind'].apply(lambda x: len(str(x))>13)]


# In[19]:


df=df[df['kind'].apply(lambda x: len(str(x))<13)]


# In[20]:


df.groupby('kind').count()


# In[21]:


df.groupby('type').count()


# In[22]:


df.describe(include='all')
# df.describe()


# In[23]:


df['num_claims'].hist()


# In[24]:


df.dtypes


# In[25]:


df.set_index('id').to_csv(dst, compression='gzip')

