from aloe.clause import Function, Constant, Variable, Term, Atom, Type
from aloe.utils import generate_variable_names
from aloe.collections  import OrderedSet

class ModeCollection:
    def __init__(self, modes=None, determinations=None, options=None):
        """
        Inputs:
            -modes: list of all modes
            -determinations: dict: modeh -> list of modeb
        """
        modes = modes or []
        determinations = determinations or []
        
        self.modeh = {mode.atom_name:mode for mode in modes if isinstance(mode, Modeh)}
        self.modeb = {mode.atom_name:mode for mode in modes if isinstance(mode, Modeb)}

        # determinations is a dict of sets
        # input: f/2 -> {f/2, d/3, k/2}
        self.determinations = dict()
        for (deterh, l_deterb) in determinations:
            for deterb in l_deterb:
                self.add_determination(deterh, deterb)
            
    def add_determination(self, deterh, deterb):
        if deterh not in self.modeh:
            raise Exception("Determination error: %s does not correspond to any modeh." % (deterh,))
        if deterb not in self.modeb:
            raise Exception("Determination error: %s does not correspond to any modeb." % (deterb,))
        if not deterh in self.determinations:
            self.determinations[deterh] = OrderedSet()
        self.determinations[deterh].add(deterb)
        
    def add(self, item):
        if   isinstance(item, Modeh):
            self.modeh[item.atom_name]=item
        elif isinstance(item, Modeb):
            self.modeb[item.atom_name]=item
        else: # determination
            deterh, l_deterb = item
            for deterb in l_deterb:
                self.add_determination(deterh, deterb)
                
    def remove(self, item):
        if   isinstance(item, Modeh):
            del self.modeh[item.atom_name]
        elif isinstance(item, Modeb):
            del self.modeb[item.atom_name]
        else: # determination
            deterh, l_deterb = item
            for deterb in l_deterb:
                self.determinations[deterh].remove(deterb)
            if not self.determinations[deterh]:
                del self.determinations[deterh]
            
    def get_modeh(self, expr):
        if   isinstance(expr, Atom):
            name = expr.name
        elif isinstance(expr, str):
            name = expr
        else:
            raise KeyError(expr)
        
        return self.modeh[name]
    
    def get_modeb(self, expr):
        if   isinstance(expr, Atom):
            name = expr.name
        elif isinstance(expr, str):
            name = expr
        else:
            raise KeyError(expr)
        
        return self.modeb[name]    
        
    def get_modeb_from_modeh(self, expr):
        if   isinstance(expr, Modeh):
            name = expr.atom_name
        elif isinstance(expr, Atom):
            name = expr.name
        elif isinstance(expr, str):
            name = expr
        else:
            raise KeyError(expr)
            
        if name in self.determinations:
            return [self.modeb[bname] for bname in self.determinations[name]]
        else:
            return [value for _, value in self.modeb.items()]
            
    def __repr__(self):
        return 'modeh: %s' % repr(self.modeh) + \
             '\nmodeb: %s' % repr(self.modeb) + \
             '\ndeterminations: %s' % repr(self.determinations)

class Mode:
    def __init__(self, recall, atom):
        self.recall = recall
        self.atom   = atom
    
    @property
    def atom_arity(self):
        return self.atom.arity
    
    @property
    def atom_name(self):
        """ 
        Determination form of a mode
        Ex: Input: modeh(*,parent_of(+person,-person)) (as a Mode object)
            Ouput: 'parent_of/2' (string)
        """
        return self.atom.name
    
    def instantiate(self):
        var_names = generate_variable_names()
        def _instantiate(t):
            if   isinstance(t, Constant):
                return t
            elif isinstance(t, Function):
                args = [_instantiate(t_) for t_ in t]
                return t.__class__(t.functor, args)
            elif isinstance(t, Type):
                var_name = next(var_names)
                return Variable(var_name)
            else: raise KeyError(t)
        return _instantiate(self.atom)
        
class Modeh(Mode):
    def __repr__(self):
        return 'modeh(%s,%s).' % (repr(self.recall), repr(self.atom))
class Modeb(Mode):
    def __repr__(self):
        return 'modeb(%s,%s).' % (repr(self.recall), repr(self.atom))

       