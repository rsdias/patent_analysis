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
    
file_list=glob.glob("parquet/uspatentcitation*")
dst='data/cleanuspatentcitation.parquet.gz'

# This is the date of the first patent ever granted, so patents with grant dates previous to these should be wrong
# first_patent = datetime.date(1790, 7, 31)
# small change from the actual first patent's grant date because one of the citations for n1 seems to be right
# first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") 

dfs = [delayed(pd.read_parquet)(f) for f in file_list]

myTypes={'patent_id':str, 'citation_id':str, 'date':object}
df = dd.from_delayed(dfs, meta=myTypes)

df=delayed(clean_field)(df)
df=delayed(correct_date)(df)
df=delayed(convert_todatetime)(df)

df.dropna(subset=['date'], inplace=True)

#result=client.persist(df)
df=df.compute(num_workers=8)
df.set_index('patent_id').to_parquet(dst, compression='gzip')

