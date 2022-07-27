from aloe.logic_concepts import Function, Constant, Predicate, Variable, Term, Atom, Type
from aloe.utils import generate_variable_names
from aloe.collections  import OrderedSet

class Mode:
    def __init__(self, recall, atom):
        """ Mode as defined in the progol framework 

        Attributes
        ----------
        recall : int 
            The number of times this mode can be used to build new clauses
        atom : aloe.logic_concepts.Atom
            The template of atoms that the mode defines
        """
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
    
    def instantiate(self) -> Predicate:
        """ 
        Instantiates the mode by converting all types (aloe.mode.Type) within 
        its atom to variables (aloe.logic_concepts.Variable).

        Examples
        --------
        mode_str = 'modeh(*, parent(+person, -person))' 
        mode = aloe.parser.parse(mode_str)
        atom = mode.isinstance()
        print(atom)
        > 'parent(A, B)'
        """
        var_names = generate_variable_names()
        def _instantiate(t):
            if   isinstance(t, Constant):
                return t
            elif isinstance(t, Function):
                args = [_instantiate(t_) for t_ in t]
                return t.__class__(t.symbol, args)
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

       
def get_input_name_decorator(input_types = [str]):
    """ Feeds the name of the input to the decorated function """
    transform = (
        (str, lambda x: x),
        (Predicate, lambda x: x.name),
        (Modeh, lambda x: x.atom_name),
        (Modeb, lambda x: x.atom_name), 
    )
    def wrapper(func):
        def func_decorated(self, expr):
            for _class, _fun in transform:
                if isinstance(expr, _class):
                    return func(self, _fun(expr))
            valid_classes = ', '.join([c.__name__ for c, _ in transform if c in input_types])
            message = "Expected input of type: %s, got: %s" % (valid_classes, str(type(expr)))
            raise KeyError(message)
        return func_decorated
    return wrapper

class ModeCollection: # TODO: Change to ModeManager
    def __init__(self, modes=None, determinations=None, options=None):
        """
        Object storing and interacting with all things related to modes 

        Attributes
        ----------
        map_to_modeh : dict
            Maps predicate symbol to modeh (str to aloe.modes.Modeh) 
        map_to_modeb : dict    
            Maps predicate symbol to modeb (str to aloe.modes.Modeb) 
        determinations : dict
            Maps modeh to a list of modeb
        """
        self.modes = modes or []
        determinations = determinations or []
        
        self.map_to_modeh = {mode.atom_name:mode for mode in modes if isinstance(mode, Modeh)}
        self.map_to_modeb = {mode.atom_name:mode for mode in modes if isinstance(mode, Modeb)}

        # determinations is a dict of sets
        # input: f/2 -> {f/2, d/3, k/2}
        self.determinations = dict()
        for (deterh, l_deterb) in determinations:
            for deterb in l_deterb:
                self.add_determination(deterh, deterb)
            
    def add_determination(self, deterh, deterb):
        """ Adds a single determination """
        if deterh not in self.map_to_modeh:
            raise Exception("Determination error: %s does not correspond to any modeh." % (deterh,))
        if deterb not in self.map_to_modeb:
            raise Exception("Determination error: %s does not correspond to any modeb." % (deterb,))
        if not deterh in self.determinations:
            self.determinations[deterh] = OrderedSet()
        self.determinations[deterh].add(deterb)
        
    def add(self, item):
        """ Adds an new item to the manager

        The item can be a aloe.mode.Modeh object, a aloe.mode.Modeb object or 
        it must represent a determination
        """
        if   isinstance(item, Modeh):
            self.map_to_modeh[item.atom_name] = item
        elif isinstance(item, Modeb):
            self.map_to_modeb[item.atom_name] = item
        else: # determination
            deterh, l_deterb = item
            for deterb in l_deterb:
                self.add_determination(deterh, deterb)
                
    def remove(self, item):
        """ Remove a single item from the manager """
        if   isinstance(item, Modeh):
            del self.map_to_modeh[item.atom_name]
        elif isinstance(item, Modeb):
            del self.map_to_modeb[item.atom_name]
        else: # determination
            deterh, l_deterb = item
            for deterb in l_deterb:
                self.determinations[deterh].remove(deterb)
            if not self.determinations[deterh]:
                del self.determinations[deterh]
            
    @get_input_name_decorator(input_types = (Predicate, str))
    def get_modeh(self, name):
        return self.map_to_modeh[name]
    
    @get_input_name_decorator(input_types = (Predicate, str))
    def get_modeb(self, name):
        return self.map_to_modeb[name]    
    
    @get_input_name_decorator(input_types = (Modeh, Predicate, str))
    def get_modeb_from_modeh(self, name):
        if name in self.determinations:
            return [self.map_to_modeb[bname] for bname in self.determinations[name]]
        else:
            return [value for _, value in self.map_to_modeb.items()]
            
    def __repr__(self):
        return 'modeh: %s' % repr(self.map_to_modeh) + \
             '\nmodeb: %s' % repr(self.map_to_modeb) + \
             '\ndeterminations: %s' % repr(self.determinations)

