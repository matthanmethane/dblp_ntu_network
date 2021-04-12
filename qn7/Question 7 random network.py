#!/usr/bin/env python
# coding: utf-8

# In[40]:


import preprocessingfQn7
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import operator
import faculty


# In[3]:


dictForAllCoAuthors = preprocessingfQn7.find_all_coauthors()


# # For Hiring faculty member, the condition set is that the co-author has to have written at least 4 publications with the same Author

# In[4]:


keylist = preprocessingfQn7.keys_return()


# In[5]:


listForEligible = []
dictOfEdges = {}
x=0
keylist = preprocessingfQn7.keys_return()
for i in range(len(keylist)):
    tempList = []
    for j in range(len(dictForAllCoAuthors[keylist[i]])):
        tempPid = (dictForAllCoAuthors[keylist[i]][j])
        count = 0
        for h in range(len(dictForAllCoAuthors[keylist[i]])):
            if tempPid == dictForAllCoAuthors[keylist[i]][h]:
                count = count + 1
        if count > 4 and tempPid not in listForEligible:   # count > 4 in order to account for the repeat.
            listForEligible.append(tempPid)
            tempList.append(tempPid)
    dictOfEdges[keylist[i]] = tempList
print(len(listForEligible))            
    


# In[6]:


print(len(dictOfEdges))


# In[7]:


listOfEdges = []
for i in range(len(keylist)):
    for j in range(len(dictForAllCoAuthors[keylist[i]])):
        tuple = (keylist[i],dictForAllCoAuthors[keylist[i]][j])
        listOfEdges.append(tuple)
        tuple = ()


# In[8]:


G = nx.Graph(dictOfEdges)
d = dict(G.degree)
# nx.draw(G)

color_map = []
for node in G:
    if len(G.edges(node))<1:
        color_map.append('blue')
    elif len(G.edges(node)) > 1 and len(G.edges(node))< 10:
        color_map.append('green')
    elif len(G.edges(node)) > 10 and len(G.edges(node)) < 20:
        color_map.append('yellow')
    else: 
        color_map.append('red')      
nx.draw(G, node_size = 10,node_color=color_map, with_labels=False)
plt.show()


# In[10]:


print(nx.info(G))


# In[ ]:





# In[15]:


degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')
sorted_degree = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse=True)
print("Top 20 nodes by degree:")
for d in sorted_degree[:20]:
    print(d)


# In[42]:


degree_cen_dict = nx.degree_centrality(G) # run degree centrality
betweenness_dict = nx.betweenness_centrality(G) # run betweenness centrality
eigenvector_dict = nx.eigenvector_centrality(G) # run eigenvector centrality

nx.set_node_attributes(G, degree_cen_dict , 'degree')
nx.set_node_attributes(G, betweenness_dict, 'betweenness')
nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')


# In[50]:


sorted_degreeC = sorted(degree_cen_dict.items(), key=operator.itemgetter(1), reverse=True)
df0= pd.DataFrame(sorted_degreeC)
df0.columns = ['Nodes','Degree Centrality']
print("Top 20 nodes by degree centrality:")
for b in sorted_degreeC[:20]:
    print(b)


# In[56]:


sorted_betweenness = sorted(betweenness_dict.items(), key=operator.itemgetter(1), reverse=True)
print("Top 20 nodes by betweenness centrality:")
df1= pd.DataFrame(sorted_betweenness)
df1.columns = ['Nodes','Betweeness Centrality']
for b in sorted_betweenness[:20]:
    print(b)


# In[61]:


sorted_eigenvector = sorted(eigenvector_dict.items(), key=operator.itemgetter(1), reverse=True)
df2=pd.DataFrame(sorted_eigenvector)
df2.columns = ['Nodes','Eigenvector Centrality']
print("Top 20 nodes by eigenvector centrality:")
for b in sorted_eigenvector[:20]:
    print(b)


# In[63]:


data = pd.read_excel('Faculty.xlsx')
df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])


# In[64]:


file = open("pid.txt",'r')
pidlist = []
for lines in file.readlines():
    pidlist.append(lines.strip('\n'))
df['pid'] = pidlist


# In[65]:


df1 = df[['Area', "pid"]]


# In[66]:


g= list(df1['pid'])
words = [w.replace('_', '/') for w in g]


# In[67]:


df1.drop(columns = 'pid')


# In[68]:


df1['pida']= words


# In[69]:


df1


# In[70]:


cyberSec = []
ai_ml = []
comVision = []
comArc = []
multiM=[]
comNet = []
distSys = []
bioM=[]
ir = []
listOfField=[]
for area in df1['Area']:
    if area not in listOfField:
        listOfField.append(area)


# In[71]:


print(len(listOfField))


# In[72]:


dictOfField = {}


for i in listOfField:
    listm=[]
    for ind in df1.index:
        if(str(df1['Area'][ind]) == str(i)):
            listm.append(df1['pida'][ind])
    dictOfField[i] =listm
    


# In[74]:


for keys in dictOfField:
    print(str(keys) + ' '+ str(len(dictOfField[keys])))


# In[75]:


noDict ={}
for keys in dictOfField:
    noDict[keys]= len(dictOfField[keys])


# In[76]:


dictA ={}
for s in dictOfEdges:
    dictA[s]=len(dictOfEdges[s])


# In[81]:


newDict =dictOfField
finalD={}
for s in newDict:
    og = 0
   
    for i in dictA:
        
        for m in range(len(newDict[s])):
            
            if str(i) == str(newDict[s][m]):
                finalD[s] = og + dictA[i]
                og = og + dictA[i]
                


# In[82]:


finalD


# In[ ]:




