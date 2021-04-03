from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt


file = open("pid.txt","r")
pid_list = file.readlines()
pid_list_rstrip = [pid.replace("_",'/').rstrip() for pid in pid_list]


def get_coworker_graph(nodes, year = 2021, mode = "all", weighted = True):
    edges = []
    for pid_string in nodes:
        file = open(f'faculty_xml/{pid_string.replace("/","_")}.xml','r',encoding = 'utf-8')
        content = BeautifulSoup(file,"lxml")
        file.close()

        contents_r = content.findAll("r")
        for content_r in contents_r:
            content_year = int(content_r.find("year").text)
            #filter out content after year
            if (content_year <= year):
                coauthors = content_r.findAll("author")
                for coauthor in coauthors:
                    if((coauthor["pid"] in nodes) and (pid_string<coauthor["pid"])):
                        edge = (pid_string,coauthor["pid"])
                        edges.append(edge)

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    
    if weighted:
        #give weight to edges
        for i in edges:
            G[i[0]][i[1]]['weight']=edges.count(i)

    #use mode="connected" to filter out unconnected nodes
    if(mode=="connected"):
        isolates = list(nx.isolates(G))
        G.remove_nodes_from(isolates)
    #use mode="giant" to choose giant component onlyl
    if(mode=="giant"):
        giant = G.subgraph(max(nx.connected_components(G), key=len))
        return giant
    return(G)
def get_properties(G):
    number_of_nodes=G.number_of_nodes()
    number_of_edges=G.number_of_edges()
    average_degree=number_of_edges/number_of_nodes
    average_clustering=nx.average_clustering(G)
    print("number of nodes: n =", number_of_nodes)
    print("number of edges: ∑k =", number_of_edges)
    print("average degree: <k> =", average_degree)
    print("average clustering coefficient: <C> =", average_clustering)
    print("diameter: d = ", end="")
    try: 
        diameter=nx.diameter(G)
        print(diameter)
    except (nx.exception.NetworkXError):
        diameter = "NA"
        print("The graph is not connected")
    print("average distance: <d> = ", end="")
    try: 
        average_distance = nx.average_shortest_path_length(G)
        print(average_distance)
    except (nx.exception.NetworkXError):
        average_distance = "NA"
        print("The graph is not connected")

        
    degree_centrality = nx.degree_centrality(G)
    highest_degree_centrality_pid = max(degree_centrality, key=degree_centrality.get)
    highest_degree_centrality_value = degree_centrality.get(highest_degree_centrality_pid)
    print("highest degree centrality:", highest_degree_centrality_pid, highest_degree_centrality_value)
    
    #default using max_iter = 100, tolerance=10^-6
    #eigen_centrality = nx.eigenvector_centrality_numpy(G)
    eigen_centrality = nx.eigenvector_centrality(G)
    highest_eigen_centrality_pid = max(eigen_centrality, key=eigen_centrality.get)
    highest_eigen_centrality_value = eigen_centrality.get(highest_eigen_centrality_pid)
    print("highest eigen centrality:", highest_eigen_centrality_pid, highest_eigen_centrality_value)
    
    closeness_centrality = nx.closeness_centrality(G)
    highest_closeness_centrality_pid = max(closeness_centrality, key=closeness_centrality.get)
    highest_closeness_centrality_value = closeness_centrality.get(highest_closeness_centrality_pid)
    print("highest closeness centrality:", highest_closeness_centrality_pid, highest_closeness_centrality_value)
    
    betweenness_centrality = nx.betweenness_centrality(G)
    highest_betweenness_centrality_pid = max(betweenness_centrality, key=betweenness_centrality.get)
    highest_betweenness_centrality_value = betweenness_centrality.get(highest_betweenness_centrality_pid)
    print("highest betweenness centrality:", highest_betweenness_centrality_pid, highest_betweenness_centrality_value)
    
    #return a list of network properties
    result = []
    for i in (number_of_nodes,number_of_edges,average_degree,average_clustering,diameter,average_distance,highest_degree_centrality_pid,highest_degree_centrality_value,highest_eigen_centrality_pid,highest_eigen_centrality_value,highest_closeness_centrality_pid,highest_closeness_centrality_value,highest_betweenness_centrality_pid,highest_betweenness_centrality_value):
        result.append(i)
    return result

nodes = pid_list_rstrip
G = get_coworker_graph(nodes, year = 2019, mode = "connected", weighted = False)
nx.draw(G)
plt.show()
get_properties(G)

'''
##uncomment to write yearly output to result_year.csv in current directory
import csv
import time
import contextlib

file = open('result_yearly.csv', 'w+', newline ='')
with file:
    write = csv.writer(file)
    write.writerows([["Year","nodes","edges","average_degree","average_clustering","diameter","average_distance","highest_degree_centrality_pid","highest_degree_centrality_value","highest_eigen_centrality_pid","highest_eigen_centrality_value","highest_closeness_centrality_pid","highest_closeness_centrality_value","highest_betweenness_centrality_pid","highest_betweenness_centrality_value"]])
    with contextlib.redirect_stdout(None):
        for i in range(int(time.strftime("%Y")),1999,-1):
            G = get_coworker_graph(nodes, year = i, mode = "connected")
            result = get_properties(G)
            result.insert(0,i) 
            write.writerows([result])
print("result is written to file")
'''



    
