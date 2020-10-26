import pandas as pd
#import zipfile
#import gzip
import re
import csv

file="data/uspatentcitation.tsv.zip"
dst='data/cleanuspatentcitation.csv.gz'
#file="D:\\PatentsView_2020\\uspatentcitation.tsv.zip"
#dst='D:\\PatentsView_2020\\cleanuspatentcitation.csv.gz'
df=pd.read_csv(file, compression='zip', sep="\t", chunksize=1024*1024, error_bad_lines=False, encoding="utf-8", usecols=['patent_id', 'citation_id', 'date'])
cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
# first_patent = datetime.date(1790, 7, 31)
first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right
for chunk in df:
    chunk['patent_id']=chunk['patent_id'].apply(cleaning_patent)
    chunk.date.replace({'-00':'-01'}, regex=True, inplace=True)
    chunk['date']=pd.to_datetime(chunk['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
    chunk.dropna(subset=['date'], inplace=True)
    chunk.to_csv(dst, mode='a', compression='gzip', encoding='utf-8')
