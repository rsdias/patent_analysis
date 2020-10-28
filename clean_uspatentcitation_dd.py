import pandas as pd
#import zipfile
#import gzip
import re
import csv
import dask.dataframe as dd
from dask.delayed import delayed
import glob
from fastparquet import ParquetFile

def clean_field(df, field):
    cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
    #df['patent_id']=df['patent_id'].apply(cleaning_patent, meta=pd.Series(dtype='object', name='patent_id'))
    df[field]=df[field].apply(cleaning_patent)
    return df

@delayed
def load_chunk(pth):
    return ParquetFile(pth).to_pandas()


file_list=glob.glob("parquet/uspatentcitation*.gz")
dst='data/cleanuspatentcitation.parquet.gz'
#file="D:\\PatentsView_2020\\uspatentcitation.tsv.zip"
#dst='D:\\PatentsView_2020\\cleanuspatentcitation.csv.gz'

first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right
# first_patent = datetime.date(1790, 7, 31)
df = dd.from_delayed([load_chunk(f) for f in file_list])
#df = delayed(pd.read_csv)(file_list, compression='zip', usecols=['patent_id', 'citation_id', 'date'], dtype=object, sep="\t", error_bad_lines=False, encoding="utf-8", nrows=64*1024)

#myTypes={'patent_id':object, 'citation_id':object, 'date':object}
#df = dd.from_delayed(df, meta=myTypes)

df=delayed(clean_field)(df, 'patent_id')

#correct_date=lambda x:re.sub('-00', "-01", x)
#df['date']=df['date'].apply(correct_date, meta=pd.Series(dtype='object', name='date'))

#df['date']=pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
#df.dropna(subset=['date'], inplace=True)

#result=client.persist(df)
df=df.compute(num_workers=8)

df.to_parquet(dst)
