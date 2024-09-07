import networkx as nx
G = nx.Graph()
import matplotlib.pyplot as plt 

# adicionando vertices
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)
G.add_node(5)
G.add_node(6)


# Visualizando os vertices
print(G.nodes())
 #[1, 2]

#adicionando arestas
G.add_edge(1, 2)
G.add_edge(1, 5)
G.add_edge(2, 5)
G.add_edge(2, 3)
G.add_edge(3, 4)
G.add_edge(4, 5)
G.add_edge(4, 6)

# Desenha o grafo
nx.draw(G, with_labels=True)

# Mostra o grafo
plt.show()

# total de vertices e arestas
n_vertices = G.number_of_nodes()
n_arestas = G.number_of_edges()

print('vertices: ', n_vertices, '\narestas: ', n_arestas)
