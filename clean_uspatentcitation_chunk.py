import pandas as pd
#import zipfile
#import gzip
import re
import csv

dst='cleanuspatentcitation_chunks.csv.gz'
file="data/uspatentcitation.tsv.zip"
df=pd.read_csv(file, compression='zip', sep="\t", chunksize=10000, error_bad_lines=False, encoding="utf-8")
cleaning_patent=lambda x:re.sub('([^a-zA-Z0-9]+)', "", x)
for chunk in df:
    chunk['patent_id']=chunk['patent_id'].apply(cleaning_patent)
    chunk.to_csv(dst, mode='a', compression='gzip')
