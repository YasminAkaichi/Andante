from abc import ABC
from dataclasses import dataclass
import copy

class SystemParameters:
    max_recall = 100 # value from Progol (p.4 from tutorial4.4.pdf)
    maxclauses = 100 # Maximum number of clause learned when inducing
    generic_name_for_variable = True

@dataclass       
class Options(object):
    i       = 2
    c       = 2        # Maximal body size for new clauses
    h       = 10000    # Maximal depth of deduction
    verbose = 0        # Level of logging output
    solver  = "AndanteSolver"
    
    # Learning Options
    learner = "ProgolLearner"
    hmetric = "FnMetric"
    update_knowledge = True
    
    logging = False
    
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
            message = "andante.options.Options object has no attribute '%s'" % (attr)
            raise AttributeError(message)
            
    def __repr__(self):
        return '\n'.join(['%s: %s' % (attr, str(getattr(self, attr))) for attr in self])

    def __setitem__(self, key, value): setattr(self, key, value)        
    def __getitem__(self, key): return getattr(self, key)    
    def copy(self): return copy.copy(self)
    
    def __iter__(self):
        for attr in self.__dir__():
            if attr[:1]!='_' and attr!='copy':
                yield attr
    
    
class ObjectWithTemporaryOptions(ABC):
    def __init__(self, options=None):
        assert isinstance(options, Options) or options is None
        super().__init__()
        self._options = options if options else Options()
        self._temp_options = None
        self._revert_temp_options = []
        
    def add_temporary_options(self, **options):
        revert_options = dict()
        if options:
            if not self._temp_options:
                self._temp_options = self._options.copy()
            for attr, value in options.items():
                revert_options[attr] = getattr(self._temp_options, attr)
                setattr(self._temp_options, attr, value)
        self._revert_temp_options.append(revert_options)
    
    def rem_temporary_options(self):
        if len(self._revert_temp_options)<1:
            message = 'self._revert_temp_options is empty'
            raise Exception(message)
        revert_options = self._revert_temp_options.pop()
        if len(self._revert_temp_options)==0:
            self._temp_options = None
        else:
            for attr, value in revert_options.items():
                setattr(self._temp_options, attr, value)
    
    @property
    def options(self):
        if self._temp_options is None:
            return self._options
        else:
            return self._temp_options
        
    def verboseprint(self, *args, **kwargs):
        if self.options.verbose>0: print(*args, **kwargs)


            
