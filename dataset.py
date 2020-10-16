#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Jan 30, 2020
# Joined the 5 classification tables available
# to be evaluated:
    # join is left by default
    # because I adopt cit_received as the leftmost data
        # this dataset keep data on the patents who received citation
    # I can make the first join as an 'outer' operation between cit_received and cit_made
    # To be complete, I can begin with patent.csv.gz and make the first two joins with 'outer' type
#     Ill git add now and try this
    

# Jan 29, 2020
# many errors appeared after joining the dataset 
# i rewritten code into simpler scripts
# this script joins variables together to be processed later

# they are:
#     - cit_delay - reads clean_patent and clean_uspatentcitation and calculates delay by patent
#     - cit_made - reads clean_uspatentcitation and calculates citations made 
#     - cit_received - reads clean_uspatentcitation and calculates citations received
#     - cit_tree - reads clean_uspatentcitation and cit_made and calculates parent_citation
#     - generalit - reads wipo and clean_uspatentcitation and calculates generality
#     - originality - reads wipo and clean_uspatentcitation and calculates originality
#     - wipo_first_class - reads wipo and generates wipo_first_class

# it is now way faster, but I cannot know for sure if this is a consequence of coding or something changed in 
# infrastructure. 

# since class is a variable that also appear in non-cited patents, I'll include them in the final step


# Jan, 20th 2020
# join delay and tree data to form the analysis dataset


# In[2]:


import pandas as pd
import numpy as np

import gzip


# In[3]:


def data_read(file, names, usecols, dtype):
    df = pd.read_csv(file, names=names, usecols=usecols, dtype=dtype, index_col='id', header=0)
    dfs.append(df)


# In[4]:


patent='data/cleanpatent.csv.gz'

received='data/cit_received.csv.gz'
made='data/cit_made.csv.gz'
received_delay='data/cit_received_delay.csv.gz'
made_delay='data/cit_made_delay.csv.gz'
# cit_tree = 'data/cit_tree.csv.gz'
originality = 'data/originality.csv.gz'
generality = 'data/generality.csv.gz'

dst='data/dataset.csv.gz'

wipo = 'data/wipo.csv.gz'
#ipcr = 'data/ipcr.csv.gz'
#cpc = 'data/cpc.csv.gz'
#nber = 'data/nber.csv.gz'
#uspc = 'data/uspc.csv.gz'

centrality='data/eigen.csv.gz'
#eigen='data/eigen2.csv.gz'

#self_cit='data/self_cit.csv.gz'
int_ext_cit='data/internal_external_citation.csv.gz'


# In[5]:


dfs=[]


# In[6]:


#adopting patent.csv as the reference of patents
file=gzip.open(patent, 'r')
df = pd.read_csv(file, dtype=object)
df['num_claims']=df['num_claims'].astype(float) #int does not handle NAN values, so using float instead
df.set_index('id', inplace=True)


# In[7]:


#outer join to citation received
#there are patents who received citations that are not in patent.csv.gz
#for example, the very ancient ones

names=['index', 'id', 'cit_received']
usecols=['id', 'cit_received']
dtype={'id':object, 'cit_received':float}

file=gzip.open(received, 'r')
df2 = pd.read_csv(file, names=names, usecols=usecols, dtype=dtype, header=0)
df2.set_index('id', inplace=True)

df=df.join(df2, how='outer')
df['cit_received']=df['cit_received'].fillna(0)
dfs.append(df)
df2=[]


# In[8]:


#i dont see any reason for patents making citations not to appear in patent.csv.gz
#so from this data on, the list of patents is stable
#the number of rows should not change (check)

names=['index', 'id', 'cit_made']
usecols=['id', 'cit_made']
dtype={'id':object}
file=gzip.open(made, 'r')
data_read(file, names, usecols, dtype)


# In[9]:


names=['id', 'cit_received_delay']
dtype={'id':object}
usecols=['id', 'cit_received_delay']
file=gzip.open(received_delay, 'r')
data_read(file, names, usecols, dtype)


