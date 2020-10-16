#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Script to evaluate the determinants of patent citation 
#Renato Kogeyama

# August 19, 2020
# Updated all files to latest data available in PatentsView (Jun/2020)
# Excluded self citations from the dataset

# July 13, 2020
# I am changing the script to test Nemet and Johnson 2012, but with centrality measures as DV

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
from sklearn.linear_model import LinearRegression

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
import statsmodels.api as sm
import statsmodels.formula.api as smf

import os
import math
from pandas.core.common import is_numeric_dtype


# In[3]:


#function to write results to a latex file 
def export_table(content, name):
    basename='output/'+ name
    i=1
    while os.path.exists(basename+"_"+"{:03d}".format(i)+'.out'):
        i += 1
    with open(basename+"_"+"{:03d}".format(i)+'.out','w') as fh:
        for element in content:
            fh.write( element )
 


# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
sns.set()
sns.set_palette(sns.cubehelix_palette(8))
# pd.options.display.float_format = '{:,.2f}'.format


# In[5]:


latex='data/results.tex'
# dataset='data/dataset.csv'
dataset=gzip.open('data/dataset.csv.gz', 'rt')


# In[6]:


dtypes={'id':object,'title':object, 'num_claims':float, 'cit_received':float, 'cit_made':float,
       'cit_received_delay':float, 'cit_made_delay':float, 'parent_citation':float,
       'originality':float, 'generality':float, 'wipo_sector_id':object,'wipo_far_ext':float, 'wipo_ext':float,  'pagerank':float}


# In[7]:


# only main classes (exclude uspc)

usecols=['id', 'title', 'date', 'num_claims', 'cit_received', 'cit_made',
         'cit_received_delay', 'cit_made_delay',
         'originality', 'generality', 'wipo_sector_id', 'wipo_far_ext', 'wipo_ext', 'pagerank']


# In[8]:


# only WIPO class system, exclude type and kind

# usecols=['id', 'date', 'num_claims', 'cit_received', 'cit_made',
#         'cit_received_delay', 'cit_made_delay', 'parent_citation',
#         'originality', 'generality', 'wipo_sector_id', 'eigen', 'pagerank', 'katz']


# In[9]:


wipo_sector_title={
    '0':"Chemistry",
    '1':"Electrical Eng",
    '2':"Instruments",
    '3':"Mechanical Eng",
    '4':"Other fields",
    '5':"Plant"
    }


# In[10]:


df=pd.read_csv(dataset, usecols=usecols, dtype=dtypes, parse_dates=['date'], index_col='id')

df.info()


# In[11]:


df[(df['cit_received']==0) & (df['pagerank']>4.420830e-08)] #check if a patent without citations has centrality different from 0


# In[12]:


df=df[df['cit_received']>0] #patents without citations introduce noise
df.info()


# In[13]:


df['year']=df.date.dt.year
df['decade']=df.date.dt.year//10*10 #x//y returns the integer part of the division, so this is a shortcut
df['decade'] =df['decade'].apply(lambda x: '{0:.0f}'.format(x) if str(x) != 'nan' else np.nan)

decades=list(df.decade.unique())
decades = [int(x) for x in decades if str(x) != 'nan']


# In[14]:


obj_cols=list(df.select_dtypes(include=[object]).columns.values)
obj_cols


# In[15]:


num_cols=list(df.select_dtypes(include=[np.number]).columns.values)
num_cols


# ## Data Analysis
# 
# ### Descriptive 

# In[16]:


descriptive=df.describe(include=[np.number]).loc[['count','mean','std','min','max']].append(df[num_cols].isnull().sum().rename('isnull')).transpose()


# In[17]:


descriptive.columns


# In[18]:


descriptive['count']=descriptive['count'].apply(lambda x: (x/(1e6)))


# In[19]:


descriptive['isnull']=descriptive['isnull'].apply(lambda x: (x/(1e6)))


# In[20]:


# descriptive.rename(columns={'count': 'count (MM)', 'isnull': 'isnull (MM)'}, inplace=True)


# In[21]:


# descriptive.reset_index(inplace=True)
descriptive


# In[22]:


for column in descriptive.columns.values:
    try:
        descriptive[column]=descriptive[column].apply(lambda x: '{0:3.2f}'.format(x) if str(x) != 'nan' else np.nan)
    except:
        print('problem in column ' + column)
    descriptive.rename(columns={column: "{"+column+"}"}, inplace=True) 
    #curly braces will avoid the error " siunitx error: “invalid-number” Invalid numerical input 'e'"


# In[23]:


output=[]
output.append(descriptive.to_latex())
output.append("\\newpage\n")


# In[24]:


# df.describe(include=[np.object])#.append(df[np.object].isnull().sum().rename('isnull')).transpose()


# In[25]:


df.nlargest(10, 'pagerank')[['date', 'title','pagerank','num_claims', 'cit_received', 'wipo_sector_id']]


# ### Barplots and Heatmaps

# In[26]:


# barplot
# as of 02.03.20, working

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

# In[27]:


#histograms
#could improve cutting off outliers
#for variable in num_cols:
#    ax=df[variable].hist()
#    ax.set_title('Histogram '+ variable.title()+'\n')
#    plt.show()


