#  import networkx as nx
#  import swifter
#  matplotlib.use('Agg')
#
#  import collections
#
#
#  G = nx.DiGraph()
#  counter = 0

#      global G, node2idx, counter
#          node2idx[transaction['account_id']] = counter
#      
#      if not node2idx.get(transaction['account'], None):
#          counter += 1

#  
#      G.add_edge(u, v, weight=amount)

#  
#      pickle.dump(G, f)

#  
#      indeg = [G.in_degree(v) for v in G]

#      indegs, indegs_counts = np.unique(indeg, return_counts=True)

#  