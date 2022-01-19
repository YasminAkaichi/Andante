from aloe.clause import Constant, Variable, Operator

class VariableBank:
    def __init__(self):
        self.variables = set()
        self.count = 0
                    
    def newVariable(self):
        var = Variable(self.count)
        self.variables.add(var)
        self.count += 1
        return var
    
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

    def transform_clause(self, clause, subst=None):
        if subst is None: subst = dict()
        head = self.transform(clause.head, subst)
        body = [self.transform(b, subst) for b in self.body]
        return Clause(head, body)
    
    def transform(self, element, subst=None):
        """ Transforms Variable, Constant or Operator object """
        if subst is None: subst = dict()
        if isinstance(term, Variable):
            if term in subst:
                return subst[term]
            else:
                var = newVariable()
                subst[term] = var
                return var
        elif isinstance(term, Constant):
            return Constant
        elif isinstance(term, Operator):
            op_args = [self.transform(t, subst) for t in term]
            return term.__class__(term.name, op_args)