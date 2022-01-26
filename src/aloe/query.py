from aloe.clause import Constant, Variable, Operator

# Matching 2 atoms
# unify atom1 with atom2, the head of a clause
def learn_subst(atom1, atom2):    
    """
    Tries to match two atoms together and returns the corresponding substitution.
    If not possible, returns None.
    """
    if   isinstance(atom1, Constant) and isinstance(atom2, Constant):
        if atom1 == atom2:
            return {}
        else:
            return None
    elif isinstance(atom1, Constant) and isinstance(atom2, Operator) \
      or isinstance(atom1, Operator) and isinstance(atom2, Constant):
        return None
    elif isinstance(atom1, Operator) and isinstance(atom2, Operator):
        if atom1.name != atom2.name or atom1.arity != atom2.arity:
            return None
        else:
            subst = dict()
            terms1, terms2 = atom1.terms.copy(), atom2.terms.copy()
            for term1, term2 in zip(terms1, terms2):
                s = learn_subst(term1, term2)
                if s is None:
                    return None
                for var, term in s.items():
                    if var in subst:
                        terms1.append(term)
                        terms2.append(subst[var])
                    else:
                        subst[var] = term
            return subst
    elif isinstance(atom1, Variable) and isinstance(atom2, (Constant, Operator)):
        return {atom1:atom2}
    elif isinstance(atom1, (Constant, Variable, Operator)) and isinstance(atom2, Variable):
        return {atom2:atom1}
    else:
        message = "Either %s or %s isn't a Constant, Variable or Operator object"
        raise TypeError(message)

def _apply_subst(term, subst):
    """ 
    Applies variable substitution 'subst' to term 'term'.
    Variables that are not in 'subst' are returned as they are.
    """
    if   isinstance(term, Constant):
        return term
    elif isinstance(term, Variable):
        if term in subst:
            return subst[term]
        else:
            return term
    elif isinstance(term, Operator):
        f_name = term.name
        f_args = [_apply_subst(t, subst) for t in f_args]
        return term.__class__(f_name, f_args)
        
def _var_in_term(var, term):
    """ Checks whether variable 'var' can be found in term 'term' """
    if   isinstance(term, Constant):
        return False
    elif isinstance(term, Variable):
        return term==var
    elif isinstance(term, Operator):
        return any([_var_in_term(var,t) for t in term])

#     
def unify(subst):
    """ 
    Procedes to the unification of substitution. 
    In the case that such a substitution is not valid, None is returned. 
    """
    new_subst = dict()
    for var, term in subst.items():
        n_term = _apply_subst(term, new_subst)
        if _var_in_term(var, n_term): # Fail to unify
            return None
        new_subst[var] = n_term        
    return new_subst


