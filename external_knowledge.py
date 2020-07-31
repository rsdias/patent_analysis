
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
plt.switch_backend('agg')
import datetime
import gzip 
import seaborn as sns

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
        #f.write(str(today))
        #f.write(str(today))
        f.write("\n")
        f.writelines((str(i) for i in s))
        f.write("\n")

    return None

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

    #print(results.summary(yname=dv, xname=replace_underline(chosenColumns), title=title))
    export_results(results.summary(yname=dv, xname=replace_underline(chosenColumns), title=title).as_latex(), label=title)
    return results    

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

def histog(variables):
    # #histograms
    #could improve cutting off outliers
    #plt.figure(figsize=(10,7))
    fig, axs=plt.subplots(len(variables))
    fig.suptitle('DVs Histograms')
    for i, variable in enumerate(variables):
        axs[i].hist(df[variable])
        axs[i].set_title(variable.title())
    plt.legend();
    plt.savefig('histograms.png')

#load variables
usecols=['id', 'date', 'eigen','cit_received','cit_received_delay','parent_citation', 'pagerank', 'katz', 'originality', 'generality', 'eigen', 'num_claims', 'wipo_sector_id']
#usecols=['uuid', 'wipo_sector_ext', 'wipo_field_ext', 'ipcr_section_ext', 'ipcr_ipc_class_ext', 'cpc_section_ext', 'cpc_subsection_ext', 'nber_category_ext', 'nber_subcategory_ext']

#to define types decreases reading time and errors
dtypes={'id':object,'cit_received':float, 'cit_received_delay':float, 'parent_citation':float, 'eigen':float, 'pagerank':float, 'katz':float, 'originality':float, 'generality':float, 'eigen':float, 'wipo_sector_id':object, 'num_claims':float}

file='data/dataset.csv.gz'
unzipped=gzip.open(file, 'r')
df=pd.read_csv(unzipped, usecols=usecols, dtype=dtypes, parse_dates=['date'], index_col='id')


#replace string nan with np.nan
#data description
obj_cols=list(df.select_dtypes(include=[object]).columns.values)
num_cols=list(df.select_dtypes(include=[np.number]).columns.values)
descriptive=df.describe(include=[np.number]).loc[['count','mean','std','min','max']].append(df[num_cols].isnull().sum().rename('isnull'))
descriptive.apply(lambda x: x.apply('{:,.2f}'.format)).transpose()
#df.describe(include=[np.object])#.append(df[np.object].isnull().sum().rename('isnull')).transpose()
df=df[df.cit_received>0]
df=normalize(df.dropna())
gen_decade(df)

#basic data
append_output(df)

#separate dv from iv
ivs=['cit_received','cit_received_delay','originality', 'generality', 'num_claims', 'parent_citation', 'decade']
dvs=['katz', 'eigen', 'pagerank']

sns.set_style("white")
histog(dvs)

"""
#test multiple dvs
for dv in dvs:
    try:
        model_results=run_ols(df, ivs, dv)
    except:
        print('Error in ' + dv)
        continue

samples=[0.1,0.01, 0.001]

#test samples
for sample in samples:
    for dv in dvs:
        try:
            run_ols(df.sample(frac=sample), ivs, dv, sample=str(sample*100)+"\%")
        except:
            print('Error in ' + dv) 
            continue

            
classifications=pd.unique(df.wipo_sector_id)
decades=pd.unique(df.decade)
for decade in decades:
    for dv in dvs:
        model=run_ols(df[df.decade == decade], ivs, dv, sample="Decade " + str(decade) + " dv: " + dv)
        fig = plt.figure(figsize=(12,8))
        fig = sm.graphics.plot_partregress_grid(model, fig=fig)
        plt.savefig("img/partial_plot_"+str(decade)+"_dv_"+dv+".png")
            
"""

            

#test by decade
decades=pd.unique(df.decade)
classifications=pd.unique(df.wipo_sector_id)
dv='pagerank'
for classification in classifications:
    for decade in decades:
        model=run_ols(df[(df.decade == decade) & (df.wipo_sector_id == classification)], ivs, dv, sample="Decade: " + str(decade) + " Classification: " + classification)
        fig = plt.figure(figsize=(12,8))
        fig = sm.graphics.plot_partregress_grid(model, fig=fig)
        plt.savefig("img/partial_plot_"+ str(decade) + "_" + classification +"_pagerank.png")
           
"""
#test by classification
classifications=pd.unique(df.wipo_sector_id)
for classification in classifications:
    for sample in samples:
        model=run_ols(df[df.wipo_sector_id == classification].sample(frac=sample), ivs, dv, sample="WIPO Class " + classification + " Sample: "+ str(sample*100)+"%")
        fig = plt.figure(figsize=(12,8))
        fig = sm.graphics.plot_partregress_grid(model, fig=fig)
        plt.savefig("img/partial_plot_"+classification+"_sample_"+str(sample).replace(".","_")+".png")
"""
"""
I tried to put variable names in the axes but its getting too complicated.
it seems that plot_partregress_grid puts names in the axes when the model fit is run by formula
this way of doing it generated some kind of problem - i'm not sure that sm.OLS understands the concatenated string. 


for dv in dvs:
    model = dv + " ~ "+ " + ".join(ivs)
    print(model)
    influence_model=sm.OLS(model, data=df).fit() 
    fig = plt.figure(figsize=(12,8))
    fig = sm.graphics.plot_partregress_grid(model, fig=fig)
    plt.savefig("partial_plot_"+dv+".png")
"""
