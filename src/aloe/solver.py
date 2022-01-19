from aloe.program import AloeProgram, LogicProgram
from aloe.options import Options, DefaultOptions
from aloe.variablebank import VariableBank

class AloeSolver:
    def __init__(self, knowledge, options=DefaultOptions):
        assert isinstance(knowledge, (AloeProgram, LogicProgram))
        assert isinstance(knowledge, (AloeProgram, Options))
        self._knowledge = knowledge
        self._options = options

    @property
    def knowledge(self):
        """
        Knowledge can be given either as an AloeProgram or a LogicProgram object
        Retreaving information is made differently in each case
        """
        if isinstance(self._knowledge, AloeProgram):
            return self._knowledge.B
        else:
            return self._knowledge
        
    @property
    def options(self):
        """
        Options can be given either as an AloeProgram or an Options object
        Accessing options is made differently in each case
        """
        if isinstance(self._options, AloeProgram):
            return self._options.options
        else:
            return self._options
        
    def query(self, q, **options):
        """
        Launch a query
        Input: 
        q: a clause or a list of clauses
        options: parameters for the query, see aloe.query
        """
        assert isinstance(q, Clause) or (isinstance(q, list) and all(isinstance(el, Clause) for el in q))
        if isinstance(q, Clause):
            q = [q]
        for clause in q:
            if not clause.is_unit():
                message = 'Query not implemented for non unit clauses\nClause: %s' % (clause)
                raise NotImplementedError(message)
            if clause.head:
                atom = clause.head 
                yield (clause, self._query(self, [atom]))
            else:
                atom = clause.body[0]
                yield (clause, not self._query(self, [atom]))
            
    def _query(self, atoms):
        """ 
        Checks the truth of an atom
        Takes a list of atoms as input
        """
        curr_state = AloeState(atoms)
        states = []
        while atoms:
            atom = atoms.pop() #
            
class AloeState:
    def __init__(self, atoms, var_bank=None):
        self.var_bank = var_bank if var_bank is not None else VariableBank.build_from_atom(atoms[0])
        self.atoms = atoms
        
            