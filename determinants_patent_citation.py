#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Script to evaluate the determinants of patent citation 
#Renato Kogeyama

# Apr 27, 2020
# Separe most central patents, classify them as disruptive and calculate dvs from extant literature

# Mar 16, 2020
# Introducing centrality measures as dv

# Feb 04, 2020
# to set labels in heatmap keyword:xticklabels
# for ex.
# sns.heatmap(globalWarming_df, xticklabels = np.arange(0,15))
# to be implemented later
# another alternative is to substitute the values in the dataset and convert columns to categories
# to understand the impact, i should run some test
# however i am focusing now in calculate Corredoira's 2015 and Nemet & Johnson 2012

# Feb 03, 2020
# version backed up as _old

# Feb 02, 2020
# the best way to deal with the classification names is to use a dictionary
# this avoid charging memory with the strings
# However, WIPO is organized differently than the other systems
# I'll update the wipo code to uniformize the behavior in this script
# I am creating a code that reflects the first level of classification 

# Feb 01, 2020
# Introduction of categorical graphs: barplot and heatmap
# heatmap is not the real deal, its a simplification
# the real deal would be the correlation table - there is a suggestion based on cramer, 
    # but implementation was not ready
# graphs exported and google docs updated
# next step: update cit_tree to reflect Corredoira's 205 Influence measure
# plot a network graph: https://plot.ly/python/network-graphs/
# reproduce 2012 Nemet and Johnson with other class systems
# correct bias in generality and originality (multiply for N/N-1)

# Jan 21, 2020
# Classifications added
# Code reorganized - much faster now
# Still missing the update of applications to the grant number
# I should provide now descriptive statistics on all variables

# Jan 21, 2020
# The current data does not have Class
# I should go back and get this info - but there are too many scripts now and
#   I should reorganize them before moving forward
# I should also include the patent publication date - to control for the policy changes
# In the citation file, I should change application number for grant when possible 
#   This will improve realiability of all measures related to citation
# Introduce classifications

# Jan 18, 2020
# Variables calculated
# Generality, average delay, forward and backward citations, cumulative citation (cit_tree)
# Still missing originality
# the file with variables that are used in this script should get a name independent from the date


#Miami, December 24th, 2019
# Prof. Rafael Corredoira suggested:
# - Inclusion of a tree of citations
#   To track back the source of citations. This is information is not given by direct count of citations.
# - Consider policy changes in the way patents are cited
#   Policy changes in 2000 changed the time frame of citation, and 2010 partially moved citation to applications
# - Track classification changes 
#   The original classification system in USPTO changed from a technical based to a market based classification system
#   See if there is an impact
# - Consider a text analysis of the claims
#   Classification is based on the claims but it is not clear how many claims are related to each classification category
# - Include moderation effect from classification
#   Citations patterns may change across industries, so some effects may disappear if industry is not accounted for.

# In summary, his ideas help increase structure of the current work


#Syracuse, December 3rd, 2019

#The original script is getting too complex
#There was many tentative scripts to play with data
#Here I am writing a script to show the relevance of variables to patent citation

#11-12-2019
#Introducing normalization

#10-11-2019
#I introduced log backward citation, what corrects for very dispersed results
#but the major problem is that few patents receive citations
#bring back binary output

#10-10-2019
#Added graphics and new distributions

#10-03-2019
#I rewrote the citation data to clean the strings

#09-15-2019
#O naive bayes tem algum problema com distribuicoes desbalanceadas
#o scikit learn tem um modulo que corrige count distributions com muitos zeros, o complementNB
#porem este nao esta disponivel na atual versao disponibilizada no HPC da FIU

#09-10-2019
#o trabalho pede uma abordagem mais sistematica e cuidadosa
#estou agrupando o codigo antigo comentado e vou comecar um novo codigo

#09-27-2019
#I am renaming citation as forward citation and backward citation

#09-17-2018

#Alto uso de memoria - rodar no Amazon AWS 


# In[2]:


import pandas as pd
import numpy as np
import IPython.display as display
import seaborn as sns
          
