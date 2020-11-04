#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Script to clean patent.tsv

#Aug 18st, 2020
#convert to gzip input and output

# Jan 20th, 2020
# There are citation_ids larger than 7 characters and smaller than 4
# Larger are usually applications, smallers tend to be errors
# I am keeping than so calculations on forward citations are accurate
# When matching by citation_id, it must be previously filtered

# as of Jan 9th, 2020, there are entries to be evaluated
# for now, error_bad_lines=False skips those entries


import pandas as pd
import numpy as np
import re
import gzip
import datetime

import dask.dataframe as dd
from dask.delayed import delayed
from fastparquet import ParquetFile

# patent.csv
# id:       patent this record corresponds to 
# type:     category of patent. Usually "Design", "reissue", etc.
# number:   patent number
# country:  country in which patent was granted (always US)
# date:     date when patent was granted
# abstract: abstract text of patent
# title:    title of patent
# kind:     WIPO document kind codes (http://www.uspto.gov/learning-and-resources/support-centers/electronic-business-center/kind-codes-included-uspto-patent)
# num_claims:number of claims
# filename: name of the raw data file where patent information is parsed from

def clean_patent(df):
    
    df.date.replace({'-00':'-01'}, regex=True, inplace=True)
    df['num_claims']=pd.to_numeric(df['num_claims'], errors='coerce')
    df.dropna(inplace=True)
    cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
    df['id']=df['id'].apply(cleaning_patent)

    return df
    
def date_within_boundaries(df):
    # Avoid TimeStamp limitations:
    # https://stackoverflow.com/questions/50265288/how-to-work-around-python-pandas-dataframes-out-of-bounds-nanosecond-timestamp
    df['date']=df['date'].str[:4].astype(int)
    #pd.Timestamp.min: Timestamp('1677-09-21 00:12:43.145225')
    df['date']=df['date'].apply(lambda x: x if x > 1677 else np.nan)
    #pd.Timestamp.max: Timestamp('2262-04-11 23:47:16.854775807')
    df['date']=df['date'].apply(lambda x: x if x < 2021 else np.nan)
    return df


src= 'parquet/patent_000.parquet.gz'
dst= 'data/cleanpatent.parquet.gz'
df = dd.read_parquet(src)
report_dst='clean_patent.tex'

report=[] #file to export report

#df.info()  
#df.dtypes
# Keep this for reference!\n
# As of Dec 31st, 2019, I compared the clean to the raw version of citation and patent ids
# stripping non-desired characters but keeping the originals for later check - only three changes in citation_id
# df[\id\]=df[\id\].astype(object)

df=delayed(clean_patent)(df)
df=delayed(date_within_boundaries)(df)
df=df.compute(num_workers=8)

report.append("Dataframe Description \n")
report.append(df.describe())

report.append("Dataframe info with NAN \n")
report.append(df.info())
df.dropna(inplace=True)
report.append("Dataframe info without NAN \n")
report.append(df.info())
report.append("HEAD \n")
report.append(df.head())
report.append("TAIL \n")
report.append(df.tail())

df.set_index('id').to_parquet(dst, compression='gzip')

with open(report_dst, 'a') as f:
    f.write(str(datetime.datetime.now()) + "\n")
    f.writelines([str(x) + "\n" for x in report])
