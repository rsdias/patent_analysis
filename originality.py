#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to calculate originality

# Generality: how diverse is the impact of a patent
# This is done by calculating the herfindal index of citing patents


# In[2]:


# Jan 22th, 2020
# Copy and paste from generality
# Join generality and generality_2
# mirror the script to reflect originality
# the only difference should be to change 'citation_id' by 'patent_id' in some fields
# total citations tend to be much smaller


# Jan 16th, 2020
# Due to performance problems in the HPC, this script was divided in two, the script following this is generality_2
# generality > 1 is not an error, but a consequence of adopting WIPO
# it seems that the original calculation had only one class per patent
# WIPO provides multiple classes - so when you divide by the total number of citations, 
#  you do not have the proportion of classes cited anymore
# to correct this issue, I can calculate Generality and Originality based only on the first WIPO class

# Jan 13th, 2020
# Script is running but there are two major issues
# - there should not exist generality > 1 , so there is an error in calculation
# - too many NANs (about 400k), but I will tackle this issue in 'too_many_nans.ipynb'

# to tackle the first problem, I'll begin by creating a subset of the database
# to do that, I'll use USPTO classification system


# In[3]:


# Trying to save memory is leading to a small nightmare 
# I am postponing the use of dask modules


# In[4]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd
import numpy as np
import re

import dask.dataframe as dd

import gzip


# In[5]:


# wipo_horiz.csv
# from wipo_horiz.ipynb
# Original WIPO classification reshaped
# patent_id:    patent number
# field_id_n :  'n' is the WIPO class

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


# In[6]:


wipo = '/home/rkogeyam/PATENT_CITATION/data/wipo.csv.gz' #avoid multiple classes
citation= '/home/rkogeyam/PATENT_CITATION/data/cleanuspatentcitation.csv.gz'

dst= '/home/rkogeyam/PATENT_CITATION/data/originality_temp.csv.gz'


# In[7]:


get_ipython().run_cell_magic('time', '', "usecols=['id','wipo_sector_id']\ndtype={'id':object,'wipo_sector_id':object}\n\nfile_wipo=gzip.open(wipo, 'r')\nwipo_df=pd.read_csv(file_wipo, usecols=usecols, dtype=dtype)\n# wipo_df=pd.read_csv(wipo)\n\nusecols=['patent_id', 'citation_id']\ndtype={'patent_id':object,'citation_id':object}\nfile_cit=gzip.open(citation, 'r')\ndf=pd.read_csv(file_cit, usecols=usecols, dtype=dtype)\n\n# sample_size=100\n# wipo_df=sampler(wipo, sample_size)\n# citation_df=sampler(citation, sample_size)")


# In[8]:


get_ipython().run_cell_magic('time', '', "#citation level dataset\n#join is faster than merge\nwipo_df['id']=wipo_df['id'].astype(str)\ndf=df.astype(str)\n\nwipo_df.set_index('id', inplace=True)\ndf.set_index('citation_id', inplace=True)\n#different from generality - we want to know the class of cites made\n\ndf=df.join(wipo_df, how='inner')  \n\n#the left dataframe is citation df, which is indexed by patent_id\n#when later on I group by citation_id is very possible that NaNs appear")


# In[9]:


df.info()


# In[10]:


df.describe()


# In[11]:


df.sample(n=5)


# In[12]:


df.to_csv(dst, compression='gzip')


# In[13]:


# #from generality_2

# # group on citation_id - thus adding all patents citing one receiver (citation_id)
# # thus this is generality
# # its the impact of a given patent

# # the index is equivalent to 1 - herfindal
# # this way, the closer to 1, the more general

# # the denominator is total citations squared
# # should be easy to check with citation values
# total_citation=df.groupby('patent_id').count().iloc[:,0] #different from generality
# total_citation=np.square(total_citation)

# # the numerator is the sum of the squares of citations in each class
# df=df.groupby('patent_id').sum().fillna(0) #in theory, I would not need fillna, check later
# df=np.square(df) #element-wise squaring
# df=df.sum(axis='columns') #sum all columns, per row

# df=pd.concat([df, total_citation], axis=1)
# df.columns=['df_squared', 'total_citation']
# #herfindal 

# df['herfindal']=df['df_squared']/df['total_citation'] #its a measure of concentration

# df['output']=1-df['herfindal'] # as defined in Hall et al, 2001

# df.to_csv(dst)

