#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from IPython.display import display, HTML

src='data/cpc_current.tsv'
dst='data/cpc.csv'


# In[2]:


# uuid			unique id
# patent_id		patent number

# section_id		cpc section  
# 				(A = Human Necessitites, B = Performing Operations; Transporting, 
# 				C = Chemistry; Metallurgy, D = Textiles; Paper, E = Fixed Constructions, 
# 				F = Mechanical Engineering; Lighting; Heating; Weapons; Blasting Engines or Pumps, 
# 				G = Physics, H = Electricity, Y = General Tagging of New Technological Developments)

# subsection_id	cpc subsection id: http://www.uspto.gov/web/patents/classification/cpc.html
# group_id		cpc group id: http://www.uspto.gov/web/patents/classification/cpc.html
# subgroup_id		cpc subgroup id: http://www.uspto.gov/web/patents/classification/cpc.html
# category		cpc category (primary or additional)
# sequence		order in which cpc class appears in patent file


# In[3]:


usecols=['patent_id', 'section_id', 'subsection_id', 'group_id', 'sequence']
df = pd.read_csv(src, sep='\t', usecols=usecols)


# In[4]:


df=df[df['sequence']==0]


# In[5]:


df=df.drop(['sequence'], axis=1)


# In[6]:


df.info()


# In[7]:


columns=list(df)[1:-1]
for i in columns:
    print('\nTop 10 ', i)
    print(df[i].value_counts().head(10))
    df[i].value_counts().plot.bar()
#     print(df[i].value_counts())
#     display(HTML(df[i].value_counts().to_html()))
#     display(HTML(df[i].value_counts().reset_index().to_html()))


# In[8]:


# display(HTML(df['main_group'].value_counts().reset_index().to_html()))


# In[9]:


df=df.add_prefix('cpc_')


# In[10]:


df.rename(columns={ df.columns[0]: "id" }, inplace = True)


# In[11]:


df.set_index('id').to_csv(dst)
# df.iloc[:, 0:-1].to_csv(dst)

