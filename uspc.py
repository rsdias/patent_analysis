#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from IPython.display import display, HTML

src='data/uspc_current.tsv'
dst='data/uspc.csv'


# In[2]:


# uuid			unique id
# patent_id		patent number
# mainclass_id	uspc mainclass current
# subclass_id		uspc subclass current
# sequence		order in which uspc class appears in patent file


# In[3]:


usecols=['patent_id', 'mainclass_id', 'subclass_id', 'sequence']
df = pd.read_csv(src, sep='\t', usecols=usecols)


# In[4]:


df=df[df['sequence']==0]


# In[5]:


df=df.drop(['sequence'], axis=1)


# In[6]:


df.info()


# In[7]:


# columns=list(df)
# for i in columns:
#     print('\nTop 10', i)
#     print(df[i].value_counts().head(10))
# #     print(df[i].value_counts())
# #     display(HTML(df[i].value_counts().to_html()))
# #     display(HTML(df[i].value_counts().reset_index().to_html()))


# In[8]:


# for i in columns:
#     df[i].value_counts().plot.bar()


# In[9]:


# display(HTML(df['main_group'].value_counts().reset_index().to_html()))


# In[10]:


df=df.add_prefix('uspc_')


# In[11]:


df.rename(columns={ df.columns[0]: "id" }, inplace = True)


# In[12]:


df.set_index('id').to_csv(dst)

