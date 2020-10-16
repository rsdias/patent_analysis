#!/usr/bin/env python
# coding: utf-8

# In[2]:


import matplotlib.pyplot as plt

#allows the plots to appear in the notebook
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# Plot
plt.plot([1,2,3,4,10])


# In[4]:


# 'go' stands for green dots
plt.plot([1,2,3,4,5], [1,2,3,4,10], 'go') #exemplos de x, y e 'formato'. Nesse caso, 'go' significa pontos verdes.
plt.show() #apenas exibe a figura, nao retorna o objeto


# In[5]:


# Draw two sets of points
plt.plot([1,2,3,4,5], [1,2,3,4,10], 'go')  # green dots
plt.plot([1,2,3,4,5], [2,3,4,5,11], 'b*')  # blue stars
plt.show()


# In[6]:


plt.plot([1,2,3,4,5], [1,2,3,4,10], 'go', label='GreenDots')
plt.plot([1,2,3,4,5], [2,3,4,5,11], 'b*', label='Bluestars')
plt.title('A Simple Scatterplot')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend(loc='best')  # legend text comes from the plot's label parameter.
plt.show()


# In[ ]:


import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
y_pos = np.arange(len(objects))
performance = [10,8,6,4,2,1]

plt.bar(y_pos, performance, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Usage')
plt.title('Programming language usage')

plt.show()