import itertools

from sklearn import preprocessing
from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn import naive_bayes
from sklearn.metrics import roc_curve, auc
from sklearn.feature_selection import VarianceThreshold

import scipy.stats as ss
import datetime
import matplotlib.pyplot as plt

from math import sqrt

import sys
sys.path.append('/home/rkogeyam/scripts/')
sys.path.append('scripts/')

from determinants_scripts import classes

from plotbar import plotbar
from plot_heat import heatmap


from best_num_attr import best_num_attr
from xattrSelect import xattrSelect
from sampler import sampler
from normalize import normalize
from nbayes import nbayes

import gzip


# In[3]:


latex='data/results.tex'
# dataset='data/dataset.csv'
dataset=gzip.open('data/dataset.csv.gz', 'rt')


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()
sns.set_palette(sns.cubehelix_palette(8))
# pd.options.display.float_format = '{:,.2f}'.format


# In[5]:


dtypes={'id':object,'type':object, 'kind':object, 'num_claims':float, 'cit_received':float, 'cit_made':float,
       'cit_received_delay':float, 'cit_made_delay':float, 'parent_citation':float,
       'originality':float, 'generality':float, 'wipo_sector_id':object, 'ipcr_section':object,
       'ipcr_ipc_class':object, 'ipcr_subclass':object, 'cpc_section_id':object,
       'cpc_subsection_id':object, 'cpc_group_id':object, 'nber_category_id':object,
       'nber_subcategory_id':object, 'uspc_mainclass_id':object, 'uspc_subclass_id':object, 'eigen':float, 'pagerank':float, 'katz':float}


# In[6]:


# # only main classes (exclude uspc)

# usecols=['id', 'type', 'date', 'kind', 'num_claims', 'cit_received', 'cit_made',
#          'cit_received_delay', 'cit_made_delay', 'parent_citation',
#          'originality', 'generality', 'wipo_sector_id', 'ipcr_section', 
#          'cpc_section_id', 'nber_category_id', 'eigen', 'pagerank', 'katz']


# In[7]:


# only WIPO class system, exclude type and kind

usecols=['id', 'date', 'num_claims', 'cit_received', 'cit_made',
         'cit_received_delay', 'cit_made_delay', 'parent_citation',
         'originality', 'generality', 'wipo_sector_id', 'eigen', 'pagerank', 'katz']


# In[8]:


df=pd.read_csv(dataset, dtype=dtypes, usecols=usecols, parse_dates=['date'], index_col='id')

# df.info()


# In[9]:


df['year']=df.date.dt.year

df['decade']=df.date.dt.year//10*10
df['decade'] =df['decade'].apply(lambda x: int(x) if str(x) != 'nan' else np.nan)
decades=list(df.decade.unique())
# decades = [int(x) for x in decades if str(x) != 'nan']


# In[10]:


obj_cols=list(df.select_dtypes(include=[object]).columns.values)
obj_cols


# In[11]:


num_cols=list(df.select_dtypes(include=[np.number]).columns.values)
num_cols


# ## Data Analysis
# 
# ### Descriptive 

# In[12]:


descriptive=df.describe(include=[np.number]).loc[['count','mean','std','min','max']].append(df[num_cols].isnull().sum().rename('isnull'))


# In[13]:


descriptive.apply(lambda x: x.apply('{:,.2f}'.format)).transpose()


# In[14]:


df.describe(include=[np.object])#.append(df[np.object].isnull().sum().rename('isnull')).transpose()


# ### Barplots and Heatmaps

# In[15]:


# # barplot
# # as of 02.03.20, working

# for i in obj_cols:
#     plotbar(i, df, classes)

# # barplot with decades
# for i in obj_cols:
#     plotbar(i, df, classes,decade=True)

# # barplot with decades and inverted axis
# for i in obj_cols:
#     plotbar(i, df, classes,decade=True, decade_x=True)

# # heatmaps all periods
# for double in list(itertools.combinations(obj_cols, 2)):
#     heatmap(df[double[0]], df[double[1]]) 

