This folder contains the scripts for Determinants of Patent Citation

Update Jan 20, 2020:
application_reader: reads applications, merges to patents, no output
cit_delay: reads var_builder, calculate forward and backward delay averages, output var_builder2
citation_reader: reads uspatentcitation.tsv, cleans citation_id and patent_id, calculate forward and backward citations, and calculates cumulated backward citation, outputs cit_tree
clean_uspatentciation: clean patent citation file (could be turned into an script)
determinants_patent_citation_5: main analysis
generality: reads wipo_horiz classification data, joins to cleanuspatentcitation, exports to generality_temp
generality2: reads generality_temp, calculates generality and outputs to generality.csv
patent_reader:reads patent.csv



In Dec 31, 2019, it contains three main files:


patent_citation_tree-optimized.ipynb: reads citation file and generate patent-level citation count
determinants_patent_citation_1.ipynb: joins patent-level data such as classification
determinants_patent_citation_5.ipynb: generates analyses

The names may change with further manipulation.

And one auxiliary script to run the ipynb in the scheduler:
python_test.sub
