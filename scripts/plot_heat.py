#heatmaps
#annotated and no annotation
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def heatmap(x,y, decade=None):
    print('the decade is:', decade)
    
    if decade:
        year=decade
    else:
        year=''
        
    res = pd.crosstab(x, y)
    res = res.div(res.sum(axis=1), axis=0)
 
    fig, ax = plt.subplots(figsize=(10, 8))
    ax = sns.heatmap(res, annot=True, ax=ax, linewidths=0.5, linecolor='white')
    var1=x.name
    var2=y.name
    ax.set_title(str(year)+' Heatmap '+var1.title() +' vs. '+ var2.title()+'\n')
    prefix='./img/heat_'
    sufix='_'+str(year)+'.png'

    
    plt.savefig( prefix + var1 + '_' + var2 + sufix)   
    