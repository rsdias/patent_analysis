import pandas as pd
import os
import pyarrow


file="data/otherreference.tsv.zip"

df = pd.read_csv(file, compression='zip', chunksize=15*1024*1024, dtype=object, sep="\t", error_bad_lines=False, encoding="utf-8")

for i, chunk in enumerate(df):
    #filename="parquet/uspatentcitation_"+f"{i:03d}"+".parquet.gz"
    filename="parquet/otherref_"+f"{i:03d}"+".parquet.gz"
    chunk.to_parquet(filename, compression='gzip', engine='pyarrow')