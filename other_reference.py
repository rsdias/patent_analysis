#!/usr/bin/env python
# coding: utf-8

# In[1]:


# February 11st, 2020
# Script to evaluate other references
# uuid - unique id
# patent_id - patent number
# text - non-patent literature reference text
# sequence - order in which this reference is cited by the patent


# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import zipfile


# In[ ]:


dst='data/other_ref.csv'


# In[3]:


other='data/otherreference.tsv.zip'
file=zipfile.ZipFile(other, 'r')
df=pd.read_csv(file, sep='\t', engine='python')


# In[ ]:


df.groupby('patent_id').count().to_csv(dst, compression='gzip')

