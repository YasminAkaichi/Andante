from abc import ABC
from aloe.clause import Clause, Type, extract_variables
from aloe.knowledge import MultipleKnowledge, LogicProgram
from aloe.substitution import Substitution

class HypothesisMetric(ABC):
    def State(self, *args, **kwargs):
        pass
    
    def best(self, collec):
        pass
    
    def prune(self, state):
        pass
    
    def terminated(self, Closed, Open):
        pass
    
    def rho(self, state):
        pass            
    
class FnMetric(HypothesisMetric):
    def __init__(self, B, E, M, bottom, solver, options):
        """
        B: background knowledge
        E: set of examples
        bottom: Clause object
        solver: Solver object
        options: Option object
        """
        self.B = B
        self.E = E
        self.M = M
        self.bottom = bottom
        self.solver = solver
        self.options = options
        
        self.build_d()
        
    def build_d(self):
        s  = Substitution()
        s.add_variables(self.bottom)

        self.d = dict()
                
        # var (-type) -> list of var (+type) 
        graph = {v:set() for v in s}
        
        # build graph        
        for atom in self.bottom.body:
            type_subst = s.get_type_subst(atom, self.M, body_atom=True)
            minus_type = [key for key, value in type_subst.subst.items() if isinstance(value,Type) and value.sign=='-']
            plus__type = [key for key, value in type_subst.subst.items() if isinstance(value,Type) and value.sign=='+']
            for v in minus_type:
                graph[v].update(plus__type)
        type_subst = s.get_type_subst(self.bottom.head, self.M, body_atom=False)
        
        l0 = [key for key, value in type_subst.subst.items() if isinstance(value,Type) and value.sign=='-']
        l = [l0]
        for i, li in enumerate(l):
            lnext = list()
            for v in li:
                self.d[v]=i
                lnext.extend(v_ for v_ in graph[v] if v_ not in self.d)
            if lnext:
                l.append(lnext)
        for var in s:
            if var not in self.d:
                self.d[var] = len(l)
                
    def d_of_clause(self, clause):
        vars_in_head = extract_variables(clause.head)
        vars_in_body = extract_variables(clause.body)
        vars_of_interest = {var for var in vars_in_head if self.d[var]!=0} | vars_in_body
        d_ = min(self.d[var] for var in vars_of_interest)
        return d_
                
    def State(self, *args, **kwargs):
        return self._State(self, *args, **kwargs)
    
    class _State:
        def __init__(self, hm, clause, k=0, E=None):
            """
            Represents a single state in the search for the best hypothesis
            hm: the metric used to compare hypotheses
            clause: the hypothesis at hand
            B: the knowledge composed from hm.B and clause
            k: position in the bottom clause
            E: the positive and negative examples
            E_cov: the examples covered
            
            The metrics are as follow:
            c: the number of atom in the body of clause
            h: an optimistic guess to the number of atoms still needed in the clause 
            p: the number of positive examples covered by B
            n: the number of negative examples covered by B
            g: p-c-h
            f: g-n = p-(c+h+n)
            """
            self.hm = hm            
            self.clause = clause
            self.B = MultipleKnowledge(hm.B, LogicProgram([clause],options=hm.options))
            self.k = k
            self.E = E if E is not None else hm.E
            self.E_cov = {label:[e for e in self.E[label] if hm.solver.succeeds_on(e.head, self.B, verbose=0)] for label in self.E}

            # Metrics for the state
            # - c: the number of atoms in the body of C
            self.c = len(self.clause.body)
            self.h = hm.d_of_clause(self.clause)
            self.p = len(self.E_cov['pos'])
            self.n = len(self.E_cov['neg'])
            self.g = self.p - self.c - self.h
            self.f = self.g - self.n
            
            self.metrics = (self.c,self.h,self.p,self.n,self.g,self.f)
            
        def copy(self): return self.hm.State(self.clause.copy(), self.k, self.E_cov)
        def __str__(self): 
            s = '[%3d,%3d,%3d,%3d,%3d,%3d]' % self.metrics
            return '%s %s' % (s, str(self.clause))
        def __hash__(self): return hash(str(self))
        def __eq__(self, other): return str(self)==str(other)

    def best(self, collec):
        return max([s for s in collec if s.c<=self.options.c], key=lambda s: s.f)

    def prune(self, state):
        if (state.n==0 and state.f>0) or state.g<=0 or state.c>self.options.c:
            return True
        else: return False

    def terminated(self, Closed, Open):
        s = self.best(Closed)
        if len(Open)==0:
            return True
        elif s.n==0 and s.f>0 and s.f>=self.best(Open).g:
            return True
        else: return False

    def rho(self, state):
        for i in range(state.k, len(self.bottom.body)):
            c = Clause(state.clause.head, state.clause.body+[self.bottom.body[i]])
            s = self.State(c, i+1, E=state.E_cov)
            # Added line, not in the paper
            if s.c<=self.options.c:
                yield s