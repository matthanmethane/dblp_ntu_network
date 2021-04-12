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
    #print("number of nodes: n =", number_of_nodes)
    #print("number of edges: ∑k =", number_of_edges)
    #print("average degree: <k> =", average_degree)
    #print("average clustering coefficient: <C> =", average_clustering)
    #print("diameter: d = ", end="")
    try: 
        diameter=nx.diameter(G)
        #print(diameter)
    except (nx.exception.NetworkXError):
        diameter = "NaN"
        #print("The graph is not connected")
    #print("average distance: <d> = ", end="")
    try: 
        average_distance = nx.average_shortest_path_length(G)
        #print(average_distance)
    except (nx.exception.NetworkXError):
        average_distance = "NaN"
        #print("The graph is not connected")

        
    degree_centrality = nx.degree_centrality(G)
    highest_degree_centrality_pid = max(degree_centrality, key=degree_centrality.get)
    highest_degree_centrality_value = degree_centrality.get(highest_degree_centrality_pid)
    #print("highest degree centrality:", highest_degree_centrality_pid, highest_degree_centrality_value)
    
    #default using max_iter = 100, tolerance=10^-6
    #eigen_centrality = nx.eigenvector_centrality_numpy(G)
    eigen_centrality = nx.eigenvector_centrality(G)
    highest_eigen_centrality_pid = max(eigen_centrality, key=eigen_centrality.get)
    highest_eigen_centrality_value = eigen_centrality.get(highest_eigen_centrality_pid)
    #print("highest eigen centrality:", highest_eigen_centrality_pid, highest_eigen_centrality_value)
    
    closeness_centrality = nx.closeness_centrality(G)
    highest_closeness_centrality_pid = max(closeness_centrality, key=closeness_centrality.get)
    highest_closeness_centrality_value = closeness_centrality.get(highest_closeness_centrality_pid)
    #print("highest closeness centrality:", highest_closeness_centrality_pid, highest_closeness_centrality_value)
    
    betweenness_centrality = nx.betweenness_centrality(G)
    highest_betweenness_centrality_pid = max(betweenness_centrality, key=betweenness_centrality.get)
    highest_betweenness_centrality_value = betweenness_centrality.get(highest_betweenness_centrality_pid)
    #print("highest betweenness centrality:", highest_betweenness_centrality_pid, highest_betweenness_centrality_value)
    
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
import time
import contextlib

with contextlib.redirect_stdout(None):
    result_dict = {"Year":[],"nodes":[],"edges":[],"average_degree":[],"average_clustering":[],"diameter":[],"average_distance":[],"highest_degree_centrality_pid":[],"highest_degree_centrality_value":[],"highest_eigen_centrality_pid":[],"highest_eigen_centrality_value":[],"highest_closeness_centrality_pid":[],"highest_closeness_centrality_value":[],"highest_betweenness_centrality_pid":[],"highest_betweenness_centrality_value":[]}
    dict_keys=["Year","nodes","edges","average_degree","average_clustering","diameter","average_distance","highest_degree_centrality_pid","highest_degree_centrality_value","highest_eigen_centrality_pid","highest_eigen_centrality_value","highest_closeness_centrality_pid","highest_closeness_centrality_value","highest_betweenness_centrality_pid","highest_betweenness_centrality_value"]
    for i in range(int(time.strftime("%Y")),2000-1,-1):
        G = get_coworker_graph(nodes, year = i, mode = "giant")
        result = get_properties(G)
        result.insert(0,i) 
        for i in range(len(result)):
            result_dict[dict_keys[i]].append(result[i])

result_df = pd.DataFrame.from_dict(result_dict)
#print(result_df)
#result_df.to_csv('result_yearly.csv', index=False)

                    
#create columns showing difference by year (current_year[data]-last_year[data])
def yearly_diff(df,N=1)
    shift_range = N+1
    merging_keys = ['Year']
    lag_cols = ['nodes','edges','average_degree','average_clustering']
    for shift in range(1,shift_range):
        df_shift = df[merging_keys + lag_cols].copy()

        # E.g. Year of 2000 becomes 2001, for shift = 1.
        # So when this is merged with Year of 2001 in df, this will represent lag of 2001.
        df_shift['Year'] = df_shift['Year'] + shift
        foo = lambda x: '{}_lag_{}'.format(x, shift) if x in lag_cols else x
        df_shift = df_shift.rename(columns=foo)
        df = pd.merge(df, df_shift, on=merging_keys, how='left') #.fillna(0)

        bar = lambda x: '{}_diff_{}'.format(x, shift) if x in lag_cols else x
        for i in lag_cols:
            df[bar(i)]=df[i]-df[foo(i)]
            df.drop(foo(i), axis=1, inplace=True)
    del df_shift
df = yearly_diff(df,N=1)
#df.head()
    
