#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from IPython.display import display, HTML

src='data/ipcr.tsv'
dst='data/ipcr.csv'


# In[2]:


# uuid:					unique id
# patent_id:			patent number
# classification_level:	ipc classification level (A = advanced level) 
# section:				ipc section (A = Human Necessitites, B = Performing Operations; Transporting, C = Chemistry; Metallurgy, D = Textiles; Paper, E = Fixed Constructions, F = Mechanical Engineering; Lighting; Heating; Weapons; Blasting, G = Physics, H = Electricity)
# ipc_class:			ipc class
# subclass:				ipc subclass
# main_group:			ipc group
# subgroup:				ipc subgroup
# symbol_position:				ipc symbol ( F = first or sole invention information IPC; L = any second or succeeding invention information IPC and any non-invention information IPC)
# classification_value:			ipc classification value ( I = invention information; N = non-invention information)
# classification_status:		ipc classification status ( B = Basic or Original)
# classification_data_source:	ipc classification data source ( H = Human - Generated; M = Machine - Generated; G = Generated via Software)
# action_date:					issue date of the patent grant
# ipc_version_indicator:		ipc version indicator
# sequence:						order in which ipc class appears in patent file

#IPC is hierarchical
#I am arbitrarily adopting the first three levels (section, class, subclass)


# In[3]:


usecols=['patent_id', 'section', 'ipc_class', 'subclass', 'sequence']
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
    print('\nTop 10', i)
    print(df[i].value_counts().head(10))
#     print(df[i].value_counts())
#     display(HTML(df[i].value_counts().to_html()))
#     display(HTML(df[i].value_counts().reset_index().to_html()))


# In[8]:


columns


# In[9]:


for i in columns:
    df[i].value_counts().plot.bar()


# In[10]:


# display(HTML(df['main_group'].value_counts().reset_index().to_html()))


# In[11]:


df=df.add_prefix('ipcr_')


# In[12]:


df.rename(columns={ df.columns[0]: "id" }, inplace = True)


# In[13]:


df = df.applymap(lambda x: str(x).upper())


# In[14]:


df.columns


# In[15]:


df['ipcr_section'].value_counts()


# In[16]:


df[~df['ipcr_section'].isin(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])]


# In[17]:


df=df[df['ipcr_section'].isin(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'])]


# In[18]:


# df.iloc[:, 1:-1].to_csv(dst)
df.set_index('id').to_csv(dst)

