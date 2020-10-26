import pandas as pd
#import zipfile
#import gzip
import re
import csv
import dask.dataframe as dd
from dask.delayed import delayed

file_list=["data/uspatentcitation.tsv.zip"]
dst='data/cleanuspatentcitation.csv.gz'
#file="D:\\PatentsView_2020\\uspatentcitation.tsv.zip"
#dst='D:\\PatentsView_2020\\cleanuspatentcitation.csv.gz'

first_patent = pd.to_datetime('1790-06-30', format="%Y-%m-%d") #helps us to identify citations with problems - small change from the actual first patent's grant date because one of the citations for n1 seems to be right
# first_patent = datetime.date(1790, 7, 31)
df = [delayed(pd.read_csv)(f, compression='zip', usecols=['patent_id', 'citation_id', 'date'], dtype=object, sep="\t", error_bad_lines=False, encoding="utf-8") for f in file_list]

myTypes={'patent_id':object, 'citation_id':object, 'date':object}
df = dd.from_delayed(df, meta=myTypes)

cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
df['patent_id']=df['patent_id'].apply(cleaning_patent, meta=pd.Series(dtype='object', name='patent_id'))

correct_date=lambda x:re.sub('-00', "-01", x)
df['date']=df['date'].apply(correct_date, meta=pd.Series(dtype='object', name='date'))

#df['date']=pd.to_datetime(df['date'], format="%Y-%m-%d", errors='coerce', infer_datetime_format=True)
#df.dropna(subset=['date'], inplace=True)

#result=client.persist(df)
result=result.compute(num_workers=12)

result.to_csv(dst, mode='w', compression='gzip', encoding='utf-8')
