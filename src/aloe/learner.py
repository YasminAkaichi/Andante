import itertools
from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.knowledge import MultipleKnowledge, LogicProgram
from aloe.clause import Clause, Constant, Variable, Operator
from aloe.mode import Type
from aloe.variablebank import VariableBank

class Learner(ABC):
    def __init__(self, options=None):
        assert isinstance(options, Options) or options is None
        self.options = options if options else Options()
        
    @abstractmethod
    def induce(self, examples, modes, knowledge, solver, verbose=None):
        pass

def match_head(atom, modes):
    """ 
    Should be in aloe.mode
    """
    if not atom.longname in modes.modeh:
        message = "There are no modes corresponding to '%s'" % (atom)
        raise Exception(message)
    modeh = modes.modeh[atom.longname]
    try: 
        return match(modeh.atom, atom)
    except:
        print('Error')

def match(mterm, term, vb=None):
    # subst1: skolem constant -> variable
    # subst2: variable -> type
    vb = vb if vb else VariableBank()

    plus_type  = set()
    minus_type = set()
    
    def _match(mterm, term):
        nonlocal vb, plus_type, minus_type
        if   isinstance(mterm, Type):
            if isinstance(term, Constant):
                if mterm.prefix in ('+', '-'):
                    if term not in vb.subst: 
                        vb.subst[term] = vb.newVariable()   
                    var = vb.subst[term]
                    if mterm.prefix=='+':
                        plus_type.add(term)
                    else: # mterm.prefix=='-'
                        minus_type.add(term)
                    return var
                else: # mterm.prefix=='#'
                    return term
            else:
                message = "Matching impossible of terms '%s' and '%s'" % (mterm, term)
                raise Exception(message)
        elif isinstance(mterm, Operator):
            if isinstance(term, Operator) and mterm.longname==term.longname:
                ts = list()
                for t1, t2 in zip(mterm, term):
                    t = _match(t1,t2)
                    if t is None: return None
                    ts.append(t)
                return term.__class__(term.name, ts)
        elif isinstance(mterm, Constant):
            if mterm != term:
                return None
            else: 
                return term
            
    return _match(mterm, term), vb, plus_type, minus_type

def generate_atom_from_InTerms(atom, InTerms, vb=None):
    vb = vb if vb is not None else VariableBank()
    if isinstance(atom, Type):
        if atom.prefix=='+':
            for skolem in InTerms:
                yield skolem
                #yield Constant(skolem)
        else:
            yield vb.newVariable()
    elif isinstance(atom, Constant):
        yield atom
    else: # isinstance(atom, Operator)
        children = [generate_atom_from_InTerms(t, InTerms, vb) for t in atom]
        for terms in itertools.product(*children):
            yield atom.__class__(atom.name, terms)
            
def construct_atom(matom, b, subst, vb):
    if isinstance(matom, Type):
        if   matom.prefix=='#':
            return subst[b], set()
        elif matom.prefix=='+':
            skolem = b
            if skolem not in vb.subst:
                vb.subst[skolem] = vb.newVariable()
            var = vb.subst[skolem]
            return var, set()
        else: # matom.prefix=='-'
            skolem = subst[b]
            if skolem not in vb.subst:
                vb.subst[skolem] = vb.newVariable()
            var = vb.subst[skolem]
            return var, {skolem}
    elif isinstance(matom, Constant):
        return matom, set()
    else: # isinstance(atom, Operator)
        children = []
        InTerms = set()
        for t, b_ in zip(matom,b):
            child, it = construct_atom(t, b_, subst, vb)
            children.append(child)
            InTerms.update(it)
        return matom.__class__(matom.name, children), InTerms
    
def get_variables(term):
    if   isinstance(term, Variable):
        return {term}
    elif isinstance(term, Operator):
        return set.union(*[get_variables(t) for t in term])
    else:
        return set()
            
