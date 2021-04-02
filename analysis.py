from preprocessing import find_pos_with_pid, find_man_with_pid, find_area_with_pid
import networkx as nx
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns

f = open("edge_list.txt", "r")

def rank_collab():

    G = nx.Graph()

    for line in f:
        a, b = line.split()
        n1 = find_pos_with_pid(a)
        n2 = find_pos_with_pid(b)

        G.add_node(n1)
        G.add_node(n2)

        if G.has_edge(n1, n2):
            # Increase weight by 1
            G[n1][n2]['weight'] += 1
        else:
            # new edge. add with weight = 1
            G.add_edge(n1, n2, weight=1)

    nodes = G.nodes()

    A = nx.to_numpy_array(G, nodelist=nodes)
    sns.heatmap(A, annot=True, xticklabels=nodes, yticklabels=nodes,cmap="Blues")
    plt.show()
    plt.savefig("rank_collab_heatmap.png")
    
    pos = nx.spring_layout(G, seed=7)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw(G, pos, with_labels=True)
    plt.show()
    plt.savefig("rank_collab_nwGraph.png")

def management_collab():
    G = nx.Graph()

    for line in f:
        a, b = line.split()
        n1 = find_man_with_pid(a)
        n2 = find_man_with_pid(b)

        G.add_node(n1)
        G.add_node(n2)

        if G.has_edge(n1, n2):
            # Increase weight by 1
            G[n1][n2]['weight'] += 1
        else:
            # new edge. add with weight = 1
            G.add_edge(n1, n2, weight=1)

    pos = nx.spring_layout(G, seed=7)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw(G, pos, with_labels=True)
    plt.show()
    plt.savefig("man_collab_nwGraph.png")

def area_collab():
    G = nx.Graph()

    for line in f:
        a, b = line.split()
        n1 = find_area_with_pid(a)
        n2 = find_area_with_pid(b)

        G.add_node(n1)
        G.add_node(n2)

        if G.has_edge(n1, n2):
            # Increase weight by 1
            G[n1][n2]['weight'] += 1
        else:
            # new edge. add with weight = 1
            G.add_edge(n1, n2, weight=1)
    
    for node in G.nodes():
        print (node, G.degree(node))

    degrees = G.degree()
    nodes = G.nodes()

    A = nx.to_numpy_array(G, nodelist=nodes)
    sns.heatmap(A, annot=True, xticklabels=nodes, yticklabels=nodes,cmap="Blues")
    plt.show()
    plt.savefig("area_collab_heatmap.png")

    pos = nx.spring_layout(G, seed=7)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    n_color = np.asarray([degrees[n] for n in nodes])
    nx.draw(G, pos=pos, with_labels=True, node_color=n_color, node_size=300, cmap=plt.cm.Blues)
    sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(vmin=4, vmax=13))
    plt.colorbar(sm)
    plt.show()
    plt.savefig("area_collab_nwGraph.png")

rank_collab()
management_collab()
area_collab()