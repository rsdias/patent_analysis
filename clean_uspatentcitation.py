#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to clean uspatentcitation.tsv

# Feb 7th, 2020
# I am adding a cut for citation date
# it cannot be older than 07-31-1790 (the first patent ever issued)

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
import datetime
import csv
import gzip
import zipfile as zip

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

src= r'data/uspatentcitation.tsv.zip'
dst= 'data/cleanuspatentcitation.csv'


# In[5]:


df=pd.read_csv(src, sep='\t', error_bad_lines=False, quoting = csv.QUOTE_NONNUMERIC)


# In[6]:


df=df.astype(str)


# In[7]:


df.dtypes


# In[8]:


get_ipython().run_cell_magic('time', '', "#stripping trailing white spaces - no changes\ndf['patent_id'] = df['patent_id'].str.strip()\ndf['citation_id'] = df['citation_id'].str.strip()")


# In[9]:


get_ipython().run_cell_magic('time', '', "# Keep this for reference!\n# As of Dec 31st, 2019, I compared the clean to the raw version of citation and patent ids\n\n# stripping non-desired characters but keeping the originals for later check - only three changes in citation_id\n\ndf['citation_id_raw']=df['citation_id']\ndf['patent_id_raw']=df['patent_id']")


# In[10]:


get_ipython().run_cell_magic('time', '', 'cleaning_patent=lambda x:re.sub(\'([^a-zA-Z0-9]+)\', "", x)\ndf[\'citation_id\']=df[\'citation_id\'].apply(cleaning_patent)\n\n# # #this is taking a lot of time, evaluate alternatives')


# In[11]:


get_ipython().run_cell_magic('time', '', "df['patent_id']=df['patent_id'].apply(cleaning_patent)")


# In[12]:


df.date.replace({'-00':'-01'}, regex=True, inplace=True)


# In[13]:


get_ipython().run_cell_magic('time', '', 'df[\'date\']=pd.to_datetime(df[\'date\'], format="%Y-%m-%d", errors=\'coerce\') \n# first_patent = datetime.date(1790, 7, 31)')


# In[14]:


first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #I tweaked slightly because there is a citation to the patent n1 that seems correct


# In[15]:


#as for Aug 11, 2020, two problems arose:
#- some name fields present EOF characters
#- some lines are missing their linebreaks
# this is the correction of these issues
clean_doublespace=lambda x:re.sub('\s\s', '\s', x)
df['name']=df['name'].apply(clean_doublespace)


# In[16]:


#citation with dates previous to the inauguration of USPTO office
df[df['date']<first_patent][['patent_id','citation_id','date']]


# In[17]:


len(df['date']) - df['date'].count()


# In[18]:


get_ipython().run_cell_magic('time', '', "#patents with wrong dates should not be dropped\n#the best way is to search for the correct date\n#i can do in a separated script\n#this would improve the results - other citation dates can be bugged\n\n#for now, because there are just a few mistakes, i just exclude the date\n#excluding dates from patents with wrong dates\ndf['date']=df['date'].apply(lambda x: np.nan if x < first_patent else x)")


# In[19]:


len(df['date']) - df['date'].count()


# In[20]:


# print(df[df['patent_id']!=df['patent_id_raw']][['patent_id','patent_id_raw']])


# In[21]:


# print(df[df['citation_id']!=df['citation_id_raw']][['citation_id', 'citation_id_raw']])


# In[22]:


df[df['citation_id'].apply(lambda x: len(x)>7)]


# In[23]:


df[df['citation_id'].apply(lambda x: len(x)<4)]


# In[24]:


df.citation_id.str.len().value_counts()


# In[25]:


df.to_csv(dst)

