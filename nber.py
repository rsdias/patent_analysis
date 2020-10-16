#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from IPython.display import display, HTML

src='data/nber.tsv'
dst='data/nber.csv'


# In[2]:


# uuid:           unique id
# patent_id:      patent number
# category_id:    National Bureau of Economic Research (NBER) technology category ID
# subcategory_id: NBER subcategory ID 


# In[3]:


usecols=['patent_id', 'category_id', 'subcategory_id']
df = pd.read_csv(src, sep='\t', usecols=usecols)


# In[4]:


df.info()


# In[5]:


df.groupby(['category_id']).count()


# In[6]:


df.groupby(['category_id', 'subcategory_id']).count()


# In[7]:


# columns=list(df)[1:]
# for i in columns:
#     print('\n Top 5 ', i)
#     print(df[i].value_counts().head())
#     df[i].plot.bar()
# #     print(df[i].value_counts())
# #     display(HTML(df.groupby(['nber_category_id']).count().to_html()))
# #     display(HTML(df[i].value_counts().reset_index().to_html()))


# In[8]:


# display(HTML(df['main_group'].value_counts().reset_index().to_html()))


# In[9]:


df=df.add_prefix('nber_')


# In[10]:


df.rename(columns={ df.columns[0]: "id" }, inplace = True)


# In[11]:


df.set_index('id').to_csv(dst)

