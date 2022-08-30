"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.
"""

from parsimonious.nodes import NodeVisitor

from andante.logic_concepts import (
    Clause, 
    Predicate, 
    CompoundTerm, 
    Variable,
    Constant, 
    Negation, 
    Goal, 
    Type, 
    List,
)
from andante.mathematical_expressions import (
    ArithmeticComparison, 
    UnificationComparison, 
    BasicArithmeticExpression, 
    TrigoExpression, 
    Is, 
    ParenthesisArithmeticExpression,
)
from andante.mode      import (
    ModeCollection, 
    Mode, 
    Modeh, 
    Modeb,
)
from andante.options   import (
    Options, 
    SystemParameters,
)
from andante.program   import AndanteProgram
from andante.knowledge import TreeShapedKnowledge


class Visitor(NodeVisitor):
    """ Grammar tree visitor for andante.grammar.GRAMMAR

    This class is used conjointly with the andante.grammar.GRAMMAR to parse some text.
        tree = andante.grammar.GRAMMAR.parse(text)                 # Reads the input string and outputs a tree
        obj  = andante.grammar_tree_visitor.Visitor().visit(tree)  # Navigates the tree and outputs a useable object
    
    Methods
    -------
    visit_myrule(node, visited_children)
        Visits one node of the parse tree that corresponds to some grammatical rule

        Parameters
        ----------
        node
            The node we're visiting
        visited_children
            The results of visiting the children of that node, in a list           
    """
    
    
            #-----------------------------------------------------#
            #                  Generic visits                     #
            #-----------------------------------------------------#
            
    def generic_visit(self, node, visited_children):
        """ The default visit method. """
        return visited_children or node.text
    
    def visit_choice(self, node, visited_children): 
        """ When visiting a choice, return the only element in visited_children """
        choice, = visited_children
        return choice
    
    def visit_leaf(self, node, visited_children) -> str: 
        """ When visiting a leaf, return the text matched by the regex expression """
        return node.text

        
            #-----------------------------------------------------#
            #                   Basic grammar                     #
            #-----------------------------------------------------#
            
    visit_word    = visit_leaf
    visit_number  = visit_choice
    visit_integer = lambda self, node, _: int(  node.text)
    visit_float   = lambda self, node, _: float(node.text)
    
    def visit_variable(self, node, visited_children) -> Variable:
        symbol_node, tally_node = node.children
        symbol = symbol_node.text
        if tally_node.text:
            tally_id = int(tally_node.text)
        else:
            tally_id = 0
        return Variable(symbol, tally_id)

    
            #-----------------------------------------------------#
            #                 Grammar wrt files                   #
            #-----------------------------------------------------#
    
    def visit_andantefile(self, node, visited_children) -> AndanteProgram:
        _, opt_header, _, background, _, opt_pos_ex, _, opt_neg_ex, _ = visited_children
        if opt_header:
            header = opt_header[0]
            modehandler, options = header['modehandler'], header['options']
        else:
            header, modehandler, options = None, None, None
            
        pos_ex = opt_pos_ex[0] if opt_pos_ex else []
        neg_ex = opt_neg_ex[0] if opt_neg_ex else []
        
        program = AndanteProgram(options=options, 
                              knowledge=background, 
                              modes=modehandler, 
                              examples={'pos':pos_ex,'neg':neg_ex})
        return program
    
    def visit_header(self, node, visited_children):
        header = {'mode':list(), 'determination':list(), 'set':list()}
        for node_child, (visited_child, _) in zip(node, visited_children):
            header[node_child.children[0].children[0].expr_name].append(visited_child)
            
        mhandler = ModeCollection(header['mode'], header['determination'])
        options  = Options(header['set'])
        return {'modehandler':mhandler, 'options':options}
        
    visit_hclause    = visit_choice
    visit_background = lambda self, node, visited_children: TreeShapedKnowledge([c for c, _ in visited_children[6]])
    visit_pos_ex     = lambda self, node, visited_children: [c for c, _ in visited_children[6]]
    visit_neg_ex     = lambda self, node, visited_children: [c for c, _ in visited_children[6]]    
    
    def visit_determination(self, node, visited_children):
        _, _, _, _, modeh_name, _, _, _, modeh_nargs, _, l_modeb, _, _, _ = visited_children
        deterh = '%s/%d'%(modeh_name, modeh_nargs)
        l_deterb = ['%s/%d'%(modeb_name, modeb_nargs) for _, _, modeb_name, _, _, _, modeb_nargs, _ in l_modeb]
        return (deterh, l_deterb)
        
    def visit_set(self, node, visited_children):
        _, _, _, _, attr, _, _, _, value, _, _, _, _ = visited_children
        return (attr, value)
     
    
            #-----------------------------------------------------#
            #              Grammar wrt horn clauses               #
            #-----------------------------------------------------#
    
    visit_hornclause = visit_choice
    visit_atom       = visit_choice
    visit_term       = visit_choice
    
    def visit_headlessclause(self, node, visited_children) -> Clause:
        _, _, body, _, _ = visited_children
        if len(body)==1:
            return Clause(None, body[0])
        else:
            return Clause(None, body)
    
    def visit_definiteclause(self, node, visited_children) -> Clause: 
        head, _, optional_body, _, _ = visited_children 
        if optional_body: 
            _, _, body = optional_body[0] 
            return Clause(head, body) 
        else: 
            return Clause(head, [])

    def visit_body(self, node, visited_children) -> list:
        atom1, _, opt_atoms = visited_children
        atoms = [atom1] + [atom for _, _, atom, _ in opt_atoms]
        return atoms
        
    def visit_predicate(self, node, visited_children) -> Predicate:
        predname, _, _, _, term1, _, opt_terms, _ = visited_children
        terms = [term1] + [term for _, _, term, _ in opt_terms]
        return Predicate(predname, terms)
    
    def visit_compoundterm(self, node, visited_children) -> CompoundTerm:
        funcname, _, _, _, term1, _, opt_terms, _ = visited_children
        terms = [term1] + [term for _, _, term, _ in opt_terms]
        return CompoundTerm(funcname, terms)

    visit_constant = lambda self, *args: Constant(self.visit_choice(*args))    
    visit_constant_number = visit_constant
    visit_constant_word   = visit_constant
    visit_value           = visit_choice
    
    def visit_list(self, node, visited_children) -> List:
        _, _, opt1, _, _ = visited_children
        if not opt1:
            return List([])
        t0, _, l_t, opt2 = opt1[0]
        elements1 = [t0] + [t for _, _, t, _ in l_t]
        if not opt2:
            elements2 = None
        else:
            _, _, (elements2, ) = opt2[0]
        return List(elements1, elements2)
        
        
        
            #-----------------------------------------------------#
            #                 Grammar wrt modes                   #
            #-----------------------------------------------------#
    
    
    # 2. For modes    
    visit_mode = visit_choice

    def visit_modeh(self, node, visited_children) -> Modeh:
        _, _, _, _, recall, _, _, _, atom, _, _, _, _ = visited_children
        return Modeh(recall, atom)

    def visit_modeb(self, node, visited_children) -> Modeb:
        _, _, _, _, recall, _, _, _, atom, _, _, _, _ = visited_children
        return Modeb(recall, atom)
    
    def visit_recall(self, node, visited_children) -> int:
        if node.text == '*':
            return SystemParameters.max_recall
        else:
            return int(node.text)
    
    visit_matom = visit_predicate
    
    visit_mcompterm = visit_compoundterm
    
    visit_mterm = visit_choice
    
    def visit_type(self, node, visited_children) -> Type:
        sign, name = visited_children
        return Type(sign, name)
    
    visit_sign = visit_leaf
    
    def visit_generator(self, node, visited_children):
        l_modes, l_clauses = visited_children
        lmodes = [x for (x,), _ in l_modes]
        knowledge = TreeShapedKnowledge([x for x, _ in l_clauses])
        return knowledge, lmodes

    
            #-----------------------------------------------------#
            #                Grammar wrt queries                  #
            #-----------------------------------------------------#
   
    def visit_query(self, node, visited_children) -> Goal:
        goal, _, _ = visited_children
        return goal

    def visit_goal(self, node, visited_children) -> Goal:
        el0, _, l_e = visited_children
        g = Goal((el0,))
        g.extend(e for _, _, e, _ in l_e)
        return g
    
    visit_goal_unit = visit_choice
    
    def visit_negation(self, node, visited_children) -> Negation:
        _, _, _, _, goal, _, _ = visited_children
        return Negation(goal)
    

            #-----------------------------------------------------#
            #         Grammar wrt arithmetic operations           #
            #-----------------------------------------------------#

    visit_comparison = visit_choice
    
    def visit_arithmetic_comparison(self, node, visited_children) -> ArithmeticComparison:
        expr1, _, symbol, _, expr2 = visited_children
        return ArithmeticComparison(expr1, expr2, symbol)
    
    def visit_unification_comparison(self, node, visited_children) -> UnificationComparison:
        expr1, _, symbol, _, expr2 = visited_children
        return UnificationComparison(expr1, expr2, symbol)
        
    visit_arithmetic_comparison_symbol  = visit_leaf
    visit_unification_comparison_symbol = visit_leaf
    
    visit_basic_arithmetic_symbol = visit_leaf
    visit_trigo_symbol      = visit_leaf
    
    visit_arithmetic_expression = visit_choice
    visit_arithmetic_atom       = visit_choice
    
    def visit_basic_arithmetic_expression(self, node, visited_children) -> BasicArithmeticExpression:
        expr1, _, symbol, _, expr2 = visited_children
        return BasicArithmeticExpression(expr1, expr2, symbol)
    
    def visit_in_parenthesis_arithmetic_expression(self, node, visited_children) -> ParenthesisArithmeticExpression:
        _, _, expr, _, _ = visited_children
        return ParenthesisArithmeticExpression(expr)
    
    def visit_trigo_expression(self, node, visited_children) -> TrigoExpression:
        symbol, _, _, _, expr, _, _ = visited_children
        return TrigoExpression(expr, symbol)
    
    def visit_is_evaluation(self, node, visited_children) -> Is:
        arg, _, _, _, expr = visited_children
        return Is(arg, expr)
    
