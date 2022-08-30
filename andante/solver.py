"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.
"""

from abc import ABC, abstractmethod
from andante.options import Options, ObjectWithTemporaryOptions
from andante.substitution import Substitution, SubstitutionError
from andante.knowledge import Knowledge
from andante.logic_concepts import Clause, Function, Goal, Atom, Negation
from andante.mathematical_expressions import Comparison, Is

class Solver(ObjectWithTemporaryOptions, ABC):
    """ Deduction engine """
    def __init__(self, options=None):
        super().__init__(options)
            
    @abstractmethod
    def query(self, q, knowledge, verbose=None):
        """ Queries some knowledge

        This function returns a generator of all possible substitutions for a 
        given query and a given knowledge

        Parameters
        ----------
        q: andante.logic_concepts.Goal
            The goal
        knowledge: andante.knowledge.Knowledge
            The knowledge 

        Yields
        ------
        subst : andante.substitution.Substitution
            A possible substitution for the query
        """
        pass
    
    def solve(self, *args, **options): 
        """ Same behavior as query """
        return self.query(*args, **options)
    
    def succeeds_on(self, q, knowledge, verbose=None):
        """ Similar to the query method but outputs a boolean.

        Returns true if there exists at least a substitution for the query.
        Otherwise returns false.
        """
        sigmas = self.query(q, knowledge, verbose=verbose)
        return len(sigmas)>0

class AndanteSolver(Solver):
    def query(self, q, knowledge, sigma=None, **temp_options):
        assert isinstance(knowledge, Knowledge)
        if isinstance(q, (Atom, Negation)):
            q = Goal([q])
        assert isinstance(q, Goal)
        
        self.add_temporary_options(**temp_options)
        
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
                success = self.succeeds_on(q[i].goal, knowledge, sigma=sigma)
                if not success:
                    generators[i+1] = iter([sigma])
                    i+=1
                # if success, nothing happens, the solution sigma is ignored
                
        self.rem_temporary_options()
            
    def _query(self, atoms, knowledge, sigma):
        """ Subfunction for query

        This function takes a list of andante.logic_concepts.Atom as inputs and
        otherwise works the same way as the query method.
        """
        s = AndanteState(atoms, sigma.copy())
        alternate_states = []
        count_h = 0
        while count_h < self.options.h:
            if not s.has_atoms():
                yield s.sigma
                if alternate_states:
                    s = alternate_states.pop()
                else:
                    return
                
            self.verboseprint('\nh', count_h)            
            
            atom = s.next_atom()            
            atom = s.sigma.substitute(atom)
            self.verboseprint('Atom', atom)
            
            if isinstance(atom, (Comparison, Is)):
                if not atom.evaluate(s.sigma):
                    if not alternate_states:
                        return
                    else:
                        s = alternate_states.pop()
                        continue
                else:
                    continue
            
            # If a clause has not yet be matched to the atom
            if not s.next_clause:
                # 1. Get all clauses whose head matches the atom
                candidates = knowledge.match(atom)
                self.verboseprint('Candidates', candidates)
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
                    
                self.verboseprint('Match', candidates)
                
            # 3. 
            count_h  += 1
            clause   = s.next_clause
            s.next_clause = None
            clause   = s.sigma.rename_variables(clause)
            
            self.verboseprint('Clause', clause)
            
            # Unification of two atoms
            try:
                s.sigma.unify(atom, clause.head)
            except SubstitutionError:
                self.verboseprint('Unification failed.')
                if not alternate_states: return
                else:
                    curr_state = alternate_states.pop()
                    continue       
                    
            self.verboseprint('Substitution', s.sigma)
                    
            for b in reversed(clause.body):
                s.atoms.append(s.sigma.substitute(b))
            self.verboseprint('Atoms', s.atoms)
            
    def succeeds_on(self, q, knowledge, sigma=None, **temp_options):
        # For literals and atoms
        assert isinstance(q, (Atom, Goal, Negation))
        
        self.add_temporary_options(**temp_options)
        
        if sigma is None:
            sigma = Substitution()
            sigma.add_variables(q)
        else:
            sigma = sigma.copy()
            
        if   isinstance(q, Negation):
            output_gen = self.query(q.goal, knowledge, sigma=sigma)
            sol_exists = next(output_gen, None) is not None
            success    = not sol_exists
        else:
            output_gen = self.query(q, knowledge, sigma=sigma)
            sol_exists = next(output_gen, None) is not None
            success    = sol_exists
            
        if sol_exists: # generator is not finished, we need to do the following manually
            self.rem_temporary_options()
        
        self.rem_temporary_options()
        return success

            
class AndanteState:
    """ State used in function _query

    Attributes
    ----------
    sigma : andante.substitution.Substitution
        The substitution at a given state
    atoms : list of aloe.logic_concepts.Atom
        List of atoms that still need to be proven true
    curr_atom : aloe.logic_concepts.Atom
        The current atom we try to make true
    next_clause : aloe.logic_concepts.Clause
        The clause we need to observe next
    """
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
        return AndanteState(self.atoms.copy(), self.sigma.copy(), self.next_clause)
    
    def has_atoms(self):
        return len(self.atoms)>0
    
    def next_atom(self):
        self.curr_atom = self.atoms.pop()
        return self.curr_atom
