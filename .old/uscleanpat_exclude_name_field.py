#Sao Paulo, July 31st, 2020
#Script to join CLEAN USPATENT CITATION AND SELF CITATION
#As this file will be use to calculate centrality, the output will be in the format used by the graphtool script (similar to patcitonly)
#using cleanpatentcitation has been increasingly burdensome.
#nbconvert freezes at a tcp call, direct python script is killed for some reason and dask finds an EOF error.
#to try to use dask, I am cleaning the name field previously with this script, so then I can process it with dask.

import gzip
import pandas as pd
import sys
sys.path.append('/home/rkogeyam/scripts/')
from append_output import append_output

pat='data/cleanuspatentcitation2.csv'
usecols=['uuid','patent_id', 'citation_id']

df=pd.read_csv(pat, usecols=usecols, dtype=object)
df.set_index('uuid', inplace=True)
"""
df.head()

#this function append basic df data to an output file
append_output(df, __file__.replace(".py",""))


df2=pd.read_csv(self_cit, dtype=object)
df2.set_index('uuid', inplace=True)
append_output(df2, __file__.replace(".py",""))

df=df.join(df2, how='outer')
append_output(df, __file__.replace(".py",""))
"""
"""
import dask.dataframe as dd

#dask generates a "dask.async.CParserError: Error tokenizing data. C error: EOF inside string starting at line 367620"
#it seems that dasks achieve parallelism by arbitrarily chunking the file - ie it may chunk at some problematic point
#more: https://stackoverflow.com/questions/62899330/read-csv-with-multiline-text-columns-by-dask

#I tried to clear the file with: "tr -dc '[:print:]\n' < data/cleanuspatentcitation.csv > data/cleanuspatentcitation2.csv"

#usecols=['uuid', 'patent_id', 'citation_id']
# Read in the csv files.
df1 = dd.read_csv(pat, sep=',', error_bad_lines=False).set_index('uuid')
#df1 = df1.set_index('uuid').persist()
df2 = dd.read_csv(self_cit, sep=',', error_bad_lines=False).set_index('uuid')
#df2 = df2.set_index('uuid').persist()

# Merge the csv files.
df = dd.merge(df1, df2, left_index=True)
"""

# Write the output.
df.to_csv('only_uuid_pat_cit.csv')

