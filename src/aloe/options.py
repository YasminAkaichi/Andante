from dataclasses import dataclass

@dataclass       
class Options(object):
    c       = 2     # Maximal body size for new clauses
    h       = 30    # Maximal depth of deduction
    verbose = 0     # Level of logging output
    solver  = "AloeSolver"
    
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

