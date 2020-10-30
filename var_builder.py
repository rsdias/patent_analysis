#!/usr/bin/env python
# coding: utf-8
"""
# Script to evaluate citation delay
# Backward citation - citation made by a patent
# Forward citation - citation received by a patent

# Renato Kogeyama


# Oct 22, 2020
# The original script requires more than 32 GB RAM
# Changing from pd to dd (dask dataframe)

# Aug 19, 2020
# Included gzip
# Run with latest database


# Feb 07, 2020
# The main offensor of performance in this script is the transformation to timedelta
# the solution is to change to numpy
# https://stackoverflow.com/questions/52274356/conversion-of-a-timedelta-to-int-very-slow-in-python

# Jan 17 2020
# Join cit_delay with var_builder
# The only thing var_builder was doing was including kind and type 


# Jan 03 2020
# Miami
# I am using this script to calculate the average delay in citation - to follow Hall et al, 2001
# patent.csv has the following columns
# id 	type 	number 	country 	date 	abstract 	title 	kind 	num_claims 	filename
# interest on id, type, date, kind, num_claims

# I use two sources, uspatentcitation.tsv and patent.csv
# The first is a citation-level dataset with information about the citing patent
# The second is a patent-level dataset with information about the patent

# Cleaning
# I tested in other scripts the quality of the patent identifier
# It does not require cleaning - only 4 erros from 6 million patents
# The cleaning script is there anyway

# Merging
# I merge on the citation level (df)


# --

# First U.S. Patent Issued Today in 1790


# July 31, 2001
# Press Release
# #01-33

# On July 31, 1790 Samuel Hopkins was issued the first patent for a process 
# of making potash, an ingredient used in fertilizer. The patent was signed by 
# President George Washington. Hopkins was born in Vermont, but was living in 
# Philadelphia, Pa. when the patent was granted.

# The first patent, as well as the more than 6 million patents issued since then, 
# can be seen on the Department of Commerce's United States Patent and Trademark 
# Office website at www.uspto.gov. The original document is in the collections of 
# the Chicago Historical Society.


"""


import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import gzip
import dask.dataframe as dd
from dask.delayed import delayed
import datetime

def convert_and_subtract_dates(df):
    #conversao de string para data
    #df['citation_date']=dd.to_datetime(df['citation_date'], format="%Y-%m-%d", errors='coerce')
    #df['patent_date']=dd.to_datetime(df['patent_date'], format="%Y-%m-%d", errors='coerce') 
    df['citation_date']=df['citation_date'].apply([lambda x: np.datetime64(x)])
    df['citation_date']=df['patent_date'].apply([lambda x: np.datetime64(x)])
    # delay is the time interval between grant and citation
    df['cit_delay']=df['patent_date'].sub(df['citation_date'], axis=0)
    # convert to date interval format
    df['cit_delay']=pd.to_timedelta(df['cit_delay'])  
    # convert to interval in years
    df['cit_delay']=df['cit_delay'].dt.days/360
    # this is the may offensor of performance
    # change to numpy
    # https://stackoverflow.com/questions/52274356/conversion-of-a-timedelta-to-int-very-slow-in-python
    # this takes 40min
    # df['cit_delay']=pd.to_timedelta(df['cit_delay']).dt.components.days/365
    # lets try this alternativE
    # df['cit_delay']=df['cit_delay'].apply(lambda x: convert_to_delta(x)
    # does not work")

citation_df = 'data/cleanuspatentcitation.parquet.gz'
patent= 'data/cleanpatent.parquet.gz'
dst='data/var_builder.parquet.gz'
report_dst='var_builder_report.tex'

report=[] #file to export report

df = dd.read_parquet(citation_df, parse_dates=['date']).set_index('patent_id')
pt_df = dd.read_parquet(patent, parse_dates=['date']).set_index('id')

# dtype={'patent_id':object, 'citation_id':object}
#ddf=delayed(pd.read_csv)(citation_df, usecols=['patent_id', 'citation_id', 'date'], dtype=dtype, parse_dates=['date'])
#pt_ddf = delayed(pd.read_csv)(patent, usecols=['id', 'date'], dtype={'id':object}, parse_dates=['date']).set_index('id')

#df = dd.from_delayed(ddf)
#pt_df = dd.from_delayed(pt_ddf)

report.append("file citation head \n")
report.append(df.head().to_latex())
report.append("patent file head \n")
report.append("pt_df.head()")

df=df.rename(columns = {'date':'citation_date'})

# merge between patent data and citations on patent_id (citing)
# merging on the citation dataset drops patents without citing
# later i could standardize to make patent_id index and use join instead of merge
# df = df.set_index('patent_id').persist()
df=df.merge(pt_df, how='inner', left_index=True, right_index=True)

# report.append("Info after merging\n")
# report.append(df.info().to_latex())

# date format to allow calculations
df=df.rename(columns = {'date':'patent_date'})

# if I do not drop nans, the script raises an error later when converting day interval into years
# I could substitute with average instead of dropping, this way I do not lose the citation info
# however, not always it will be possible to average - cases where there is ony one citation, for example
# For this reason, at this point, I'll keep the NAN and circumvent the issues as they arise

# df=df.dropna()


report.append("head\n")
report.append(df.sort_values('cit_delay').head())
report.append("tail \n")
report.append(df.sort_values('cit_delay').tail())

# def convert_to_delta(x):
#     try:
#         return x/np.timedelta64(1, 'Y')
#     except:
#         return np.nan


report.append("describe\n")
report.append(df.describe())

report.append("head\n")
report.append(df.head())

#get_ipython().run_cell_magic('time', '', 'df.hist()')

#Check outliers
report.append("Check cit delay outliers - 0.15 quantile")
report.append(df[df["cit_delay"]>df["cit_delay"].quantile(0.15)].sort_values(by=['cit_delay'], ascending=True))

report.append("Check cit delay outliers -0.85 quantile")
report.append(df[df["cit_delay"]<df["cit_delay"].quantile(0.85)].sort_values(by=['cit_delay'], ascending=False))
df=df.compute(num_workers=8)
df.to_parquet(dst)

report.to_latex(report_dst)
