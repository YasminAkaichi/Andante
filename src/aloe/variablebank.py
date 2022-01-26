from aloe.clause import Clause, Constant, Variable, Operator

def apply_subst(term, subst, deep=False):
    """ 
    Applies variable substitution 'subst' to term 'term'.
    Variables that are not in 'subst' are returned as they are.
    """
    if   isinstance(term, Constant):
        return term
    elif isinstance(term, Variable):
        if term in subst:
            if deep: return apply_subst(subst[term], subst, deep=True)
            else:    return subst[term]
        else:        return term
    elif isinstance(term, Operator):
        f_name = term.name
        f_args = [apply_subst(t, subst, deep=True) for t in f_args]
        return term.__class__(f_name, f_args)


class VariableBank:
    def __init__(self):
        self.variables = set()
        self.count = 0
        self.subst = dict()
                    
    def newVariable(self):
        var = Variable(self.count)
        self.variables.add(var)
        self.count += 1
        return var
    
    def update_subst(self, subst):
        self.subst.update(subst)
        for key, value in self.subst.items():
            self.subst[key] = apply_subst(value, subst, deep=True)
    
    @staticmethod
    def build_from_atom(atom):
        def update_variables(func):
            for term in func:
                if isinstance(term, Variable):
                    vb.variables.add(term)
                elif isinstance(term, Constant):
                    continue
                elif isinstance(term, Operator):
                    update_variables(term)
        vb = VariableBank()
        update_variables(atom)
        return vb

    # Rename variable in ..
    def transform_clause(self, clause, subst=None):
        if subst is None: subst = dict()
        head = self.transform(clause.head, subst)
        body = [self.transform(b, subst) for b in clause.body]
        return Clause(head, body)
    
    def transform(self, term, subst=None):
        """ Transforms Variable, Constant or Operator object """
        if subst is None: subst = dict()
        if isinstance(term, Variable):
            if term in subst:
                return subst[term]
            else:
                var = self.newVariable()
                subst[term] = var
                return var
        elif isinstance(term, Constant):
            return term
        elif isinstance(term, Operator):
            op_args = [self.transform(t, subst) for t in term]
            return term.__class__(term.name, op_args)
        
    def apply_subst(self, term):
        if isinstance(term, Variable):
            if term in self.subst:
                return self.subst[term]
            else:
                return term
        elif isinstance(term, Constant):
            return term
        elif isinstance(term, Operator):
            op_args = [self.apply_subst(t) for t in term]
            return term.__class__(term.name, op_args)
        
    def copy(self):
        vb = VariableBank()
        vb.variables = self.variables.copy()
        vb.count = self.count
        vb.subst = self.subst.copy()
        return vb
    
    def var4skolem(self, skolem):
        """ returns variable corresponding to skolem value 'skolem' """
        if skolem not in self.subst:
            self.subst[skolem] = newVariable
        return self.subst[skolem]