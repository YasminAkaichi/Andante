import itertools
from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.knowledge import MultipleKnowledge, LogicProgram
from aloe.clause import Clause, Constant, Variable, Operator
from aloe.mode import Type
from aloe.variablebank import VariableBank

class Learner(ABC):
    def __init__(self, options=None):
        self.options = options if options else Options()
    
    @abstractmethod
    def induce(self, examples, modes, knowledge, solver):
        pass

def match_head(atom, modes):
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
                yield Constant(skolem)
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
        if matom.prefix=='+':
            return b, set()
        elif matom.prefix=='#':
            return subst[b], set()
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
                    print('Candidate:',q)
                    success, subst_gen = solver.query(q, bckg)
                    print(success,subst_gen)
                    print()
                    if not success: continue
                    for subst in itertools.islice(subst_gen, modeb.recall):
                        b, it = construct_atom(modeb.atom, b, subst, vb)
                        next_InTerms.update(it)
                        bottom.body.append(b)
            InTerms = next_InTerms
        
        return bottom
        
        
    def induce(self, examples, modes, knowledge, solver):
        e1 = examples['pos'][0]
        bottom_i = self.build_bottom_i(e1, modes, knowledge, solver)
        print(e1)
        print(bottom_i)
        return bottom_i
        
        
        