# Arrij Fawwad
# I220755
# C 

from collections import defaultdict
import time
FileName = "Data/Data1.txt"
class Graph:
    def __init__(self):
        self.AdjList = defaultdict(list)
        self.weights = {}

    def AddEdge(self, u, v, weight=1.0):
        if v not in self.AdjList[u]:
            self.AdjList[u].append(v)
        if u not in self.AdjList[v]:
            self.AdjList[v].append(u)
        self.weights[(u, v)] = weight
        self.weights[(v, u)] = weight

    def neighbors(self, node):
        return self.AdjList.get(node, [])

    def nodes(self):
        return list(self.AdjList.keys())

    def edges(self):
        edges = set()
        for u in self.AdjList:
            for v in self.AdjList[u]:
                if u < v:
                    edges.add((u, v))
        return list(edges)

    def TotalNodes(self):
        return len(self.AdjList)

    def TotalEdges(self):
        return len(self.edges())

class Analyzer:
    def __init__(self):
        self.graph = Graph()

    def ReadData(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        u, v = parts[0], parts[1]
                        self.graph.AddEdge(u, v)
        except Exception as e:
            print(f"Error reading file: {e}")

    def SubGraphs(self, min_size=3, max_size=5, limit=50):
        results = {
            "stars": self.CountStars(),
            "chains": self.CountChains(),
            "cycles": self.CountCycles(),
            "cliques": self.CountCliques()
        }
        return results

    def CountStars(self):
        stars = []
        
        for center in self.graph.nodes():
            neighbors = self.graph.neighbors(center)
            
            if len(neighbors) < 2:
                continue
                
            isStar = True
            for neighbor in neighbors:
                if len(self.graph.neighbors(neighbor)) != 1:
                    isStar = False
                    break
                    
            if isStar:
                stars.append({
                    'center': center,
                    'spokes': neighbors,
                    'size': len(neighbors) + 1
                })
                
        return sorted(stars, key=lambda x: x['size'], reverse=True)

    def CountChains(self):
        chains = []
        visited = set()
        
        for node in self.graph.nodes():
            if node in visited:
                continue
                
            if len(self.graph.neighbors(node)) == 1:
                chain = [node]
                visited.add(node)
                current = self.graph.neighbors(node)[0]
                
                while current not in visited:
                    chain.append(current)
                    visited.add(current)
                    
                    NextNode = [n for n in self.graph.neighbors(current) if n not in visited]
                    
                    if len(NextNode) == 1:
                        current = NextNode[0]
                    elif len(NextNode) == 0:
                        break
                    else:
                        break
                
                if len(chain) >= 3:
                    chains.append({
                        'chain': chain,
                        'size': len(chain)
                    })
        
        return sorted(chains, key=lambda x: x['size'], reverse=True)

    def CountCycles(self):
        cycles = []
        VisitedCycles = set()
        
        def dfs(start, current, path=None, visited=None, max_depth=10):
            if path is None:
                path = []
            if visited is None:
                visited = set()
                
            path.append(current)
            visited.add(current)
            
            for neighbor in self.graph.neighbors(current):
                if neighbor == start and len(path) >= 3:
                    CycleKey = tuple(sorted(path))
                    if CycleKey not in VisitedCycles:
                        VisitedCycles.add(CycleKey)
                        cycles.append({
                            'cycle': path + [start],
                            'size': len(path) + 1
                        })
                elif neighbor not in visited and len(path) < max_depth:
                    dfs(start, neighbor, path.copy(), visited.copy(), max_depth)
        
        for node in self.graph.nodes():
            dfs(node, node)
        
        return sorted(cycles, key=lambda x: x['size'], reverse=True)

    def CountCliques(self):
        cliques = []
        
        def is_clique(nodes):
            for i in range(len(nodes)):
                for j in range(i+1, len(nodes)):
                    if nodes[j] not in self.graph.neighbors(nodes[i]):
                        return False
            return True
        
        def ExtendClique(current, candidates):
            if not candidates and len(current) >= 3:
                clique_key = tuple(sorted(current))
                if clique_key not in VisitedCliques:
                    VisitedCliques.add(clique_key)
                    cliques.append({
                        'clique': current.copy(),
                        'size': len(current)
                    })
                return
                
            for candidate in list(candidates):
                if all(neighbor in self.graph.neighbors(candidate) for neighbor in current):
                    new_current = current + [candidate]
                    new_candidates = candidates - {candidate}
                    ExtendClique(new_current, new_candidates)
        
        VisitedCliques = set()
        
        for node in self.graph.nodes():
            neighbors = set(self.graph.neighbors(node))
            if len(neighbors) >= 2:  
                ExtendClique([node], neighbors)
        
        return sorted(cliques, key=lambda x: x['size'], reverse=True)
        
    def GetResults(self, results):
        summary = [f"Nodes: {self.graph.TotalNodes()}", f"Edges: {self.graph.TotalEdges()}"]
        for subgraph_type, subgraphs in results.items():
            summary.append(f"{subgraph_type.capitalize()}: {len(subgraphs)} found")
        return "\n".join(summary)

# Main
start = time.time()
analyzer = Analyzer()
analyzer.ReadData(FileName)
print(f"Graph loaded in {time.time() - start:.2f} s")

results = analyzer.SubGraphs()
print(analyzer.GetResults(results))