# ### Trends and Boxplots

# In[28]:


#iterate over numerical variables

# num_cols.remove('decade')
# num_cols.remove('year')


# In[29]:


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


# In[30]:


# the generality data on the 2010's is too concentrated around 0
# to check, I draw this hist to understand what is happening
# it could be an effect of truncation - generality increases with forward citation

# df[df['decade']==2010]['generality'].hist()


# ### Models

# In[31]:


# normalization
df=normalize(df.dropna())


# In[32]:


df.info()


# In[33]:


df.head()


# In[34]:


# #maybe nb fit does not accept nomalized data, so i using data without normalize
# #but in that case, i have to transform the categorical variables

# obj_cols=list(df.select_dtypes(include=[object]).columns.values)

# for col in obj_cols:
#     df[col] = df[col].astype('category')

# df=pd.get_dummies(df, columns=obj_cols, prefix=obj_cols)


# In[35]:


# List of IVs
chosenColumns=df.columns.values.tolist()
len(chosenColumns)


# In[36]:


chosenColumns.remove('pagerank') #dv
chosenColumns.remove('date') #similar to year
chosenColumns.remove('wipo_sector_id') #iterate over patent class
chosenColumns.remove('decade')
chosenColumns.remove('title')

len(chosenColumns)


# In[37]:


wipo_sectors=df.wipo_sector_id.unique() #list of wipo sectors


# In[38]:


max_pagerank=df['pagerank'].max() #variable used in the transformation
max_pagerank


# In[39]:


#transform DV first by inverting (max_pagerank-1) and then applying log (see Andy Field)
df['t_pagerank']=df['pagerank'].apply(lambda x: math.log(max_pagerank+1-x))


# In[40]:


num_cols=list(df.select_dtypes(include=[np.number]).columns.values)
# num_cols


# In[41]:


# # histograms
# for variable in num_cols:
#     ax=df[df[variable]>df[variable].min()][variable].hist()
#     ax.set_title('Histogram '+ variable.title()+'\n')
#     plt.show()


# In[42]:


formula='t_pagerank ~ num_claims + cit_received + cit_made + cit_received_delay + cit_made_delay + originality + generality + wipo_far_ext + wipo_ext + year'

for wipo_sector in wipo_sectors:
#     print(wipo_sector_title[wipo_sector])
#     print(df[df.wipo_sector_id==wipo_sector].head())
#     print("\n")
    
#     myX = df[df.wipo_sector_id==wipo_sector].as_matrix(columns=chosenColumns)
#     myY = df[df.wipo_sector_id==wipo_sector].as_matrix(columns=['t-pagerank'])

    data=df[df.wipo_sector_id==wipo_sector]
#     x = sm.add_constant(myX)
#     model = sm.OLS(myY, x)
    model = smf.ols(formula, data=data) #smf permite a construcao de formulas estilo R
                                        #o uso de smf permite que os nomes das variaveis aparecam 
                                        #automaticamente no plot_partregress_grid
    results = model.fit()    
    output.append("WIPO: " + wipo_sector_title[wipo_sector])
    output.append(results.summary(title="OLS of WIPO: " + wipo_sector_title[wipo_sector]).as_latex())
    output.append("\\newpage\n")
#     for element in chosenColumns:
#         fig = sm.graphics.plot_regress_exog(results, element)
#         fig.tight_layout(pad=1.0)

#     print('\n')
#     print(wipo_sector_title[wipo_sector].title())
#     print('\n')
#     fig = plt.figure(figsize=(12, 20))
#     fig = sm.graphics.plot_partregress_grid(results, fig=fig)
#     fig.tight_layout(pad=1.0)
#     plt.savefig('img/partial_reg_plot'+wipo_sector_title[wipo_sector].replace(" ", "_")+'.png')
#     results.summary()


# In[43]:


export_table(output, "output_by_wipo")


# In[44]:


#and graphs of back citation in time


# In[45]:


# for i in classifications:
#     rank=df.groupby(i).count().iloc[:,2].sort_values(ascending=False).reset_index().set_index(i)
#     description=df_class[df_class['class']==i].set_index('id')
#     display(rank.join(description))


# In[46]:


# for i in obj_cols:
#     if i.isin(classifications):
#         df.join(df.groupby(i).count().iloc[:,2].sort_values(ascending=False)
# #     display.display(df.pivot_table(values=df.reset_index().id, index=i, columns='decade', aggfunc='count', fill_value=0, margins=False, dropna=True))
#     print(i)
#     display.display(df.groupby(i).count().iloc[:,2].sort_values(ascending=False))


# In[47]:


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


# In[48]:


# all variables
# dtypes={'id':object, 'type':object, 'kind':object, 'num_claims':float, 'cit_received':float, 'cit_made':float,
#        'cit_received_delay':float, 'cit_made_delay':float, 'parent_citation':float,
#        'originality':float, 'generality':float, 'wipo_field_id':object, 'ipcr_section':object,
#        'cpc_section_id':object,'nber_category_id':object,'uspc_mainclass_id':object}

