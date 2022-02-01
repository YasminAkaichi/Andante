import aloe.solver
import aloe.learner
from aloe.clause    import Goal
from aloe.options   import Options
from aloe.mode      import ModeCollection
from aloe.knowledge import Knowledge, LogicProgram


class AloeProgram:
    def __init__(self, options=None, knowledge=None, modes=None, examples=None):
        """
        Class representing a Aloe program
        Attributes :
            - options:   see aloe.options
            - knowledge: gathers all clauses (aloe.knowledge.Knowledge object)
            - examples:  dictionnary of positive and negative examples 
            - solver:    handles all queries (aloe.solver.Solver object)
            - modes:     assembles modes and determinations (aloe.modes.ModeCollection object)
            - learner:   handles inductive learning (aloe.learner.Learner object) 
            -B: background knowledge
            -E: examples
            -M: modes
            -options: options
        """
        self.options   = options   if options   else Options()
        self.knowledge = knowledge if knowledge else LogicProgram(options=self.options)
        self.solver    = getattr(aloe.solver, self.options.solver)(options=self.options)
        self.modes     = modes     if modes     else ModeCollection(options=self.options)
        self.examples  = examples  if examples  else {'pos':[], 'neg':[]}
        self.learner   = getattr(aloe.learner, self.options.learner)(options=self.options)
        
    @staticmethod
    def build_from_file(filename): 
        import aloe.parser
        return aloe.parser.AloeParser().parse_file(filename)
    
    @staticmethod
    def build_from_text(text): 
        import aloe.parser
        return aloe.parser.AloeParser().parse(text)
        
    def __repr__(self):
        B = repr(self.knowledge)
        E = 'Positive:\n%s\nNegative:\n%s' % ('\n'.join(repr(e) for e in self.examples['pos']),
                                              '\n'.join(repr(e) for e in self.examples['neg']))
        M = repr(self.modes)
        o = repr(self.options)
        return 'Background:\n%s\n\nExamples:\n%s\n\nModes:\n%s\n\noptions:\n%s' % (B,E,M,o)
        
    def query(self, q):
        """
        Launch a query to the aloe solver. 
        The query 'q' can be:
        - a string: the query will then first be parsed and then evaluated
        - a goal
        """
        assert isinstance(q, str) \
            or isinstance(q, Goal)
        if isinstance(q, str):
            if not hasattr(self, 'parser'):
                import aloe.parser
                self.parser = aloe.parser.AloeParser()
            q = self.parser.parse_goal(q)
        return self.solver.query(q, self.knowledge)
        
    def set(self, field, value): self.options[field] = value
        
    def induce(self):
        self.learner.induce(self.examples, self.modes, self.knowledge, self.solver)
        
        
        
        
        