#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to read application data


# In[2]:


import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler

import pandas as pd


# In[ ]:


# from the data dictionary

# id:          application id assigned by USPTO
# patent_id:   patent number
# series_code: application series; "D" for some designs; 
#              (http://www.uspto.gov/web/offices/ac/ido/oeip/taf/filingyr.htm)
# number:      unique applicaiton identifying number
# country:     country this application was filed in
# date:        date of application filing


# In[3]:


fname = r'/home/rkogeyam/PATENT_CITATION/data/application.tsv'
patent= r'/home/rkogeyam/PATENT_CITATION/data/patent.csv'


# In[4]:


sample_size=100
df=sampler(fname, sample_size, sep='\t')


# In[5]:


df.head()


# In[ ]:


pt_df = pd.read_csv(patent, sep='\t', na_values='-', usecols=[0,4], error_bad_lines=False, index_col=0, dtype={0: object})


# In[ ]:


df=pd.merge(df, pt_df, how='left', left_on='patent_id', right_index=True)

