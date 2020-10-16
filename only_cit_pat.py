#!/usr/bin/env python
# coding: utf-8

# In[75]:


import pandas as pd
import numpy as np
import itertools
# import seaborn as sns
# import networkx as nx
# import matplotlib.pyplot as plt
import csv
# from graphviz import Digraph
# import igraph


from determinants_scripts import classes, dtypes

src='data/cleanuspatentcitation.csv'
# names=['index', 'id', 'cit_received']
# usecols=['id', 'cit_received']
# dtype={'main_group':'int64', 'subgroup':'int64'}
# cols=['patent_id','citation_id', 'cit_delay']
usecols=['uuid','patent_id', 'citation_id']

df = pd.read_csv(src, chunksize=1000,usecols=[2,3], skiprows=[0], index_col=0)

# df = pd.read_csv(src, chunksize=1000,  parse_dates=['date'], error_bad_lines=False)
# df = pd.read_csv(src, usecols=usecols, names=names, chunksize=1000, dtype=dtype, index_col='id')
# df=pd.read_csv(src, usecols=[0, 1, 3], dtype={0:object}, index_col=0, chunksize=1000)

get_ipython().run_line_magic('matplotlib', 'inline')


# In[76]:


dst='data/only_cit_pat2.csv'

for i in df:
    i.to_csv(dst, mode='a', index=False)


# In[ ]:




