#this function plots three different kinds of bar graphs 

#without options, it plots the bar graph for each categorical variable
#count the 'ids', the only variable guaranteed to exist in any case

#with decade==True, it plots bar graphs with count per decade
#the idea is to observe the infuence of changes in policy

#with both decade==True and decade_x==True, the graph flips the axis
#the idea is to provide better visualization in some cases 

#today is Feb 03, 2020
#this function can be rewritten to be more readable
#many almost repeated lines can be rewritten to become one

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib

def plotbar(attribute, df, classes, decade=False, decade_x=False):
    
    fig, ax = plt.subplots(figsize=(6,4))
    filename='./img/bar_'

    if decade==True:
        table=df.reset_index().groupby([attribute, 'decade']).count()['id'].sort_values(ascending=False).reset_index()
    else:
        table=df.reset_index().groupby(attribute).count()['id'].sort_values(ascending=False).reset_index()
        

    try:
        class_codes=attribute.replace('_id', '')
        table[attribute]=table[attribute].replace(classes[class_codes])
    
    except: #for kind and type
        class_codes=attribute
    
    plt.title('Total number of patents per ' + class_codes.replace("_"," ").title() + '\n')
    filename=''.join([filename, class_codes])

    if decade==True:
        if decade_x==False:
            ax = sns.barplot(x='id', y=attribute, hue='decade', data=table)
            filename=''.join([filename, '_dec'])
            ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))


        else:
            ax = sns.barplot(x='decade', y='id', hue=attribute, data=table)
            filename=''.join([filename, '_dec_x'])
            ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

            
    else:
        ax = sns.barplot(x='id', y=attribute, data=table)
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

    
    ax.yaxis.label.set_visible(False)
    ax.xaxis.label.set_visible(False)
    
    plt.tight_layout()
    plt.savefig(filename+'.png')
    plt.show()