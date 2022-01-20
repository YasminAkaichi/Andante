from abc import ABC, abstractmethod
from aloe.options import Options
from aloe.variablebank import VariableBank

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
        q: a string, a clause or a list of clauses
        options: parameters for the query, see aloe.query
        """
        assert isinstance(knowledge, Knowledge)
        assert isinstance(q, str) \
            or isinstance(q, Clause) \
            or (isinstance(q, list) and all(isinstance(el, Clause) for el in q))
        if isinstance(q, str):
            pass
        if isinstance(q, Clause):
            q = [q]
        for clause in q:
            if not clause.is_unit():
                message = 'Query not implemented for non unit clauses\nClause: %s' % (clause)
                raise NotImplementedError(message)
            if clause.head:
                atom = clause.head 
                yield (clause, self._query(self, [atom], knowledge))
            else:
                atom = clause.body[0]
                yield (clause, not self._query(self, [atom], knowledge))
            
    def _query(self, atoms, knowledge):
        """ 
        Checks the truth of an atom
        Takes a list of atoms as input
        """
        curr_state = AloeState(atoms)
        states = []
        while curr_state.has_atoms():
            atom = curr_state.next_atom() #
            candidates = knowledge.match(atom)
            if not candidates: return False
            
        
        return True
            
class AloeState:
    def __init__(self, atoms, var_bank=None):
        self.var_bank = var_bank if var_bank is not None else VariableBank.build_from_atom(atoms[0])
        self.atoms = atoms
        
            