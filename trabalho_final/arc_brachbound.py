from arc import *
from arc_heuristic import *

class BBCARP(CARP):
    def __init__(self,file):
        
        CARP.__init__(self,file,True)
        h=HCARP(file)
        self.bknowcost,self.bknowvec=h.run()
        self.bknowvec=list(self.bknowvec)
        print (self.bknowcost)
        print (self.bknowvec)
        
        self.base_vec=self.bknowvec[:]
        self.set_min_costs()
        

    def execute(self):
        self.branch_bound([],self.n_req)
        return self.bknowcost,self.bknowvec

    def set_min_costs(self):
        self.cost_table=np.zeros(self.n_req+1)
        k=sorted(self.arc, key=lambda a_entry: a_entry[2])
        cost=0
        for i in range (self.n_req):
            cost+=k[i][2]
            self.cost_table[i+1]=cost
        print (self.cost_table)
    def branch_bound(self,sol,N):
        cost=self.calc_cost(sol)
   
        if cost+self.cost_table[N]>self.bknowcost:
            print ("cut at: {}".format(N))
            return cost
        if N==0 and cost<=self.bknowcost:
            self.bknowcost=cost
            self.bknowvec=sol[:]
            print ("solution find {} {}".format(cost,sol))
        for i in range (N):
            node=self.base_vec.pop(0)
            sol.append(node)
            self.branch_bound(sol,N-1)
            sol.pop()
            self.base_vec.append(node)



if __name__=="__main__":

    if len(sys.argv)!=2:
        print ("execucao: python arc_heuristic.py instancias/kshs1.dat")
        sys.exit(1)
    a=BBCARP(sys.argv[1])
    a.execute()