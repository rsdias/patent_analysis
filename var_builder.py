#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to evaluate citation delay
# Backward citation - citation made by a patent
# Forward citation - citation received by a patent

# Renato Kogeyama

# Aug 19, 2020
# Included gzip
# Run with latest database


# Feb 07, 2020
# The main offensor of performance in this script is the transformation to timedelta
# the solution is to change to numpy
# https://stackoverflow.com/questions/52274356/conversion-of-a-timedelta-to-int-very-slow-in-python

# Jan 17 2020
# Join cit_delay with var_builder
# The only thing var_builder was doing was including kind and type 


# Jan 03 2020
# Miami
# I am using this script to calculate the average delay in citation - to follow Hall et al, 2001
# patent.csv has the following columns
# id 	type 	number 	country 	date 	abstract 	title 	kind 	num_claims 	filename
# interest on id, type, date, kind, num_claims

# I use two sources, uspatentcitation.tsv and patent.csv
# The first is a citation-level dataset with information about the citing patent
# The second is a patent-level dataset with information about the patent

# Cleaning
# I tested in other scripts the quality of the patent identifier
# It does not require cleaning - only 4 erros from 6 million patents
# The cleaning script is there anyway

# Merging
# I merge on the citation level (df)


# --

# First U.S. Patent Issued Today in 1790


# July 31, 2001
# Press Release
# #01-33

# On July 31, 1790 Samuel Hopkins was issued the first patent for a process 
# of making potash, an ingredient used in fertilizer. The patent was signed by 
# President George Washington. Hopkins was born in Vermont, but was living in 
# Philadelphia, Pa. when the patent was granted.

# The first patent, as well as the more than 6 million patents issued since then, 
# can be seen on the Department of Commerce's United States Patent and Trademark 
# Office website at www.uspto.gov. The original document is in the collections of 
# the Chicago Historical Society.


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gzip


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


citation_df = '/home/rkogeyam/PATENT_CITATION/data/cleanuspatentcitation.csv.gz'
# cit_tree = '/home/rkogeyam/PATENT_CITATION/data/cit_tree.csv'

patent= 'data/cleanpatent.csv.gz'
dst='data/var_builder.csv.gz'

# citation_df = r'/home/rkogeyam/PATENT_CITATION/data/uspatentcitation.tsv'
# dst = '/home/rkogeyam/PATENT_CITATION/data/back_cit_delay.csv'
# dst_forw = '/home/rkogeyam/PATENT_CITATION/data/forw_cit_delay.csv'


# In[5]:


get_ipython().run_cell_magic('time', '', "file_citation=gzip.open(citation_df, 'r')\ndf = pd.read_csv(file_citation, usecols=['patent_id', 'citation_id', 'date'], dtype=object)")


# In[6]:


get_ipython().run_cell_magic('time', '', "file_patent=gzip.open(patent, 'r')\npt_df = pd.read_csv(file_patent, usecols=['id', 'date'],index_col=0, dtype=object)")


# In[7]:


# df=df.iloc[:,1:]


# In[8]:


df.head()
# df.get_chunk().head()


# In[9]:


pt_df.head()
# pt_df.get_chunk().head()


# In[10]:


get_ipython().run_cell_magic('time', '', 'df=df.rename(columns = {\'date\':\'citation_date\'})\ndf[\'citation_date\']=pd.to_datetime(df[\'citation_date\'], format="%Y-%m-%d", errors=\'coerce\') \n# df[\'citation_date\'].apply[lambda x: np.datetime64(x)]')


# In[11]:


get_ipython().run_cell_magic('time', '', "# merge between patent data and citations on patent_id (citing)\n# merging on the citation dataset drops patents without citing\n# later i could standardize to make patent_id index and use join instead of merge\n\ndf=pd.merge(df, pt_df, how='inner', left_on='patent_id', right_index=True)")


# In[12]:


df.info()


# In[13]:


get_ipython().run_cell_magic('time', '', '# date format to allow calculations\ndf=df.rename(columns = {\'date\':\'patent_date\'})\ndf[\'patent_date\']=pd.to_datetime(df[\'patent_date\'], format="%Y-%m-%d", errors=\'coerce\') #conversao de string para data\n# df[\'patent_date\'].apply[lambda x: np.datetime64(x)]')


# In[14]:


# df.shape


# In[15]:


# if I do not drop nans, the script raises an error later when converting day interval into years
# I could substitute with average instead of dropping, this way I do not lose the citation info
# however, not always it will be possible to average - cases where there is ony one citation, for example
# For this reason, at this point, I'll keep the NAN and circumvent the issues as they arise

# df=df.dropna()


# In[16]:


# df.shape


# In[17]:


get_ipython().run_cell_magic('time', '', "# delay is the time interval between grant and citation\ndf['cit_delay']=df['patent_date'].sub(df['citation_date'], axis=0)\n\n# convert to date format\ndf['cit_delay']=pd.to_timedelta(df['cit_delay'])")


# In[18]:


df.sort_values('cit_delay').head()


# In[19]:


df.sort_values('cit_delay').tail()


# In[20]:


# def convert_to_delta(x):
#     try:
#         return x/np.timedelta64(1, 'Y')
#     except:
#         return np.nan


# In[21]:


get_ipython().run_cell_magic('time', '', "# convert to interval in years\n# df['cit_delay']=df['cit_delay'].dt.days/360\n\n# this is the may offensor of performance\n# change to numpy\n# https://stackoverflow.com/questions/52274356/conversion-of-a-timedelta-to-int-very-slow-in-python\n\n# this takes 40min\ndf['cit_delay']=pd.to_timedelta(df['cit_delay']).dt.components.days/365\n\n# lets try this alternative\n# df['cit_delay']=df['cit_delay'].apply(lambda x: convert_to_delta(x))\n# does not work")


# In[22]:


df.describe()


# In[23]:


df.head()


# In[24]:


get_ipython().run_cell_magic('time', '', 'df.hist()')


# In[25]:


#Check outliers
df[df["cit_delay"]>df["cit_delay"].quantile(0.15)].sort_values(by=['cit_delay'], ascending=True)


# In[26]:


df.head()


# In[27]:


df[df["cit_delay"]<df["cit_delay"].quantile(0.85)].sort_values(by=['cit_delay'], ascending=False)


# In[28]:


df.to_csv(dst, compression='gzip')