# # print heatmaps per decade
# for decade in decades:
#     df_dec=df[df['decade']==decade]
#     for double in list(itertools.combinations(obj_cols, 2)):
#         heatmap(df_dec[double[0]], df_dec[double[1]], decade) 


# ### Histograms

# In[16]:


# #histograms
# #could improve cutting off outliers
# for variable in num_cols:
#     ax=df[variable].hist()
#     ax.set_title('Histogram '+ variable.title()+'\n')
#     plt.show()


# ### Trends and Boxplots

# In[17]:


#iterate over numerical variables

num_cols.remove('decade')
num_cols.remove('year')


# In[18]:


# for variable in num_cols:
    
#     title=variable.replace('_', ' ')
#     fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 6))

#     axes[0] = df.groupby('year').mean().plot(y=variable, ax=axes[0])
#     evl_title='Evolution of '+ title +'\n'
#     axes[0].set_title(evl_title)
#     axes[0].set_ylim(bottom=0)
    
#     axes[1] = sns.boxplot(x='decade', y=variable, data=df)

#     box_title='Dispersion of '+ title +'\n'
#     axes[1].set_title(box_title)
#     axes[1].set_ylim(bottom=0)
#     axes[1].set_ylabel("")
    
#     filename='./img/evol_dispersion_'+variable.lower()+'.png'  
#     plt.savefig(filename) 
#     plt.show()


# In[19]:


# the generality data on the 2010's is too concentrated around 0
# to check, I draw this hist to understand what is happening
# it could be an effect of truncation - generality increases with forward citation

# df[df['decade']==2010]['generality'].hist()


# ### Models

# In[20]:


# normalization
df=normalize(df.dropna())


# In[21]:


# #maybe nb fit does not accept nomalized data, so i using data without normalize
# #but in that case, i have to transform the categorical variables

# obj_cols=list(df.select_dtypes(include=[object]).columns.values)

# for col in obj_cols:
#     df[col] = df[col].astype('category')

# df=pd.get_dummies(df, columns=obj_cols, prefix=obj_cols)


# In[22]:


# List of IVs
chosenColumns=df.columns.values.tolist()
len(chosenColumns)


# In[23]:


chosenColumns.remove('cit_received')
len(chosenColumns)


# In[24]:


chosenColumns.remove('parent_citation')
len(chosenColumns)


# In[25]:


chosenColumns.remove('katz')
len(chosenColumns)


# In[26]:


chosenColumns.remove('eigen')
len(chosenColumns)


# In[27]:


chosenColumns.remove('pagerank')
len(chosenColumns)


# In[28]:


chosenColumns.remove('date')
len(chosenColumns)


# ### DV: citation received (forward citation)

# In[29]:


# myX = df.as_matrix(columns=chosenColumns)
# myY = df.as_matrix(columns=['cit_received'])

# xTrain, xTest, yTrain, yTest = train_test_split(myX, myY, train_size=0.7, random_state=3) 
# testSize = yTest.shape[0]
# trainSize = yTrain.shape[0]


# In[30]:


# namesList, errorList = best_num_attr(myX, xTrain, xTest, yTrain, yTest, chosenColumns, regtype='linear')


# ### DV: Parent citation (rename the variable)

# In[31]:


# myX = df.as_matrix(columns=chosenColumns)

# myY = df.as_matrix(columns=['parent_citation'])

# xTrain, xTest, yTrain, yTest = train_test_split(myX, myY, train_size=0.7, random_state=3) 
# testSize = yTest.shape[0]
# trainSize = yTrain.shape[0]
# namesList, errorList = best_num_attr(myX, xTrain, xTest, yTrain, yTest, chosenColumns, regtype='linear')


# ### DV: pagerank (centrality)

# In[32]:


# myX = df.as_matrix(columns=chosenColumns)
# myY = df.as_matrix(columns=['pagerank'])

# xTrain, xTest, yTrain, yTest = train_test_split(myX, myY, train_size=0.7, random_state=3) 
# testSize = yTest.shape[0]
# trainSize = yTrain.shape[0]


