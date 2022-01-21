from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.variablebank import VariableBank
from aloe.query import learn_subst, unify
from aloe.knowledge import Knowledge
from aloe.clause import Clause

class Solver(ABC):
    @abstractmethod
    def query(self, q, knowledge):
        pass

class AloeSolver(Solver):
    def __init__(self, options=None):
        assert isinstance(options, Options) or options is None
        self.options = options if options else Options()
        
    def query(self, q, knowledge):
        """
        Launch a query
        Inputs: 
        q: a clause or a list of clauses
        options: parameters for the query, see aloe.query
        """
        assert isinstance(knowledge, Knowledge)
        assert isinstance(q, Clause) \
            or (isinstance(q, list) and all(isinstance(el, Clause) for el in q))
        if isinstance(q, Clause):
            q = [q]
        for clause in q:
            if not clause.is_unit():
                message = 'Query not implemented for non unit clauses\nClause: %s' % (clause)
                raise NotImplementedError(message)
            if clause.head:
                atom = clause.head 
                results = list(self._query([atom], knowledge))
                success = len(results)>0
                yield (clause, success, results)
            else:
                atom = clause.body[0]
                results = list(self._query([atom], knowledge))
                success = len(results)>0
                yield (clause, not success, results)
            
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
            verboseprint('Atom', atom)
            
            # If a clause has not yet be matched to the atom
            if not curr_state.next_clause:
                # 1. Get all clauses whose head matches the atom
                candidates = knowledge.match(atom)
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
