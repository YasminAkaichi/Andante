# aloe.query
# Matching 2 atoms
CST, VAR, FUN = Constant.__name__, Variable.__name__, Function.__name__
def match(atom1, atom2):    
    """
    Tries to match two atoms together and returns the corresponding substitution.
    If not possible, returns None.
    """
    classes = atom1.__class__, atom2.__class__
    if   classes == (CST, CST):
        if atom1 == atom2:
            return {}
        else:
            return None
    elif classes in [(FUN, CST), (CST, FUN)]:
        return None
    elif classes == (FUN, FUN):
        if atom1.name != atom2.name or atom1.arity != atom2.arity:
            return None
        else:
            subst = dict()
            terms1, terms2 = atom1.terms.copy(), atoms2.terms.copy()
            for term1, term2 in zip(terms1, terms2):
                s = match(term1, term2)
                if s is None:
                    return None
                for var, term in s:
                    if var in subst:
                        term1.append(term)
                        term2.append(subst[var])
                    else:
                        subst[var] = term
            return subst
    elif classes in [(VAR, CST), (VAR, FUN)]:
        return {atom1:atom2}
    elif classes in [(CST, VAR), (VAR, VAR), (FUN, VAR)]:
        return {atom2:atom1}

def apply_subst(term, subst):
    """ 
    Applies variable substitution 'subst' to term 'term'.
    Variables that are not in 'subst' are returned as they are.
    """
    term_class = term.__class__
    if   term_class == CST:
        return term
    elif term_class == VAR:
        if term in subst:
            return subst[term]
        else:
            return term
    elif term_class == FUN:
        f_name = term.name
        f_args = [apply_subst(t, subst) for t in f_args]
        return Function(f_name, f_args)
        
def var_in_term(var, term):
    """ Checks whether variable 'var' can be found in term 'term' """
    term_class = term.__class__
    if   term_class == CST:
        return False
    elif term_class == VAR:
        return term==var
    elif term_class == FUN:
        return any([var_in_term(var,t) for t in term])
    
def unify(subst):
    """ 
    Procedes to the unification of substitution. 
    In the case that such a substitution is not valid, None is returned. 
    """
    new_subst = dict()
    for var, term in subst:
        n_term = apply_subst(term, new_subst)
        if var_in_term(var, n_term): # Fail to unify
            return None
        new_subst[var] = n_term
    return new_subst