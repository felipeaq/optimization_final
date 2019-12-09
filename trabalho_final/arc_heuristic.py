from arc import *
from dijkstra import *
import random
import numpy as np
import time

class SearchAlg:
    def __init__(self):
        pass
    def annealing(self,c, maxsteps=2600,T=9999999,f=0.99,size=100):
        state = c.random_start()
        cost = c.calc_cost(state)
        print ("initial_cost:",cost)
        bcost=cost
        states, costs = [state], [cost]
        for i in range(maxsteps):
            
            T*=f
            if T<=0.0001:
                print (i,"a")
                break
            
            new_state,new_cost=self.vec_random(c,state,size,T)
            if new_cost<bcost:
                bcost=new_cost
                bstate=new_state
                states.append(bstate)
                costs.append(bcost)
                state=bstate
                cost=bcost

            elif np.exp((new_cost-cost)/  T) > random.random():
                state, cost = new_state, new_cost
                states.append(state)
                costs.append(cost)

        return bcost,bstate

    def vec_random(self,c,state,size,T):
        
        bstate=None
        bcost=float("inf")
        for i in range(size):
            n_state=c.random_neighbour(state,T)
            cost=c.calc_cost(n_state)
            if cost<bcost:
                bcost=cost
                bindex=i
                bstate=n_state
        return bstate,bcost
    def swap_values(self,c,state):
        
        cost=c.calc_cost(state)
        swaping=True
        while(swaping):
            print (cost)
            swaping=False
            for i in range (c.n_req):
                for j in range (c.n_req):
                    state[i],state[j]=state[j],state[i]
                    cost_new=c.calc_cost(state)
                    if (cost_new<cost):
                        cost=cost_new
                        swaping=True
                    else:
                        state[i],state[j]=state[j],state[i]
        return cost, state
    

class HCARP(CARP):
    def __init__(self,file):
        CARP.__init__(self,file,True)

    def random_start(self):
        v=np.arange(self.n_req)
        for i in range(self.n_req):
            j=random.randint(0,self.n_req-1)
            v[i],v[j]=v[j],v[i]
        return v

    def random_neighbour(self,state,T):
        new_state=state.copy()
        i=random.randint(0,self.n_req-1)
        j=random.randint(0,self.n_req-1)
        while i==j:
            j=random.randint(0,self.n_req-1)
        new_state[i],new_state[j]=new_state[j],new_state[i]
        return new_state

    def run(self,maxsteps=2600):
        begin=time.time()
        s=SearchAlg()
        bcost,bstate=s.annealing(self,maxsteps=maxsteps)
        bcost,bstate=s.swap_values(self,bstate)
        print (bcost)
        print (time.time()-begin)
        return bcost,bstate
        
    
    def run_and_save(self):
        with open ("dados.csv","a") as f:
            
            s=SearchAlg()
            st=sys.argv[1]
            begin=time.time()
            bcost,bstate=s.annealing(self)
            st+=";"+str(time.time()-begin)
            st+=";"+str(bcost)
            bcost,bstate=s.swap_values(self,bstate)
            st+=";"+str(time.time()-begin)
            st+=";"+str(bcost)+"\n"
            f.write(st)

if __name__=="__main__":

    if len(sys.argv)!=2:
        print ("execucao: python arc_heuristic.py instancias/kshs1.dat")
        sys.exit(1)
    a=HCARP(sys.argv[1])
    a.run_and_save()