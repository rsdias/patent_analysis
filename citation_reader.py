#!/usr/bin/env python
# coding: utf-8

# In[1]:


#This script opens the citation dataset and perform calculations in patent level
#Renato Kogeyama


#Miami, December 29th, 2019
# The script runs in about 20 min with the full dataset - excellent!
# The main change was in the philosophy of the code - ditching for loops
# This version includes application data calculate time variables 
# The idea is to evaluate changes in patent policy and evaluate time to citation

#Miami, December 27th, 2019
# Due bad performance, I am updating the script to more efficient coding

# This script generates a citation ouput with patent|backward citation|cumulated backward citation | year
# The output generates a citation record by year, considering direct and indirect citation


# In[2]:


import pandas as pd
import re

import sys
sys.path.append('/home/rkogeyam/scripts/')
from sampler import sampler


# In[3]:


get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


fname = r'/home/rkogeyam/PATENT_CITATION/data/uspatentcitation.tsv'
dst = '/home/rkogeyam/PATENT_CITATION/data/cit_tree.csv'


# In[5]:


get_ipython().run_cell_magic('time', '', "df=pd.read_csv(fname)\n\n# sample_size=100\n# df=sampler(fname, sample_size, sep='\\t')")


# In[6]:


df.head()


# In[7]:


df['patent_id']=df['patent_id'].astype(str)
df['citation_id']=df['citation_id'].astype(str)


# In[8]:


df.dtypes


# In[9]:


df.shape


# In[10]:


# some data cleaning

# here I should keep the information for further analysis

# drop rows in which column citation_id has a length smaller than 5
indexNames = df[df['citation_id'].map(len) < 5].index
df.drop(indexNames , inplace=True)

# drop rows for which column patent_id has a length smaller than 5
indexNames = df[df['patent_id'].map(len) < 5].index
df.drop(indexNames , inplace=True)


# In[11]:


df.shape


# In[12]:


get_ipython().run_cell_magic('time', '', '# # Keep this for reference!\n# # As of Dec 31st, 2019, I compared the clean to the raw version of citation and patent ids\n\n# #stripping non-desired characters but keeping the originals for later check - only three changes in citation_id\n\ndf[\'citation_id_raw\']=df[\'citation_id\']\ndf[\'patent_id_raw\']=df[\'patent_id\']\n\ncleaning_patent=lambda x:re.sub(\'([^a-zA-Z0-9]+)\', "", x)\ndf[\'citation_id\']=df[\'citation_id\'].apply(cleaning_patent)\ndf[\'patent_id\']=df[\'patent_id\'].apply(cleaning_patent)\n\n# #stripping trailing white spaces - no changes\n# df[\'patent_id\'] = df[\'patent_id\'].str.strip()\n# df[\'citation_id\'] = df[\'citation_id\'].str.strip()\n\n# #this is taking a lot of time, evaluate alternatives\n\nprint(df[df[\'citation_id\'].map(len) > 8])')


# In[13]:


print(df[df['patent_id'].map(len) > 8])


# In[14]:


print(df[df['patent_id']!=df['patent_id']])


# In[15]:


get_ipython().run_cell_magic('time', '', "#Non-conforming dates\n#this corrects days or months registered as 00\ndf.date.replace({'-00':'-01'}, regex=True, inplace=True)\n\n#replacing day or month would not affect the output\n#replacing the year could be more problematic\n\n#Ditch month and day altogether, since it is not a reliable source of information")


# In[16]:


get_ipython().run_cell_magic('time', '', "#attention to date format - original data is year-month-day\ndf['date']=pd.to_datetime(df.date,format='%Y-%m-%d', errors='coerce') ")


# In[17]:


get_ipython().run_cell_magic('time', '', "#cited patents registers total citations received \n\ncited_patents=df.groupby(['citation_id']).count().iloc[:, 1].reset_index() #Series, patent-level\n# cited_patents.dropna(0, inplace=True) #Series, '0' implies that rows are dropped\n\n#I should check this, because later I make citation back as index for merging purposes\n# cited_patents=cited_patents.reset_index() #Dataframe")


# In[18]:


cited_patents.rename(columns={'patent_id': 'back_citation'}, inplace=True)


# In[19]:


df.head()


# In[20]:


#forward citation
forward_citation=df.groupby(['patent_id']).count().iloc[:, 1].reset_index()
forward_citation.rename(columns={'citation_id': 'forw_citation'}, inplace=True)


# In[21]:


forward_citation.head()


# In[22]:


get_ipython().run_cell_magic('time', '', "#this is the trick code\n#I match the total of citations received by the citing patent (identified by patent_id)\n#Then I sum all citations received by the citing patents\n\ndf=df.merge(cited_patents, how='inner', left_on='patent_id', right_on='citation_id')\ndf.rename(columns={'back_citation': 'parent_back_citation'}, inplace=True)")


# In[23]:


get_ipython().run_cell_magic('time', '', '#merging generates new NaNs\n#NaN in citations means no citation\ndf.fillna(0, inplace=True)')


# In[24]:


get_ipython().run_cell_magic('time', '', "#now I collapse df to become a patent level dataframe\n#citation_id_x is the original cited patent\npatent_level_df=df.groupby('citation_id_x').sum()")


# In[25]:


# now i merge the number of citations to patent_level_df
# patent_level has the information about the citing patent

outcome=cited_patents.merge(patent_level_df, how='outer', left_on='citation_id', right_index=True)


# In[26]:


outcome.head()


# In[27]:


outcome=outcome.merge(forward_citation, how='outer', left_on='citation_id', right_on='patent_id')


# In[28]:


outcome.head()


# In[29]:


outcome.fillna(0, inplace=True)


# In[30]:


outcome.head()


# In[31]:


outcome.drop(['sequence', 'patent_id'], axis=1, inplace=True)


# In[ ]:


outcome.set_index('citation_id')


# In[32]:


outcome.describe()


# In[33]:


get_ipython().run_cell_magic('time', '', 'outcome.to_csv(dst)')


# In[34]:


# I should introduce a test to see if the script is calculating correctly
# I should search for the information of one specfic patent and compare with the output generated by the script

