# MODEL GENERATOR i.e., chains_from_graph.txt
import networkx as nx

### THIS IS FOR TEMPORAL ONES
TRIGGER = 0
ACTION = 1

INPUT_FILE= 'generated_data/dot_files/policy.dot'
DATA_FILE= 'generated_data/data_for_graphs/tokens.txt'
OUTPUT_FILE = 'generated_data/chains/chains_temporal_graphHome.txt'



def findPaths(G,u,n):
    if n==0:
        return [[u]]
    paths = [[u]+path for neighbor in G.neighbors(u) for path in findPaths(G,neighbor,n-1) if u not in path]
    return paths


a = nx.drawing.nx_agraph.read_dot(INPUT_FILE)
G=nx.DiGraph(a) # Construct Directed Graph
# print("-->", list(G.nodes))
# Any node that doesn't have incoming edge
roots = [v for v, d in G.in_degree() if d == 0]
# print(len(roots))
# Any node that doesn't have outgoing edge
leaves = [v for v, d in G.out_degree() if d == 0]
# print(len(leaves))

khatra_hash = {}
khatra_hash['two'] = 0
khatra_hash['three'] = 0
khatra_hash['four'] = 0

for root in roots:
    for leaf in leaves:
        for path in nx.all_simple_paths(G, source=root, target=leaf):
            if(len(path) == 2):
                khatra_hash['two'] +=1
                # print(path)
            elif(len(path) == 3):
                khatra_hash['three'] +=1
                # print(path)
            elif(len(path) == 4):
                khatra_hash['four'] += 1
            print(len(path), path)

print(khatra_hash)

