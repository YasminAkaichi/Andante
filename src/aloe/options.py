from dataclasses import dataclass

class SystemParameters:
    max_recall = 100 # value from Progol (p.4 from tutorial4.4.pdf)
    maxclauses = 100 # Maximum number of clause learned when inducing
    generic_name_for_variable = True

@dataclass       
class Options(object):
    i       = 2
    c       = 2     # Maximal body size for new clauses
    h       = 30    # Maximal depth of deduction
    verbose = 0     # Level of logging output
    solver  = "AloeSolver"
    
    # Learning Options
    learner = "ProgolLearner"
    hmetric = "FnMetric"
    
    def __init__(self, options=[]):
        # Here we introduce the user's options
        if isinstance(options, dict): 
            options = options.items()
        for attr, value in options:
            setattr(self, attr, value)
            
    def __setattr__(self, attr, value):
        if attr in Options.__dict__:
            super().__setattr__(attr, value)
        else:
            message = "aloe.options.Options object has no attribute '%s'" % (attr)
            raise AttributeError(message)
            
    def __repr__(self):
        return '\n'.join(['%s: %s' % (attr, str(getattr(self, attr))) for attr in self.__dir__() if attr[:1]!='_'])

    def __setitem__(self, key, value): setattr(self, key, value)
        
    def __getitem__(self, key): return getattr(self, key)
    