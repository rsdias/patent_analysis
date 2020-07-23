
# coding: utf-8

# Jun 8, 2020
# 
# So far, I collected and calculated variables on citation- and patent-levels. The first contribution is to use centrality measures such as pagerank, katz and eigen, as proxies to relevance, impact and influence. Also, I test various effects including the relevance of industries. So far, to the best of our knowledge, scholarly production  focused on studies of innovation in specific industries. Our approach allows us to understand broader patterns of innovation.
# 
# Here, I am testing the hypothesis of the relationship between originality and impact, following 2012 Nemet and Johnson.
# 
# Originality is measured as the number (or proportion) of citation from patents outside their own domain of knowledge.
# 

# In[ ]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import gzip 
#import seaborn as sns

import sys
sys.path.append('/home/rkogeyam/scripts/')
sys.path.append('scripts/')
from datetime import datetime
import io
import statsmodels.api as sm

from normalize import normalize

def append_output(df):

    buffer = io.StringIO()

    s=[]
    try:
        df.info(buf=buffer)
        s.append(buffer.getvalue())
    except:
        s.append("no info\n")
    try:
        s.append(df.describe())
    except:
        s.append("no description\n")
    try:
        s.append(df.head())
    except:
        s.append("no head\n")

    with open(str(__file__.replace(".py","")+'_output.txt'), 'a') as f:
        #today = date.today()
        #f.write("\n")
        #f.write()
        f.write("\n")
        f.writelines((str(i) for i in s))
        f.write("\n")

    return None

def test_set_index(df):
    try:
        df.set_index('uuid', inplace=True)
    except:
        print('error set index')

def export_results(s, label):
    with open(str(__file__.replace(".py","")+'_results.tex'), 'a') as f:
        f.write("\n")
        f.write(label)
        f.write("\n")
        f.writelines((str(i) for i in s))
        f.write("\n")
        f.write("\\break")

def run_ols(df, chosenColumns, dv, sample=None):
    myX = df.as_matrix(columns=chosenColumns)
    myY = df.as_matrix(columns=[dv])
    x = sm.add_constant(myX)
    model = sm.OLS(myY, x)
    results = model.fit()
    if sample:
        title="OLS on " + dv + " sample: " + sample
    else:
        title="OLS on " + dv

    print(results.summary(yname=dv, xname=replace_underline(chosenColumns), title=title))
    export_results(results.summary(yname=dv, xname=replace_underline(chosenColumns), title=title).as_latex(), label=title)

def replace_underline(list):
    output=[]
    for element in list:
        output.append(element.replace("_", " "))
    return output   

def gen_decade(df):
    #creating year and decade
    df['year']=df.date.dt.year
    df['decade']=df.date.dt.year//10*10
    #replace string nan with np.nan
    df['decade'] =df['decade'].apply(lambda x: int(x) if str(x) != 'nan' else np.nan)
    return df

#load variables
usecols=['id', 'date', 'eigen','cit_received','cit_received_delay','parent_citation', 'pagerank', 'katz', 'originality', 'generality', 'eigen', 'num_claims']
#usecols=['uuid', 'wipo_sector_ext', 'wipo_field_ext', 'ipcr_section_ext', 'ipcr_ipc_class_ext', 'cpc_section_ext', 'cpc_subsection_ext', 'nber_category_ext', 'nber_subcategory_ext']

#define types decreases reading time and errors
dtypes={'id':object,'cit_received':float, 'cit_received_delay':float, 'parent_citation':float, 'eigen':float, 'pagerank':float, 'katz':float, 'originality':float, 'generality':float, 'eigen':float, 'wipo_sector_id':object, 'num_claims':float}

file='data/dataset.csv.gz'
unzipped=gzip.open(file, 'r')

df=pd.read_csv(unzipped, usecols=usecols, dtype=dtypes, parse_dates=['date'], index_col='id')
#new_list basic reading test
append_output(df)


#data description
obj_cols=list(df.select_dtypes(include=[object]).columns.values)
num_cols=list(df.select_dtypes(include=[np.number]).columns.values)
descriptive=df.describe(include=[np.number]).loc[['count','mean','std','min','max']].append(df[num_cols].isnull().sum().rename('isnull'))
descriptive.apply(lambda x: x.apply('{:,.2f}'.format)).transpose()
#df.describe(include=[np.object])#.append(df[np.object].isnull().sum().rename('isnull')).transpose()

df=normalize(df.dropna())

#separate dv from iv
ivs=['cit_received','cit_received_delay','originality', 'generality', 'num_claims', 'parent_citation']
dvs=['katz', 'eigen', 'pagerank']

#test multiple dvs
for dv in dvs:
    try:
        run_ols(df, ivs, dv)
    except:
        print('Error in ' + dv.columns.values) 
        continue
samples=[0.1,0.01, 0.001]

#test samples
for sample in samples:
    for dv in dvs:
        try:
            run_ols(df.sample(frac=sample), ivs, dv, sample="{:.0%}".format(sample))
        except:
            print('Error in ' + dv.columns.values) 
            continue
"""
#test sample 1%
for dv in dvs:
    try:
        run_ols(df.sample(frac=0.01), ivs, dv, sample="1\%")
    except:
        print('Error in ' + dv.columns.values) 
        continue
#test sample 0.1%
for dv in dvs:
    try:
        run_ols(df.sample(frac=0.001), ivs, dv, sample="0.1\%")
    except:
        print('Error in ' + dv.columns.values) 
        continue
"""

# usecols=['uuid', 'wipo_sector_ext', 'wipo_field_ext'] #choice for wipo is arbitrary
#file='data/centrality.csv.gz'
#unzipped=gzip.open(file, 'r')

#df2=pd.read_csv(unzipped, dtype=object)
#df2=pd.read_csv(unzipped, usecols=usecols, dtype=object)
#test_set_index(df2)
#append_output(df2)

#an outer join would lead to the same result as a left
#since there should not have a classification without a citation
#df=df.join(df2, how='outer', lsuffix='_left', rsuffix='_right')
#append_output(df)

# In[ ]:
#df.info()

# In[ ]:
#df.describe()

# In[ ]:
#df.head()

# In[ ]:





