"""
#Sao Paulo, Aug 13th, 2020
#Adapted the script for excluding the name field from cleanuspatentcitation

#Sao Paulo, July 31st, 2020
#Script to join CLEAN USPATENT CITATION AND SELF CITATION
#As this file will be use to calculate centrality, the output will be in the format used by the graphtool script (similar to patcitonly)
#using cleanpatentcitation has been increasingly burdensome.
#nbconvert freezes at a tcp call, direct python script is killed for some reason and dask finds an EOF error.
#to try to use dask, I am cleaning the name field previously with this script, so then I can process it with dask.
"""

import gzip
import pandas as pd
import sys
sys.path.append('/home/rkogeyam/scripts/')
from append_output import append_output

pat='data/cleanuspatentcitation2.csv'
usecols=['uuid','patent_id', 'citation_id']

df=pd.read_csv(pat, usecols=usecols, dtype=object)
df.set_index('uuid', inplace=True)

# Write the output.
df.to_csv('only_uuid_pat_cit.csv')

