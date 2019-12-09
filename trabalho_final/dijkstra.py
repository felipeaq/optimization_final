import heapq
import numpy as np
class Node:
    def __init__(self,present,ant,cost):
        self.present=present
        self.ant=ant
        self.cost=cost
        
    def __lt__(self, other):
        return self.cost < other.cost
    def __repr__(self):
        return "present: {} -> prev: {} cost: {}".format(self.present,self.ant,self.cost)

def dij_matrix(graph):
    return [dijkstra(i,graph) for i in range(len(graph))]

def dijkstra(start, graph):    
    node=Node(start,None,0)
    visited={start:node}
    l=[node]
    while l:
        v=heapq.heappop(l)
        for arc in graph[v.present]:
            n=Node(arc.j,v.present,arc.cost+v.cost)
            if not arc.j in visited.keys() or n<visited[arc.j]:
                visited[arc.j]=n
                heapq.heappush(l,n)
            
    return visited
                



if __name__=="__main__":
    a=node(1,4)
    b=node(2,6)
    c=node(1,6)

    l=[]

    heapq.heappush(l,b)
    heapq.heappush(l,a)
    heapq.heappush(l,c)
    print (l)





