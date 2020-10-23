import pandas as pd
#import zipfile
#import gzip
import re
import csv

dst='data/cleanuspatentcitation.csv.gz'
file="data/uspatentcitation.tsv.zip"
df=pd.read_csv(file, compression='zip', sep="\t", chunksize=10000, error_bad_lines=False, encoding="utf-8")
cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
# first_patent = datetime.date(1790, 7, 31)
first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right
df clean(df):
    df['patent_id']=df['patent_id'].apply(cleaning_patent)
    df.date.replace({'-00':'-01'}, regex=True, inplace=True)
    df['date']=pd.to_datetime(chunk['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
    df.dropna(subset=['date'], inplace=True)
    df.to_csv(dst, mode='a', compression='gzip')
    
result=clean(df)
result=result.compute(num_workers=4)
