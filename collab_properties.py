# Collab Properties
from preprocessing import find_pos_with_pid, find_man_with_pid, find_area_with_pid, find_name_with_pid
import networkx as nx
import matplotlib.pyplot as plt
import time

fig_count = 0

# Set True to select collaborative property to plot
num_collab = False
rank_collab = False
man_collab = False
area_collab = False


fig, axes = plt.subplots(5, 5, figsize=(20, 20))
ax = axes.flatten()

for i in range(int(time.strftime("%Y")),1999,-1):
    file = open(f'edge_lists/{str(i)+"_edge_list"}.txt','r')
    G = str(i)
    # print(G)
    G = nx.Graph()
    for line in file:
        a, b = line.split()
        # change faculty member name to track 
        if (find_name_with_pid(a) or find_name_with_pid(b)) == "Ong Yew Soon":
            # print(find_name_with_pid(a))

            if num_collab:
                n1 = a
                n2 = b

                G.add_node(n1)
                G.add_node(n2)
            
            if rank_collab:
                n1 = find_pos_with_pid(a)
                n2 = find_pos_with_pid(b)

                G.add_node(n1)
                G.add_node(n2)

            if man_collab:
                n1 = find_man_with_pid(a)
                n2 = find_man_with_pid(b)
                
                G.add_node(n1)
                G.add_node(n2)
            
            if area_collab:
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

    # plt.figure(fig_count)
    pos = nx.spring_layout(G, seed=7)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw(G, pos, with_labels=True, ax=ax[fig_count])
    ax[fig_count].set_axis_off()
    plt.tight_layout()

    fig_count = fig_count + 1

fig.delaxes(axes[4, 2])
fig.delaxes(axes[4, 3])
fig.delaxes(axes[4, 4])
# plt.tight_layout()
plt.show()

