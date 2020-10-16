#!/usr/bin/env python
# coding: utf-8

# In[7]:


#Miami, December 27th, 2019
#Renato Kogeyama

# Due bad performance, I am updating the script to more efficient coding

# This script generates a citation ouput with patent|backward citation|cumulated backward citation | year
# The output generates a citation record by year, considering direct and indirect citation


# In[8]:


import pandas as pd
import re
import matplotlib.pyplot as plot

import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler


# In[9]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[10]:


fname = r'/home/rkogeyam/PATENT_CITATION/data/uspatentcitation.tsv'
dst = '/home/rkogeyam/PATENT_CITATION/cit_tree.csv'


# In[ ]:


get_ipython().run_cell_magic('time', '', "# df=pd.read_csv(fname, sep='\\t')\n\nsample_size=100\ndf=sampler(fname, sample_size, sep='\\t')")


# In[ ]:


df['patent_id']=df['patent_id'].astype(str)


# In[ ]:


df['citation_id']=df['citation_id'].astype(str)


# In[ ]:


df.shape


# In[ ]:


df.dtypes


# In[10]:


# drop rows for which column citation_id has a length smaller than 5
indexNames = df[df['citation_id'].map(len) < 5].index
df.drop(indexNames , inplace=True)


# In[11]:


# drop rows for which column patent_id has a length smaller than 5
indexNames = df[df['patent_id'].map(len) < 5].index
df.drop(indexNames , inplace=True)


# In[12]:


df.shape


# In[13]:


get_ipython().run_cell_magic('time', '', '#stripping non desired characters but keeping the originals for later check\n#could merge unwanted information\ncleaning_patent=lambda x:re.sub(\'([^a-zA-Z0-9]+)\', "", x)\ndf[\'citation_id\']=df[\'citation_id\'].apply(cleaning_patent)\ndf[\'patent_id\']=df[\'patent_id\'].apply(cleaning_patent)\n# df[\'citation_id\'] = df[\'citation_id\'].str.extract(\'([a-zA-Z0-9]+)\', expand=True)\n# df[\'patent_id\'] = df[\'patent_id\'].str.extract(\'([a-zA-Z0-9]+)\', expand=True)')


# In[14]:


#stripping trailing white spaces
df['patent_id'] = df['patent_id'].str.strip()
df['citation_id'] = df['citation_id'].str.strip()


# In[15]:


get_ipython().run_cell_magic('time', '', "#to avoid problems when converting object to datetime format\n#replacing day or month would not affect the output\ndf.date.replace({'-00':'-01'}, regex=True, inplace=True)\n#replacing the year could be more problematic\n#for now, I am just dropping")


# In[16]:


get_ipython().run_cell_magic('time', '', "df['date']=pd.to_datetime(df.date,format='%Y-%m-%d', errors='coerce') #attention to date format - original data is year-month-day\n# df['date_format']=pd.to_datetime(df.date,format='%Y-%m-%d', errors='coerce')")


# In[17]:


df.shape


# In[18]:


get_ipython().run_cell_magic('time', '', "#first, i'll run only patents with some kind of citation\n#as we have many zero citations in the dataset, this should decrease processing time\n\nback_citation=df.groupby(['citation_id']).count().iloc[:, 1].reset_index() #reset_index returns dataframe\nforw_citation=df.groupby(['patent_id']).count().iloc[:, 1].reset_index()\n# back_citation=df.groupby(['citation_id']).count() ")


# In[19]:


back_citation.rename(columns={'patent_id': 'back_citation'}, inplace=True) #index: 'citation_id'
forw_citation.rename(columns={'citation_id': 'forw_citation'}, inplace=True) #index: 'patent_id'


# In[ ]:


back_citation.head()


# In[ ]:


forw_citation.head()


# In[20]:


get_ipython().run_cell_magic('time', '', "#this is the trick calculation\n#I match the total of citations received by the citing patent (identified by patent_id)\n#In the next step I sum all citations received by the citing patents\n\ndf=df.merge(back_citation, how='inner', left_on='patent_id', right_on='citation_id')\ndf.rename(columns={'back_citation': 'parent_back_citation'}, inplace=True)")


# In[ ]:


outcome=df.groupby('citation_id').sum()


# In[ ]:


outcome.head()


# In[26]:


# lastly, i merge the number of citations to patent_level_df
# patent_level has the information about the citing patent

outcome=back_citation.merge(df, how='outer', left_on='citation_id', right_index=True)
outcome=back_citation.merge(forw_citation, how='outer', left_on='citation_id', right_on='patent_id')


# In[27]:


# outcome.fillna(0, inplace=True)


# In[28]:


outcome.head()


# In[29]:


outcome.drop(['patent_id'], axis=1, inplace=True)


# In[30]:


# outcome=outcome.loc[:,['citation_id','back_citation','citation_id_y','parent_back_citation']].set_index('citation_id')


# In[31]:


outcome.describe()


# In[32]:


outcome.head()


# In[33]:


get_ipython().run_cell_magic('time', '', 'outcome.to_csv(dst)')

