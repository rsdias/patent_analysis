#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
# Sao Paulo, Aug 14, 2020
# Script to check patcitonly2.csv
Helps to test intermediate steps of the code

"""


# In[2]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd
import numpy as np
import re
import datetime

import matplotlib.pyplot as plt


# In[3]:


# uspatentcitation.tsv
# uuid:         unique id
# patent_id:    patent number
# citation_id:  identifying number of patent to which select patent cites
# date:         date select patent (patent_id) cites patent (citation_id)
# name:         name of cited record
# kind:         WIPO document kind codes 
#               (http://www.uspto.gov/learning-and-resources/support-centers/electronic-business-center/kind-codes-included-uspto-patent)	2002 and After
# country:      country cited patent was granted (always US)
# category:     who cited the patent (examiner, applicant, other etc) - 2002 and After
# sequence:     order in which this reference is cited by select patent	all


# In[4]:


# src= r'/home/rkogeyam/PATENT_CITATION/data/patcitonly2.csv'
src= r'/home/rkogeyam/PATENT_CITATION/data/uspatclean_selfcit.csv'
# dst= '/home/rkogeyam/PATENT_CITATION/data/cleanuspatentcitation.csv'


# In[5]:


df=pd.read_csv(src, dtype=object)


# In[6]:


df.dtypes


# In[7]:


df[[0]] = df[[0]].astype(str) #type object may contain mixed types


# In[8]:


df[df[0].apply(lambda x: len(x)>7)]


# In[9]:


df[df[0].apply(lambda x: len(x)<7)]


# In[10]:


df[0].str.len().value_counts()


# In[11]:


# pat='data/uspatclean_selfcit.csv'
# df=pd.read_csv(pat)
# df.dtypes


# In[12]:


df.groupby([0])[0].count().nlargest(n=15)


# In[13]:


# df.groupby([1])[0].count().nlargest(n=15)


# In[14]:


# pat='data/only_uuid_pat_cit.csv'
# df=pd.read_csv(pat)
# df.dtypes
# df.uuid.str.len().value_counts()


# In[15]:


# self_cit='data/self_cit.csv'
# df=pd.read_csv(self_cit)
# df.dtypes
# df.uuid.str.len().value_counts()


# In[16]:





# In[16]:


# df['pagerank'].nlargest(15)

