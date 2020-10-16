#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
# import random
# from collections import Counter
import matplotlib.pyplot as plt
# import json

# import csv


# In[3]:


# class ItemLoader(ItemLoader):

#     default_output_processor = MapCompose(unicode.strip)


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


fname = r'/home/rkogeyam/PATENT_CITATION/uspatentcitation.tsv'
# fname = r'/home/rkogeyam/PATENT_CITATION/cit_sample.csv' #for running a sample

dst = '/home/rkogeyam/PATENT_CITATION/fwd_back_cit.csv'


# In[6]:


get_ipython().run_cell_magic('time', '', "df = pd.read_csv(fname, sep='\\t', lineterminator='\\n', na_values='-')\n#df = pd.read_csv(fname, lineterminator='\\n', na_values='-')")


# In[7]:


# asg = pd.read_csv(r'/home/rkogeyam/PATENT_CITATION/uspatentcitation.tsv', sep='\t', lineterminator='\n', na_values='-')


# In[8]:


get_ipython().run_cell_magic('time', '', 'df=df.iloc[:,1:]')


# In[9]:


get_ipython().run_cell_magic('time', '', 'df')


# In[10]:


get_ipython().run_cell_magic('time', '', 'df.describe()')


# In[11]:


df.head()


# In[12]:


#stripping white spaces
# df['patent_id'] = df1['patent_id'].str.strip()
# df['citation_id'] = df1['citation_id'].str.strip()


# In[13]:


# df1=df


# In[14]:


get_ipython().run_cell_magic('time', '', 'df.shape')


# In[15]:


get_ipython().run_cell_magic('time', '', "#stripping non desired characters\ndf['patent_id'] = df['patent_id'].str.extract('([a-zA-Z0-9]+)', expand=False)\ndf['citation_id'] = df['citation_id'].str.extract('([a-zA-Z0-9]+)', expand=False)")


# In[16]:


get_ipython().run_cell_magic('time', '', "df['patent_id'] = df['patent_id'].str.strip()\ndf['citation_id'] = df['citation_id'].str.strip()\n# [a-fA-F0-9]")


# In[17]:


# ne = (df != df1).any(1)
# ne_stacked = (df != df1).stack()
# changed = ne_stacked[ne_stacked]
# changed.index.names = ['id', 'col']
# changed


# In[18]:


get_ipython().run_cell_magic('time', '', 'df.head()')


# In[19]:


get_ipython().run_cell_magic('time', '', 'df.tail()')


# In[20]:


# df.sort_values('patent_id').head()


# In[21]:


# df1.tail()


# In[22]:


get_ipython().run_cell_magic('time', '', "# forward_citation=df.groupby(['patent_id']).count().reset_index()\nforward_citation=df.groupby(['patent_id']).count().iloc[:, 1]")


# In[23]:


# forward_citation


# In[24]:


get_ipython().run_cell_magic('time', '', 'forward_citation=forward_citation.fillna(0)')


# In[25]:


get_ipython().run_cell_magic('time', '', 'forward_citation.describe()')


# In[26]:


get_ipython().run_cell_magic('time', '', "    backward_citation=df.groupby(['citation_id']).count().iloc[:, 1]")


# In[27]:


#to find weird ids - backward citation only

#bigger citation ids are generally application numbers
# backward_citation_big=df[df['citation_id'].str.len() > 8 ]

#many small citation id are citation of very old patents
# backward_citation_small=df[df['citation_id'].str.len() < 6 ]


# In[28]:


# backward_citation_big


# In[29]:


# backward_citation_small


# In[30]:


#41579 small and 136935 large citation_ids (total=178514 citations) from 91453297 citations represent 0.2% of citations
#for this reason, I am ignoring these errors for now


# In[31]:


#%%time
#result = pd.concat([forward_citation, backward_citation], axis=1, join='outer')

#result.columns=['forward_citation', 'backward_citation']

