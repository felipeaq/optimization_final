import numpy as np
import sys
from dijkstra import *

class ARC:
    def __init__(self,i,j,cost,dem=0):
        self.i=i
        self.j=j
        self.cost=cost 
        self.dem=dem

    def __repr__(self):
        return "({}->{} cost: {} dem:{}) ".format(self.i,self.j,self.cost,self.dem)

class CARP:
    def __init__(self,file,make_path=False):
        self.read(file)
        if make_path:
            self.contr_path()
    
    def contr_path(self):
        self.dist=dij_matrix(self.digraph)

    def node_arc_cost(self,inode,iarc):
        #get end postion, cost, demand from a node to an arc
        i,j=self.arc[iarc][0],self.arc[iarc][1]
        first=min(self.dist[inode][i],self.dist[inode][j])
        second=max((self.dist[inode][i],self.dist[inode][j]))
        cost=first.cost+self.arc[iarc][2]
        demand=self.arc[iarc][3]
        pos=second.present
        return (pos,cost,demand)

    def dep_cost(self,i):
        return self.dist[self.dep][i].cost

    def calc_cost(self,arc_order,start=None,cap=None):
        if not start:
            node=self.dep
        else:
            node=start
        if not cap:
            cap=self.cap
        cost=0
        for i in arc_order:
            
            if cap<self.arc[i][3]:
                cost+=self.dep_cost(node)
                node=self.dep
                cap=self.cap

            if cap<self.arc[i][3]:
                return float("inf")
            
            node,plus_cost,minus_cap=self.node_arc_cost(node,i)
            cost+=plus_cost
            cap-=minus_cap
        cost+=self.dep_cost(node)
        return cost
        
    def read(self,file):
        with open(file) as f:
            f.readline()
            f.readline()
            self.n_v=int(f.readline().split()[2])
            self.n_req=int(f.readline().split()[2])
            self.n_not_req=int(f.readline().split()[2])
            self.k=int(f.readline().split()[2])
            self.cap=int(f.readline().split()[2])
            f.readline()
            self.min_cost=int(f.readline().split()[2])
            
            f.readline()

            read_f=lambda x:(x[0][0][0])
            #read_f= lambda x:(x[0][1][0],int(x[0][2]),int(x[0][4]),int(x[0][6]))
            self.adj_list=[[] for i in range(self.n_v)]
            self.digraph=[[] for i in range(self.n_v)]
            self.arc_req=np.zeros([self.n_req,4],dtype=np.int)
            self.arc_not_req=np.zeros([self.n_not_req,4],dtype=np.int)
            for i in range (self.n_req):
                s=f.readline().split()
                l=int(s[1].strip(","))-1,int(s[2].strip(")"))-1,int(s[4]),int(s[6])
                self.adj_list[l[0]].append(ARC(l[0],l[1],l[2],l[3]))
                self.digraph[l[0]].append(ARC(l[0],l[1],l[2],l[3]))
                self.digraph[l[1]].append(ARC(l[1],l[0],l[2],l[3]))
                #self.adj_list[l[1]].append(l[0])
                self.arc_req[i]=l
            self.arc=self.arc_req
            #print (self.arc_req)
            s=f.readline().split()
            if s[0]=="DEPOSITO":
                self.dep=int(s[2])-1
                return
            for i in range (self.n_not_req):
                s=f.readline().split()
                l=int(s[1].strip(","))-1,int(s[2].strip(")"))-1,int(s[4]),0
                self.arc_not_req[i]=l
                self.adj_list[l[0]].append(ARC(l[0],l[1],l[2]))
                self.digraph[l[0]].append(ARC(l[0],l[1],l[2]))
                self.digraph[l[1]].append(ARC(l[1],l[0],l[2]))
                #self.adj_list[l[1]].append(l[0])
            s=f.readline().split()
            self.dep=int(s[2])-1
            #print (self.arc_not_req)
            #print ("*"*100)
            #print (self.adj_list)
            self.arc=np.concatenate((self.arc,self.arc_not_req))
            #print (self.arc)
            #print ("#"*1000)

    


    