# In[10]:


names=['id', 'cit_made_delay']
dtype={'id':object}
usecols=['id', 'cit_made_delay']
file=gzip.open(made_delay, 'r')
data_read(file, names, usecols, dtype)


# In[11]:


# names=['id', 'parent_citation']
# dtype={'id':object}
# usecols=['id', 'parent_citation']
# file=gzip.open(cit_tree, 'r')
# data_read(file, names, usecols, dtype)


# In[12]:


names=['id', 'df_squared','total_citation','herfindal','originality']
dtype={'id':object}
usecols=['id', 'originality']
file=gzip.open(originality, 'r')
data_read(file, names, usecols, dtype)


# In[13]:


names=['id', 'df_squared','total_citation','herfindal','generality']
dtype={'id':object}
usecols=['id', 'generality']
file=gzip.open(generality, 'r')
data_read(file, names, usecols, dtype)


# In[14]:


file=gzip.open(wipo, 'r')
df = pd.read_csv(file, dtype=object)
df.set_index('id', inplace=True)
dfs.append(df)


# In[15]:


# file=gzip.open(ipcr, 'r')
# df = pd.read_csv(file, dtype=object)
# df.set_index('id', inplace=True)
# dfs.append(df)


# In[16]:


# file=gzip.open(ipcr, 'r')
# df = pd.read_csv(file, dtype=object)
# df.set_index('id', inplace=True)
# dfs.append(df)


# In[17]:


# file=gzip.open(cpc, 'r')
# df = pd.read_csv(file, dtype=object)
# df.set_index('id', inplace=True)
# dfs.append(df)


# In[18]:


# file=gzip.open(nber, 'r')
# df = pd.read_csv(file, dtype=object)
# df.set_index('id', inplace=True)
# dfs.append(df)


# In[19]:


# file=gzip.open(uspc, 'r')
# df = pd.read_csv(file, dtype=object)
# df.set_index('id', inplace=True)
# dfs.append(df)


# In[20]:


file=gzip.open(int_ext_cit, 'r')
df = pd.read_csv(file, dtype=object)
df.set_index('index', inplace=True)
dfs.append(df)


# In[21]:


# centrality
file=gzip.open(centrality, 'r')
# df = pd.read_csv(file, dtype=object, usecols=['id','katz', 'pagerank'])
df = pd.read_csv(file, dtype=object, usecols=['id','pagerank'])
df.set_index('id', inplace=True)
dfs.append(df)


# In[22]:


# # eigen
# file=gzip.open(eigen, 'r')
# df = pd.read_csv(file, dtype=object)
# df.set_index('id', inplace=True)
# dfs.append(df)


# In[23]:


# dfs = [df, df_made, df_received_delay]
# dfs = [df.set_index('id') for df in dfs]
df=dfs[0].join(dfs[1:])


# In[24]:


df.info()


# In[25]:


df.sample(n=10).transpose()


# In[26]:


df.describe()


# In[27]:


df.describe(include=[np.object]).transpose()


# In[28]:


# df=df.merge(wipo, left_index=True, right_index=True, how='outer')


# In[29]:


# df.sample(n=10)


# In[30]:


# df.describe()


# In[31]:


df.to_csv(dst, compression='gzip')


# In[32]:


# this code includes WIPO in the dataset
# as class is also part of non-cited patents, I'm not including in here.
# in any case, for some reason this merge could not be done by the method used in the previous
# there is a bug when using read_csv.gz using dtype and indexing. 
# it is a known bug in the community but i do not know why the previous join did not accused the issue
# the method below corrects the issue 

# names=['index', 'id', 'field_id']
# dtype={'id':object}
# usecols=['id', 'field_id']
# # data_read(wipo, names, usecols, dtype)
# wipo = pd.read_csv.gz(wipo, names=names, usecols=usecols, dtype=dtype, header=0)
# wipo['id']=wipo['id'].astype(str)
# wipo=wipo.set_index('id')
# wipo.info()

# dfs.append(wipo)

