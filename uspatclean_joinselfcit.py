#Sao Paulo, July 31st, 2020
#Script to join CLEAN USPATENT CITATION AND SELF CITATION
#As this file will be use to calculate centrality, the output will be in the format used by the graphtool script (similar to patcitonly)

import gzip
import pandas as pd
import sys
sys.path.append('/home/rkogeyam/scripts/')

pat='data/cleanuspatentcitation.csv.gz'
self='data/self_cit.csv.gz'

file=gzip.open(pat, 'r')
df=pd.read_csv(file, dtype=object)
df.set_index('uuid', inplace=True)

df.head()
append_output(df)