class ProgolLearner(Learner):
    """ 
    Inductive logic learner as described by S. Muggleton in 'Inverse entailment and progol.' 1995
    available at http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.31.1630&rep=rep1&type=pdf
    """
        
    def build_bottom_i(self, example, modehandler, knowledge, solver):
        # 1. Add e_bar to the background knowledge
        ex_bckg = LogicProgram([example], options=self.options)
        bckg = MultipleKnowledge(knowledge, ex_bckg, options=self.options)
        
        # 2. Initialize InTerms and the bottom clause
        InTerms, bottom = set(), Clause(None, [])
        
        # 3. Modeh
        a = example.head
        h, vb, plus_type, minus_type = match_head(a, modehandler)
        InTerms.update(plus_type)
        bottom.head = h

        # 4. Modeb
        for i in range(self.options.i):
            next_InTerms = set()
            for modeb in modehandler.modeb4modeh(h.longname):
                for b in generate_atom_from_InTerms(modeb.atom, InTerms):
                    q = Clause(b, [])
                    success, subst_gen = solver.query(q, bckg, verbose=0)
                    if not success: continue
                    for subst in itertools.islice(subst_gen, modeb.recall):
                        bclause, it = construct_atom(modeb.atom, b, subst, vb)
                        next_InTerms.update(it)
                        if bclause not in bottom.body:
                            print(bclause)
                            bottom.body.append(bclause)
            InTerms = next_InTerms
        
        return bottom
    
    def build_hypothesis(self, examples, bottom_i, knowledge, solver):
        options = self.options
        verboseprint = print if self.verbose==1 else lambda *a, **k: None
        
        class State:
            def __init__(self, clause, vb=None, k=0):
                self.clause = clause
                self.localKnowledge = MultipleKnowledge(knowledge, LogicProgram([clause],options=options))
                self.vb = vb if vb is not None else VariableBank()
                self.k = k
                
                self.c = len(self.clause.body)
                temp = [get_variables(b) for b in clause.body]
                self.h = len(get_variables(clause.head) - set.union(*temp)) if temp else len(get_variables(clause.head))
                self.h = min(1,self.h)
                def solver_succeed(e):
                    success, _ = solver.solve(e, self.localKnowledge, verbose=0)
                    return success
                self.p = len([1 for e in examples['pos'] if solver_succeed(e)])
                self.n = len([1 for e in examples['neg'] if solver_succeed(e)])
                self.g = self.p - self.c - self.h
                self.f = self.g - self.n
                
            def copy(self): return State(self.clause.copy(), self.vb.copy(), self.k)
            def __str__(self): return '[%2d,%2d,%2d,%2d,%2d,%2d] Clause(k=%d):%s' %(self.c,self.h,self.p,self.n,self.g,self.f, self.k, str(self.clause))
            def __hash__(self): return hash(str(self))
            def __eq__(self, other): return str(self)==str(other)
        
        def best(collec):
            return max([s for s in collec if s.c<=self.options.c], key=lambda s: s.f)
        
        def prune(state):
            if (state.n==0 and state.f>0) or state.g<=0 or state.c>self.options.c:
                return True
            else: return False
        
        def terminated(Closed, Open):
            s = best(Closed)
            if len(Open)==0:
                return True
            elif s.n==0 and s.f>0 and s.f>=best(Open).g:
                return True
            else: return False
                
        def rho(state):
            for i in range(state.k, len(bottom_i.body)):
                c = Clause(state.clause.head, state.clause.body+[bottom_i.body[i]])
                s = State(c, state.vb.copy(), i+1)
                yield s

                
        
        s0 = State(Clause(bottom_i.head, []))
        Open = {s0}
        Closed = set()
        for _ in range(100):
            s = best(Open)
            verboseprint(s)
            Open.remove(s)
            Closed.add(s)
            
            if not prune(s):
                Open = (Open | set(list(rho(s)))) - Closed
                
            if terminated(Closed, Open):
                return best(Closed)
            
            if not Open:
                return None
        
    def induce(self, examples, modes, knowledge, solver, verbose=None):
        self.verbose = verbose if verbose is not None else self.options.verbose
        e1 = examples['pos'][0]
        bottom_i = self.build_bottom_i(e1, modes, knowledge, solver)
        C = self.build_hypothesis(examples, bottom_i, knowledge, solver)
        print('Example considered:',e1)
        print('Bottom_i',bottom_i)
        print('Clause found', C)
        return C
    
        
        
        