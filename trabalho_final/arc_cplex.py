from arc import *
class CCARP(CARP):
    def __init__(self,file):
        CARP.__init__(self,file)
    def get_name(self,arr,i):
        return str(arr[i][0])+"_"+str(arr[i][1])

    def setup_problem(self,c):

        c.objective.set_sense(c.objective.sense.minimize)
        req_names = [self.get_name(self.arc_req,i) for i in range(self.n_req)]
        n_req_names=[self.get_name(self.arc_not_req,i) for i in range(self.n_not_req)]
        names=req_names+n_req_names
        
        costs=np.concatenate((self.arc_req[:,2],self.arc_not_req[:,2])).astype(np.float)
        print (names)
        print(costs)
        
        c.variables.add(obj = costs,names=names)#, types = types) #names = xvar )
        #c.linear_constraints.add(
        #    lin_expr=[cplex.SparsePair(names, w)],
        #    senses=["L"],
        #    rhs=[self.wmax])
#
        #c.linear_constraints.add(
        #    lin_expr=[cplex.SparsePair([names[i]], val=[1]) for i in range (len(names))],
        #    senses=["L"]*len(names),
        #    rhs=[1]*len(names))
#
        #if max_lengh:
        #    other_names=names[self.vals]
        #    c.linear_constraints.add(
        #        lin_expr=[cplex.SparsePair(other_names,val=[1]*len(other_names))],
        #        senses=["E"],
        #        rhs=[len(other_names)])
#
        #    other_names_zero=names[self.vals_zeros]
        #    c.linear_constraints.add(
        #        lin_expr=[cplex.SparsePair(other_names_zero,val=[1]*len(other_names_zero))],
        #        senses=["E"],
        #        rhs=[0])
            

    def execute(self):
        c = cplex.Cplex()
        self.setup_problem(c)
        #self.setup_problem(c)
        #c.solve()
        #sol = c.solution
        #return sol

    
if __name__=="__main__":

    if len(sys.argv)!=2:
        print ("execucao: python arc_cplex TCARP-S2.dat")
        sys.exit(1)
    a=CCARP(sys.argv[1])
    a.execute()