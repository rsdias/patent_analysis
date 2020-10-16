#!/usr/bin/env python
# coding: utf-8

# In[1]:


#this scripts takes the output from var_builder
#converts timedelta to numeric
#calculates backward citation average delay
#calculates forward citation average delay
#counts forward and backward citations

# Jan 19, 2020
# Joining is not generating matches
# probably is an issue with dtype
# i am running joining with inner but it should be updated later with outer.


# In[2]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd
import numpy as np
import re

import gzip


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


src='data/var_builder.csv.gz'
cit_received_delay = 'data/cit_received_delay.csv.gz'
cit_made_delay='data/cit_made_delay.csv.gz'


# In[5]:


cols=['patent_id','citation_id', 'cit_delay' ]
dtypes={'patent_id': object, 'citation_id': object, 'cit_delay': np.float64}

file_varbuilder=gzip.open(src, 'r')
df = pd.read_csv(file_varbuilder, usecols=cols)


# In[6]:


df.info()


# In[7]:


df.dtypes


# In[8]:


# df['cit_delay']=pd.to_timedelta(df['cit_delay']).dt.components.days/365 
#for some reason dt.days stopped working. dt.components came around and is working


# In[9]:


# output: patent-level data
# if group by citation_id, the delay will give the average delay gives how much time it took,
#    in average, for a patent to receive citations
# it is a measure of time to become influent

received_delay=df.groupby('citation_id').mean()
# back_delay.rename(columns={'count': 'back_citation', 'mean':'mean_back_delay'}, inplace=True)
received_delay.head()


# In[10]:


received_delay.dropna(inplace=True)


# In[11]:


received_delay.dtypes #this will tell us if i am trying to join data of the same format


# In[12]:


received_delay.hist()


# In[13]:


received_delay[received_delay["cit_delay"]<received_delay["cit_delay"].quantile(0.01)]


# In[14]:


received_delay[received_delay["cit_delay"]>received_delay["cit_delay"].quantile(0.99)]


# In[15]:


received_delay.to_csv(cit_received_delay, compression='gzip')


# In[16]:


# if you group by patent_id, the delay will give a measure of how far back the patent is rooted.

made_delay=df.groupby('patent_id').mean()
# forw_delay.rename(columns={'count': 'forw_citation', 'mean':'mean_forw_delay'}, inplace=True)
made_delay.head()


# In[17]:


made_delay.dropna(inplace=True)


# In[18]:


made_delay.dtypes


# In[19]:


made_delay.hist()


# In[20]:


made_delay[made_delay["cit_delay"]<made_delay["cit_delay"].quantile(0.01)].sort_values(by=['cit_delay'], ascending=False)


# In[21]:


made_delay[made_delay["cit_delay"]>made_delay["cit_delay"].quantile(0.99)].sort_values(by=['cit_delay'], ascending=True)


# In[22]:


made_delay.to_csv(cit_made_delay, compression='gzip')