#result=result.fillna(0)


# In[32]:


#result.shape


# In[33]:


# result.head()


# In[34]:


# result.describe()


# In[35]:


# plt.figure()
# result.hist()


# In[36]:


# result.boxplot()


# In[37]:


# result.to_csv(dst) #the file is frozen as of Oct 10 2019


# In[38]:


# Some additional analysis


# In[39]:


get_ipython().run_cell_magic('time', '', "pt_df = pd.read_csv('patent.csv', sep='\\t', na_values='-', usecols=[0,4], error_bad_lines=False, index_col=0, dtype={0: object})\n# pt_df.columns=['patent_date']")


# In[40]:


# pt_df


# In[41]:


get_ipython().run_cell_magic('time', '', 'df=df.rename(columns = {\'date\':\'citation_date\'})\ndf[\'citation_date\']=pd.to_datetime(df[\'citation_date\'], format="%Y-%m-%d", errors=\'coerce\') #conversao de string para data\n# df[\'cit_year\']=df[\'citation_date\'].dt.year\n# df[\'cit_month\']=df[\'citation_date\'].dt.month\n# df[\'cit_day\']=df[\'citation_date\'].dt.day')


# In[42]:


get_ipython().run_cell_magic('time', '', "# df is the citation dataset\n# pt_df is the patent dataset\ndf=pd.merge(df, pt_df, how='left', left_on='patent_id', right_index=True)")


# In[43]:


get_ipython().run_cell_magic('time', '', 'df.shape')


# In[44]:


get_ipython().run_cell_magic('time', '', 'df=df.rename(columns = {\'date\':\'patent_date\'})\ndf[\'patent_date\']=pd.to_datetime(df[\'patent_date\'], format="%Y-%m-%d", errors=\'coerce\') #conversao de string para data\n# df[\'patt_year\']=df[\'patent_date\'].dt.year\n# df[\'pat_month\']=df[\'patent_date\'].dt.month\n# df[\'pat_day\']=df[\'patent_date\'].dt.day')


# In[45]:


get_ipython().run_cell_magic('time', '', 'df=df.dropna()')


# In[46]:


get_ipython().run_cell_magic('time', '', "df.sort_values('citation_id').head()")


# In[47]:


get_ipython().run_cell_magic('time', '', "df['cit_delay']=df['patent_date'].sub(df['citation_date'], axis=0)")


# In[48]:


get_ipython().run_cell_magic('time', '', "df['cit_delay']=pd.to_timedelta(df['cit_delay'])")


# In[49]:


get_ipython().run_cell_magic('time', '', 'df.describe()')


# In[50]:


get_ipython().run_cell_magic('time', '', "df['cit_delay']=df['cit_delay'].dt.days/360\n# ")


# In[51]:


get_ipython().run_cell_magic('time', '', 'df.cit_delay.describe()')


# In[52]:


get_ipython().run_cell_magic('time', '', "avg_delay=df.groupby('citation_id').cit_delay.agg(['mean', 'count'])\n# std=df.groupby('citation_id').std()")


# In[53]:


get_ipython().run_cell_magic('time', '', "avg_delay.sort_values('count')\n# avg_delay")


# In[54]:


get_ipython().run_cell_magic('time', '', 'df.head()')


# In[55]:


get_ipython().run_cell_magic('time', '', "result = pd.concat([avg_delay, forward_citation], axis=1, join='outer')")


# In[56]:


get_ipython().run_cell_magic('time', '', 'result.shape')


# In[57]:


get_ipython().run_cell_magic('time', '', "result.columns=['avg_delay', 'backward_citation', 'forward_citation']")


# In[58]:


get_ipython().run_cell_magic('time', '', 'result')


# In[59]:


#result.dropna()


# In[60]:


#result.fillna(0)


# In[61]:


get_ipython().run_cell_magic('time', '', 'result.to_csv(dst)')

