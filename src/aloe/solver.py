from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.substitution import Substitution
from aloe.knowledge import Knowledge
from aloe.clause import Clause, Function, Goal, Literal, Atom, Negation
from aloe.exceptions import SubstitutionError

class Solver(ABC):
    def __init__(self, options=None):
        assert isinstance(options, Options) or options is None
        self.options = options or Options()
            
    @abstractmethod
    def query(self, q, knowledge, verbose=None):
        pass
    
    def solve(self, *args, **options): return self.query(*args, **options)
    
    def succeeds_on(self, q, knowledge, verbose=None):
        sigmas = self.query(q, knowledge, verbose=verbose)
        return len(sigmas)>0

class AloeSolver(Solver):
    def query(self, q, knowledge, sigma=None, verbose=None):
        """
        Launch a query
        Inputs: 
        q: Goal, Atom
        options: parameters for the query, see aloe.options
        """
        assert isinstance(knowledge, Knowledge)
        
        if isinstance(q, (Atom, Negation)):
            q = Goal([q])
        assert isinstance(q, Goal)
        self.verbose = verbose if verbose is not None else self.options.verbose
        
        # Initialisation
        sigma0 = sigma.copy() if sigma is not None else Substitution()
        sigma0.add_variables(q) # add variables from q to domain of sigma
        
        generators = [iter([sigma0])] + [None for _ in range(len(q))]
        i = 0
        while i>=0:
            sigma = next(generators[i],None)
            if sigma is None:
                i-=1 # backtrack
                continue
            if i==len(q):
                yield sigma.remove_excess_variables(sigma0.variables)
                continue
            
            if isinstance(q[i], Atom):                
                generators[i+1] = self._query([q[i]], knowledge, sigma)
                i+=1
            else: # isinstance(q[i], Negation)
                success = self.succeeds_on(q[i].goal, knowledge, sigma=sigma, verbose=self.verbose)
                if not success:
                    generators[i+1] = iter([sigma])
                    i+=1
                # if success, nothing happens, the solution sigma is ignored
            
    def _query(self, atoms, knowledge, sigma):
        """ 
        Checks the truth of an atom
        Takes a list of atoms as input
        Output is a generator of VariableBank objects, one for each solution
        """
        verboseprint = print if self.verbose else lambda *a, **k: None
        
        s = AloeState(atoms, sigma.copy())
        alternate_states = []
        count_h = 0
        while count_h < self.options.h:
            if not s.has_atoms():
                yield s.sigma
                if alternate_states:
                    s = alternate_states.pop()
                else:
                    return
                
            verboseprint('\nh', count_h)            
            
            atom = s.next_atom()            
            atom = s.sigma.apply_subst(atom)
            verboseprint('Atom', atom)
            
            # If a clause has not yet be matched to the atom
            if not s.next_clause:
                # 1. Get all clauses whose head matches the atom
                candidates = knowledge.match(atom)
                verboseprint('Candidates', candidates)
                if not candidates: 
                    if not alternate_states:
                        return
                    else:
                        s = alternate_states.pop()
                        continue

                # 2. Generate new atoms in state
                c1, *c2n = candidates
                s.next_clause = c1
                for c in reversed(c2n):
                    s_ = s.copy()
                    s_.next_clause = c
                    s_.atoms.append(atom)
                    alternate_states.append(s_)
                    
                verboseprint('Match', candidates)
                
            # 3. 
            count_h  += 1
            clause   = s.next_clause
            s.next_clause = None
            clause   = s.sigma.rename_variables(clause)
            
            verboseprint('Clause', clause)
            
            # Unification of two atoms
            try:
                s.sigma.unify(atom, clause.head)
            except SubstitutionError:
                verboseprint('Unification failed.')
                if not alternate_states: return
                else:
                    curr_state = alternate_states.pop()
                    continue       
                    
            verboseprint('Substitution', s.sigma)
                    
            for b in reversed(clause.body):
                s.atoms.append(s.sigma.apply_subst(b))
            verboseprint('Atoms', s.atoms)
            
    def succeeds_on(self, q, knowledge, sigma=None, verbose=None):
        # For literals and atoms
        assert isinstance(q, (Atom, Goal, Negation))
        if sigma is None:
            sigma = Substitution()
            sigma.add_variables(q)
        else:
            sigma = sigma.copy()
        self.verbose = verbose if verbose is not None else self.options.verbose
            
        if   isinstance(q, Negation):
            output_gen = self.query(q.goal, knowledge, sigma=sigma, verbose=verbose)
            return next(output_gen, None) is None
        else:
            output_gen = self.query(q, knowledge, sigma=sigma, verbose=verbose)
            return next(output_gen, None) is not None

            
class AloeState:
    def __init__(self, atoms, sigma=None, next_clause=None):
        assert isinstance(atoms, list) and all(isinstance(atom, Atom) for atom in atoms)
        assert sigma is None or isinstance(sigma, Substitution)
        assert next_clause is None or isinstance(next_clause, Clause)
        if not sigma:
            sigma = Substitution()
            sigma.rename_variables(atoms)
        self.sigma = sigma
        self.atoms = atoms
        self.curr_atom = None
        self.next_clause = next_clause
        
    def copy(self):
        return AloeState(self.atoms.copy(), self.sigma.copy(), self.next_clause)
    
    def has_atoms(self):
        return len(self.atoms)>0
    
    def next_atom(self):
        self.curr_atom = self.atoms.pop()
        return self.curr_atom
