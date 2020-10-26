"""
Sao Paulo, October 30th, 2020
This script reads parquet uspatentcitation files, drops rows with errors on patent and date fields.
This cleaning aims to avoid later processing problems.

This script should offer a report on the dropped rows.
Alternatively, it could generate a flag indicating rows with errors.

"""
import pandas as pd
import re
import csv
import dask.dataframe as dd
from dask.delayed import delayed
import glob
from fastparquet import ParquetFile

def clean_field(df):
    cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
    df.dropna(inplace=True)
    df['patent_id']=df['patent_id'].apply(cleaning_patent)
    return df

def correct_date(df):
    correct_date=lambda x:re.sub('-00', "-01", x)
    df['date']=df['date'].apply(correct_date)
    return df

def convert_todatetime(df):
    df['date']=dd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce')
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
    
file_list=glob.glob("parquet/uspatentcitation*")
dst='data/cleanuspatentcitation.parquet.gz'

first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right
# first_patent = datetime.date(1790, 7, 31)
dfs = [delayed(pd.read_csv)(f, compression='zip', usecols=['patent_id', 'citation_id', 'date'], dtype=object, sep="\t", error_bad_lines=False, encoding="utf-8") for f in file_list]


def cleaning(df): 
    cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
    df['patent_id']=df['patent_id'].apply(cleaning_patent)
    correct_date=lambda x:re.sub('-00', "-01", x)
    df['date']=df['date'].apply(correct_date)
    #df['date']=pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
    #df.dropna(subset=['date'], inplace=True)
    df.to_csv(dst, mode='w', compression='gzip', encoding='utf-8')

ddf = dd.from_delayed(dfs, meta={'patent_id':object, 'citation_id':object, 'date':object})
result=cleaning(df)
result=result.compute()