# In[33]:


# namesList, errorList = best_num_attr(myX, xTrain, xTest, yTrain, yTest, chosenColumns, regtype='linear')


# ### DV: katz (centrality)

# In[34]:


# myX = df.as_matrix(columns=chosenColumns)
# myY = df.as_matrix(columns=['katz'])

# xTrain, xTest, yTrain, yTest = train_test_split(myX, myY, train_size=0.7, random_state=3) 
# testSize = yTest.shape[0]
# trainSize = yTrain.shape[0]


# In[35]:


# namesList, errorList = best_num_attr(myX, xTrain, xTest, yTrain, yTest, chosenColumns, regtype='linear')


# ### DV: eigen (centrality)

# In[36]:


# myX = df.as_matrix(columns=chosenColumns)
# myY = df.as_matrix(columns=['eigen'])

# xTrain, xTest, yTrain, yTest = train_test_split(myX, myY, train_size=0.7, random_state=3) 
# testSize = yTest.shape[0]
# trainSize = yTrain.shape[0]


# In[37]:


# namesList, errorList = best_num_attr(myX, xTrain, xTest, yTrain, yTest, chosenColumns, regtype='linear')


# In[38]:


# This selector does not work because almost every attribute is p-value significant

# selector = SelectKBest(f_classif, k=4) #initialize 
# selector.fit(myX, myY) #fit
# scores = -np.log10(selector.pvalues_) #transform pvalues (why?)
# scores /= scores.max() #normalize 
# plt.bar(myX - .45, scores, width=.2,
#         label=r'Univariate score ($-Log(p_{value})$)', color='darkorange',
#         edgecolor='black')


# In[39]:


# nbayes(xTrain, yTrain, xTest, yTest)


# In[ ]:


df.dropna()


# In[40]:


#Let's do something else
#Change the DV 

myX = df.as_matrix(columns=chosenColumns)
myY = df.as_matrix(columns=['parent_back_citation'])

xTrain, xTest, yTrain, yTest = train_test_split(myX, myY, train_size=0.7, random_state=3) 


# In[41]:


nbayes(xTrain, yTrain, xTest, yTest)


# In[42]:


# df.parent_back_citation.boxplot()


# In[43]:


#and graphs of back citation in time


# In[44]:


# for i in classifications:
#     rank=df.groupby(i).count().iloc[:,2].sort_values(ascending=False).reset_index().set_index(i)
#     description=df_class[df_class['class']==i].set_index('id')
#     display(rank.join(description))


# In[45]:


# for i in obj_cols:
#     if i.isin(classifications):
#         df.join(df.groupby(i).count().iloc[:,2].sort_values(ascending=False)
# #     display.display(df.pivot_table(values=df.reset_index().id, index=i, columns='decade', aggfunc='count', fill_value=0, margins=False, dropna=True))
#     print(i)
#     display.display(df.groupby(i).count().iloc[:,2].sort_values(ascending=False))


# In[46]:


# def cramers_v(x, y):
#     confusion_matrix = pd.crosstab(x,y)
#     chi2 = ss.chi2_contingency(confusion_matrix)[0]
#     n = confusion_matrix.sum().sum()
#     phi2 = chi2/n
#     r,k = confusion_matrix.shape
#     phi2corr = max(0, phi2-((k-1)*(r-1))/(n-1))
#     rcorr = r-((r-1)**2)/(n-1)
#     kcorr = k-((k-1)**2)/(n-1)
#     return np.sqrt(phi2corr/min((kcorr-1),(rcorr-1)))


# In[47]:


# all variables
# dtypes={'id':object, 'type':object, 'kind':object, 'num_claims':float, 'cit_received':float, 'cit_made':float,
#        'cit_received_delay':float, 'cit_made_delay':float, 'parent_citation':float,
#        'originality':float, 'generality':float, 'wipo_field_id':object, 'ipcr_section':object,
#        'cpc_section_id':object,'nber_category_id':object,'uspc_mainclass_id':object}

