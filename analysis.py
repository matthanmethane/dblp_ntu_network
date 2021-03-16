from preprocessing import find_pos_with_pid, find_man_with_pid, find_area_with_pid
import networkx as nx
import matplotlib.pyplot as plt

# pid = f = open("pid.txt", "r")
# s1=find_name_with_pid("66/549")

# s1.split(':')
# s1.split(':')[0]

# print(s1)

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

    print(G.nodes)
    print(G.edges)
    pos = nx.spring_layout(G, seed=7)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw(G, pos, with_labels=True)

    # plt.show()
    plt.savefig("rank_collab.png")

def management_collab():
    G = nx.Graph()

    for line in f:
        a, b = line.split()
        n1 = find_man_with_pid(a)
        n2 = find_man_with_pid(b)

        G.add_node(n1)
        G.add_node(n2)

        # edge = (n1, n2)
        # G.add_edge(*edge)
        # print(f.readline())

        if G.has_edge(n1, n2):
            # Increase weight by 1
            G[n1][n2]['weight'] += 1
        else:
            # new edge. add with weight = 1
            G.add_edge(n1, n2, weight=1)

    print(G.nodes)
    print(G.edges)
    
    d = dict(G.degree)
    pos = nx.spring_layout(G, seed=7)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw(G, pos, with_labels=True)
    # plt.show()
    plt.savefig("man_collab.png")

def area_collab():
    G = nx.Graph()

    for line in f:
        a, b = line.split()
        n1 = find_area_with_pid(a)
        n2 = find_area_with_pid(b)

        G.add_node(n1)
        G.add_node(n2)

        # edge = (n1, n2)
        # G.add_edge(*edge)
        # print(f.readline())

        if G.has_edge(n1, n2):
            # Increase weight by 1
            G[n1][n2]['weight'] += 1
        else:
            # new edge. add with weight = 1
            G.add_edge(n1, n2, weight=1)

    print(G.nodes)
    print(G.edges)
    
    d = dict(G.degree)
    pos = nx.spring_layout(G, seed=7)

    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw(G, pos, with_labels=True)
    # plt.show()
    plt.savefig("area_collab.png")

# rank_collab()
# management_collab()
area_collab()

# def load(fname):
#     G = nx.DiGraph()
#     d = simplejson.load(open(fname))
#     for item in d:
#         for attribute, value in item.iteritems():
#             subject_id, object_id = value['subject_id'], value['object_id']
#             if G.has_edge(subject_id, object_id):
#                 # we added this one before, just increase the weight by one
#                 G[subject_id][object_id]['weight'] += 1
#             else:
#                 # new edge. add with weight=1
#                 G.add_edge(subject_id, object_id, weight=1)
#     return G








