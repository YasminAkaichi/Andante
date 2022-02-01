from aloe.clause import Clause, Constant, Variable, Function, Literal, Goal, Type
from aloe.exceptions import SubstitutionError

class Substitution:
    """
    This class represents a substitution of variables
    It has three properties:
    - variables: the domain of substitution, a set of Variable objects
    - tally: dict giving for a symbol the number of Variable objects with the symbol
    - subst: dict mapping a Variable object to a term
    """
    def __init__(self):
        self.variables = set()
        self.tally = dict()
        self.subst = dict()
        
    def rename_variables(self, x, subst=None, new_variables=True):
        """ 
        Renames all variables in x. 
        x: Clause, Constant, Type, Variable, Function, Literal or Goal
        subst: prior substitution information
        new_variables: True or False, if True, allows the creation of new variables
        """
        subst = subst if subst is not None else dict()
        if   isinstance(x, Clause):
            renamed_head =  self.rename_variables(x.head, subst, new_variables) if x.head else None
            renamed_body = [self.rename_variables(atom,   subst, new_variables) for atom in x.body]
            return x.__class__(renamed_head, renamed_body)
        elif isinstance(x, Constant):
            return x
        elif isinstance(x, Type):
            return x
        elif isinstance(x, Variable):
            if x in subst: return subst[x]
            else:
                if not new_variables:
                    message = 'New variable needed and new_variables is set to False'
                    raise Exception(message)
                if not x.symbol in self.tally:
                    self.tally[x.symbol] = 0
                var = Variable(x.symbol, self.tally[x.symbol])
                self.variables.add(var)
                self.tally[x.symbol] += 1
                subst[x] = var
                return var
        elif isinstance(x, Function):
            renamed_args = [self.rename_variables(arg, subst, new_variables) for arg in x]
            return x.__class__(x.functor, renamed_args)
        elif isinstance(x, Literal):
            return x.__class__(self.rename_variables(x.atom, subst, new_variables), x.sign)
        elif isinstance(x, Goal):
            return x.__class__([self.rename_variables(lit, subst, new_variables) for lit in x])
        elif isinstance(x, list):
            return [self.rename_variables(e, subst, new_variables) for e in x]
        else: raise NotImplementedError('%s object cannot be renamed for now. (%s)' % (str(x.__class__.__name__), str(x)))

    def copy(self):
        sigma = Substitution()
        sigma.variables = self.variables.copy()
        sigma.tally = self.tally.copy()
        sigma.subst = self.subst.copy()
        return sigma
    
    def __contains__(self, var): return var in self.variables
    def __iter__(self): return iter(self.variables)

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
        If key is not present in the set of variables, throws a KeyError
        If key is not present in the set of substitutions, adds the substitution
        """
        if   key not in self.variables:
            message = str(key)
            raise KeyError(message)
        elif key.is_in(item): 
            raise SubstitutionError(key, item)
        elif key not in self.subst:
            self.subst[key] = item
        else: #key in self.subst
            self.subst[key] = self.unify(self.subst[key],item)
        self.update_everywhere(key)
            
    def unify(self, atom1, atom2):
        """
        Tries to match two atoms together and iteratively updates self.subst
        If not possible, raises a SubstitutionError
        """
        if   isinstance(atom1, Constant) and isinstance(atom2, Constant):
            if atom1!=atom2: raise SubstitutionError(atom1, atom2)
            else: return atom1
        elif isinstance(atom1, Constant) and isinstance(atom2, Function) \
          or isinstance(atom1, Function) and isinstance(atom2, Constant):
            raise SubstitutionError(atom1, atom2)
        elif isinstance(atom1, Function) and isinstance(atom2, Function):
            if atom1.name != atom2.name: #functor or arity unequal
                raise SubstitutionError(atom1, atom2)
            else:
                t = [self.unify(t1,t2) for t1, t2 in zip(atom1, atom2)]
                return atom1.__class__(atom1.functor, t)
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
        
    def update_everywhere(self, var):
        for key in self.subst:
            self.subst[key] = self.replace_var_in_expr(var, self.subst[key])

    def replace_var_in_expr(self, var, expr):
        if   isinstance(expr, Constant): return expr
        elif isinstance(expr, Type):     return expr
        elif isinstance(expr, Variable): return self.subst[var] if expr==var else expr
        elif isinstance(expr, Function):
            t = [self.replace_var_in_expr(var,t) for t in expr]
            return expr.__class__(expr.functor, t)
        else: 
            message = 'CompoundTerm replace_var_in_expr has not been implemented for %s objects' % (expr.__class__.__name__)
            raise NotImplementedError(message)
            
    def apply_subst(self, expr):
        return self.rename_variables(expr, subst=self, new_variables=False)
            
    def __repr__(self):
        return repr(self.subst)
    
    @staticmethod
    def from_mode(M):
        s  = Substitution()
        am = s.rename_variables(M.instantiate())
        s.unify(am, M.atom)
        return s, am
