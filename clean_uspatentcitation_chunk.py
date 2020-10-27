import pandas as pd
#import zipfile
#import gzip
import re
import csv
import dask.dataframe as dd
import multiprocessing

dst='data/cleanuspatentcitation.parquet'
file="data/uspatentcitation.tsv.zip"
df=pd.read_csv(file, compression='zip', sep="\t", encoding="utf-8")
# first_patent = datetime.date(1790, 7, 31)
first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right

cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
#df['patent_id']=df['patent_id'].swifter.apply(cleaning_patent)
ddata=dd.from_pandas(df, npartitions=4*multiprocessing.cpu_count()).map_partitions(lambda df: df.apply(cleaning_patent)).compute(scheduler='processes')

#replace_zeroes=lambda x:re.sub('-00', "-01", x)
#df['date']=df['date'].swifter.apply(replace_zeroes)
#df['date']=pd.to_datetime(chunk['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
#df.dropna(subset=['date'], inplace=True)
df.to_parquet(dst)
    
#result=clean(df)
#result=result.compute(num_workers=4)
