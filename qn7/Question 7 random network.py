#!/usr/bin/env python
# coding: utf-8


import preprocessing_QN7
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import operator
import faculty



# # For Hiring faculty member, the condition set is that the co-author has to have written at least 4 publications with the same Author




def get_dict_of_edges():
    
    dictForAllCoAuthors = preprocessing_QN7.find_all_coauthors()    
    listForEligible = []
    dictOfEdges = {}
    x=0
    keylist = preprocessing_QN7.keys_return()
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
    
    return dictOfEdges


def draw_graph(dictOfEdges):
    
    G = nx.Graph(dictOfEdges)
    d = dict(G.degree)
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
    return G

def graph_Qn7(dictOfEdges):
    G = nx.Graph(dictOfEdges)
    return G

def get_graph_sorted_degree(G):
    result=[]
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("Top 20 nodes by degree:")
    for d in sorted_degree[:20]:
        print(d)
        result.append(d)
    return result

def get_graph_degree_cen(G):
    result=[]
    degree_cen_dict = nx.degree_centrality(G) # run degree centrality
    nx.set_node_attributes(G, degree_cen_dict , 'degree')
    
    sorted_degreeC = sorted(degree_cen_dict.items(), key=operator.itemgetter(1), reverse=True)
    df0= pd.DataFrame(sorted_degreeC)
    df0.columns = ['Nodes','Degree Centrality']
    print("Top 20 nodes by degree centrality:")
    for b in sorted_degreeC[:20]:
        print(b)
        result.append(b)
    return result

def get_graph_betweeness(G):
    result=[]
    betweenness_dict = nx.betweenness_centrality(G) # run betweenness centrality
    nx.set_node_attributes(G, betweenness_dict, 'betweenness')
    sorted_betweenness = sorted(betweenness_dict.items(), key=operator.itemgetter(1), reverse=True)
    print("Top 20 nodes by betweenness centrality:")
    df1= pd.DataFrame(sorted_betweenness)
    df1.columns = ['Nodes','Betweeness Centrality']
    for b in sorted_betweenness[:20]:
        print(b)
        result.append(b)
    return result


def get_graph_eigen(G):
    result=[]
    eigenvector_dict = nx.eigenvector_centrality(G) # run eigenvector centrality
    nx.set_node_attributes(G, eigenvector_dict, 'eigenvector')
    sorted_eigenvector = sorted(eigenvector_dict.items(), key=operator.itemgetter(1), reverse=True)
    df2=pd.DataFrame(sorted_eigenvector)
    df2.columns = ['Nodes','Eigenvector Centrality']
    print("Top 20 nodes by eigenvector centrality:")
    for b in sorted_eigenvector[:20]:
        print(b)
        result.append(b)
    return result




def get_dict_of_field():
    data = pd.read_excel('Faculty.xlsx')
    df = pd.DataFrame(data, columns=["Faculty","Position","Gender","Management","Area"])
    file = open("pid.txt",'r')
    pidlist = []
    for lines in file.readlines():
        pidlist.append(lines.strip('\n'))
    df['pid'] = pidlist


    df1 = df[['Area', "pid"]]


    g= list(df1['pid'])
    words = [w.replace('_', '/') for w in g]

    df1.drop(columns = 'pid')
    df1['pida']= words

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

    dictOfField = {}
    for i in listOfField:
        listm=[]
        for ind in df1.index:
            if(str(df1['Area'][ind]) == str(i)):
                listm.append(df1['pida'][ind])
        dictOfField[i] =listm
        
    return dictOfField  

def get_total_number(dictOfField,dictOfEdges):
    noDict ={}
    for keys in dictOfField:
        noDict[keys]= len(dictOfField[keys])


    dictA ={}
    for s in dictOfEdges:
        dictA[s]=len(dictOfEdges[s])


    newDict =dictOfField
    finalD={}
    for s in newDict:
        og = 0
       
        for i in dictA:
            
            for m in range(len(newDict[s])):
                
                if str(i) == str(newDict[s][m]):
                    finalD[s] = og + dictA[i]
                    og = og + dictA[i]
    data = finalD
    dfTotal = pd.DataFrame.from_dict(data,orient='index',columns=['Total New Members'])
    
    return dfTotal                

def show_new_members(G):
    LL = preprocessing_QN7.name_with_pid()
    df_edge = nx.to_pandas_edgelist(G)
    for index, row in df_edge.iterrows():
        for i in LL:
            if str(row[1]) == str(i[0]):
                row[1] = i[1]
    for index, row in df_edge.iterrows():
        for i in dictOfField:
            for g in dictOfField[i]:
          
                if str(row[0]) == str(g):
                
                    row[0] = str(i)
            
    df_edges = df_edge.rename(columns={'source': 'Department','target':'Name'})
    
    return df_edges







