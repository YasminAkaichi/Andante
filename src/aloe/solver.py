from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.variablebank import VariableBank
from aloe.query import learn_subst, unify
from aloe.knowledge import Knowledge
from aloe.clause import Clause, Operator

class Solver(ABC):
    @abstractmethod
    def query(self, q, knowledge):
        pass
    
    def solve(self, q, knowledge): return self.query(q, knowledge)

class AloeSolver(Solver):
    def __init__(self, options=None):
        assert isinstance(options, Options) or options is None
        self.options = options if options else Options()
        
    def query(self, q, knowledge):
        """
        Launch a query
        Inputs: 
        q: a clause
        options: parameters for the query, see aloe.query
        """
        assert isinstance(knowledge, Knowledge)
        assert isinstance(q, Clause)
        if not q.is_unit():
            message = 'Query not implemented for non unit clauses\nClause: %s' % (clause)
            raise NotImplementedError(message)
        if q.head:
            atom = q.head 
            results = list(self._query([atom], knowledge))
            print('R',results)
            success = len(results)>0
            return success, results
        else:
            atom = q.body[0]
            results = list(self._query([atom], knowledge))
            success = len(results)>0
            return not success, results
            
    def _query(self, atoms, knowledge):
        """ 
        Checks the truth of an atom
        Takes a list of atoms as input
        """
        verboseprint = print if self.options.verbose else lambda *a, **k: None
        curr_state = AloeState(atoms)
        alternate_states = []
        count_h = 0
        while count_h < self.options.h:
            verboseprint(count_h)
            
            if not curr_state.has_atoms():
                yield curr_state.var_bank.subst
                if alternate_states:
                    curr_state = alternate_states.pop()
                else:
                    return
            
            atom = curr_state.next_atom()
            atom = curr_state.var_bank.apply_subst(atom)
            verboseprint('Atom', atom, atom.longname)
            
            # If a clause has not yet be matched to the atom
            if not curr_state.next_clause:
                # 1. Get all clauses whose head matches the atom
                candidates = knowledge.match(atom)
                verboseprint('Candidates', candidates)
                if not candidates: 
                    if not alternate_states:
                        return
                    else:
                        curr_state = alternate_states.pop()
                        continue

                # 2. Generate new atoms in state
                c1, *c2n = candidates
                curr_state.next_clause = c1
                for c in reversed(c2n):
                    s = curr_state.copy()
                    s.next_clause = c
                    s.atoms.append(atom)
                    alternate_states.append(s)
                    
                verboseprint('Match', candidates)
                
            # 3. 
            count_h  += 1
            clause   = curr_state.next_clause
            curr_state.next_clause = None
            var_bank = curr_state.var_bank
            clause   = var_bank.transform_clause(clause)
            subst = learn_subst(atom, clause.head)
            if subst:
                subst = unify(subst)
                            
            verboseprint('Clause', clause)
            verboseprint('Subst', subst)
            if subst is None:
                if not alternate_states:
                    return
                else:
                    curr_state = alternate_states.pop()
                    continue                
            
            var_bank.update_subst(subst)
            for b in reversed(clause.body):
                curr_state.atoms.append(curr_state.var_bank.apply_subst(b))
            verboseprint('Atoms', curr_state.atoms)
            
class AloeState:
    def __init__(self, atoms, var_bank=None, next_clause=None):
        self.var_bank = var_bank if var_bank is not None else VariableBank.build_from_atom(atoms[0])
        self.atoms = atoms
        self.curr_atom = None
        self.next_clause = next_clause
        
    def copy(self):
        return AloeState(self.atoms.copy(), self.var_bank.copy(), self.next_clause)
    
    def has_atoms(self):
        return len(self.atoms)>0
    
    def next_atom(self):
        self.curr_atom = self.atoms.pop()
        return self.curr_atom

    
def print_class_in_depth(element):
    print(element.__class__, element)
    if isinstance(element, Operator):
        for t in element:
            print('Child -',end=' ')
            print_class_in_depth(t)
