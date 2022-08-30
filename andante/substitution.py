from andante.logic_concepts import Clause, Constant, Variable, Function, Goal, Type, extract_variables
from andante.utils import generate_variable_names, multiple_replace
import re

class SubstitutionError(Exception):
    def __init__(self, key, item):
        message = 'Substitution {%s/%s} is not valid' % (str(key), str(item))
        super().__init__(message)

class Substitution:
    """ Substitution as defined in first order logic

    Attributes
    ----------
    variables : set of andante.logic_concepts.Variable
        The domain of substitution
    tally : dict of int
        Gives for a variable symbol, the highest tally number
    subst : dict of andante.logic_concepts.Term
        Mapping of variables to terms
    """
    def __init__(self):
        self.variables = set()
        self.tally = dict()
        self.subst = dict()
        
        from andante.parser import Parser
        self.parser = Parser()
        
    def items(self): return self.subst.items()
        
    def new_variable(self, symbol):
        """ Creates a new variable that has some input symbol """
        if symbol not in self.tally:
            self.tally[symbol] = 0
            
        while True:
            var = Variable(symbol, self.tally[symbol])
            if var not in self.variables:
                break
            self.tally[symbol] += 1
            
        self.variables.add(var)
        self.tally[symbol] += 1
        return var
            
    def add_variable(self, variable):
        """ Adds a single variable to the domain of the substitution """
        self.add_variables(variable)
                
    def add_variables(self, expr):
        """ Adds all variables present in some expression to the domain of substitution """
        self.variables.update(extract_variables(expr))
        
    def rename_variables(self, x, subst=None, new_variables=True):
        """ Rename all variables by mapping to an already existing substitution or by introducing new variables """
        subst = subst if subst is not None else dict()
        
        def fun(expr):
            if   isinstance(expr, (Constant, Type)):
                return expr
            elif isinstance(expr, Variable):
                if expr in subst: return subst[expr]
                else:
                    if not new_variables:
                        message = 'New variable needed and new_variables is set to False'
                        raise Exception(message)
                    var = self.new_variable(expr.symbol)
                    subst[expr] = var
                    return var
                    
            else: 
                raise NotImplementedError('%s object cannot be renamed for now. (%s)' % (str(expr.__class__.__name__), str(expr)))
                
        return x.apply(fun)
        
    def copy(self):
        """ Returns a deep copy of itself """
        sigma = Substitution()
        sigma.variables = self.variables.copy()
        sigma.tally = self.tally.copy()
        sigma.subst = self.subst.copy()
        return sigma
    
    def __contains__(self, var): return var in self.variables
    def __iter__(self):          return iter(self.variables)
    def __repr__(self):          return repr(self.subst)

    def __getitem__(self, key):
        if   key not in self.variables:
            message = str(key)
            raise KeyError(message)
        elif key in self.subst:
            return self.subst[key]
        else:
            return key
        
    def __setitem__(self, key, item):
        """ 
        Considers the substitution {key/item}

        Raises
        ------
        KeyError
            If the key is not present in the set of variables
        """
        if   key not in self.variables:
            message = str(key)
            raise KeyError(message)
        elif key == item:
            return
        elif key.is_in(item): 
            raise SubstitutionError(key, item)
        elif key not in self.subst:
            self.subst[key] = item
        else: #key in self.subst
            self.subst[key] = self.unify(self.subst[key],item)

        for key in self.subst:
            self.subst[key] = self.substitute(self.subst[key])

    def unify(self, atom1, atom2):
        """
        Tries to match two expressions together and iteratively updates self.subst

        Raises
        ------
        SubstitutionError
            If unification impossible
        """
        if   isinstance(atom1, Constant) and isinstance(atom2, Constant):
            if atom1!=atom2: raise SubstitutionError(atom1, atom2)
            else: return atom1
        elif isinstance(atom1, Constant) and isinstance(atom2, Function) \
          or isinstance(atom1, Function) and isinstance(atom2, Constant):
            raise SubstitutionError(atom1, atom2)
        elif isinstance(atom1, Function) and isinstance(atom2, Function):
            if atom1.name != atom2.name: #symbol or arity unequal
                raise SubstitutionError(atom1, atom2)
            else:
                t = [self.unify(t1,t2) for t1, t2 in zip(atom1, atom2)]
                return atom1.__class__(atom1.symbol, t)
        elif isinstance(atom1, Variable) and isinstance(atom2, (Constant, Function)):
            self[atom1] = atom2
            return self[atom1]
        elif isinstance(atom1, (Constant, Variable, Function)) and isinstance(atom2, Variable):
            self[atom2] = atom1
            return self[atom2]
        elif isinstance(atom1, Type):
            if   isinstance(atom2, (Constant, Function)): raise SubstitutionError(atom1, atom2)
            elif isinstance(atom2, Variable): 
                self[atom2] = atom1
                return atom1
        elif isinstance(atom2, Type):
            return self.unify(atom2, atom1)
        else:
            message = "Either %s or %s isn't a Constant, Variable or Function object"
            raise TypeError(message)
            
    def substitute(self, expr):
        """ Applies the substitution to some expression """
        def fun(el):
            if isinstance(el, Variable):   return self[el]
            else:                          return el
        return expr.apply(fun)
            
    def get_type_subst(self, atom, M, body_atom=False):
        if body_atom:
            m = M.get_modeb(atom)        
        else:
            m = M.get_modeh(atom)
        type_subst = self.copy()
        type_subst.unify(atom, m.atom)
        return type_subst
    
    @staticmethod
    def from_mode(M):
        s  = Substitution()
        am = s.rename_variables(M.instantiate())
        s.unify(am, M.atom)
        return s, am

    @staticmethod
    def generic_name_for_variables(expr):
        subst = dict()
        var_names = generate_variable_names()
        def fun(element):
            if isinstance(element, Variable):
                if element not in subst:
                    subst[element] = Variable(next(var_names))
                return subst[element]
            else:
                return element
        return expr.apply(fun)
    
    def remove_excess_variables(self, domain):
        """ Returns a substitution with its variables restrained to some input domain """
        # Subst: maps from old variables to new ones
        s = Substitution()
        s.add_variables(domain)
        for key in self.subst:
            if key in domain:
                s.add_variables(self[key])
                s.subst[key] = self[key]
        return s