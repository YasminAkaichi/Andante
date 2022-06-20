#---------------------------------------------------------------------------------------------------------------#
#                                                    Imports                                                    #
#---------------------------------------------------------------------------------------------------------------#

import re
import bisect 
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from parsimonious.exceptions import ParseError, VisitationError
from aloe.clause    import Clause, Predicate, CompoundTerm, Variable, Constant, Negation, Goal, Type, List
from aloe.clause    import ArithmeticComparison, UnificationComparison, BasicArithmeticExpression, TrigoExpression, Is, ParenthesisArithmeticExpression
from aloe.mode      import ModeCollection, Mode, Modeh, Modeb
from aloe.options   import Options, SystemParameters
from aloe.program   import AloeProgram
from aloe.knowledge import LogicProgram
from aloe.utils     import red
import parser



#---------------------------------------------------------------------------------------------------------------#
#                                                    Grammar                                                    #
#---------------------------------------------------------------------------------------------------------------#

grammar = Grammar(
    r"""    
            #-----------------------------------------------------#
            #                   Basic grammar                     #
            #-----------------------------------------------------#
    
    word      = ~"[a-z]\w*"
    variable  = ~"[A-Z]\w*" ~"\d*"
    number    = float / integer
    integer   = ~"\d+"
    float     = ~"[+-]?(\d*\.\d+)"
    __        = ~"\s*"                                                # Represents whitespaces
    
    
            #-----------------------------------------------------#
            #                 Grammar wrt files                   #
            #-----------------------------------------------------#
            
    aloefile         = __ header? __ background __ pos_ex? __ neg_ex? __
    header           =                       (hclause __)+
    background       = ":-" __ "begin_bg"     __ "." __ (hornclause __)+ __ ":-" __ "end_bg"     __ "."
    pos_ex           = ":-" __ "begin_in_pos" __ "." __ (hornclause __)+ __ ":-" __ "end_in_pos" __ "."
    neg_ex           = ":-" __ "begin_in_neg" __ "." __ (hornclause __)+ __ ":-" __ "end_in_neg" __ "."
    hclause          = mode / determination / set
    determination = "determination" __ "(" __ predname __ "/" __ integer __ ("," __ predname __ "/" __ integer __)+ ")" __ "."    
    set           = "set" __ "(" __ word __ "," __ value __ ")" __ "."
    
    
            #-----------------------------------------------------#
            #              Grammar wrt horn clauses               #
            #-----------------------------------------------------#
    
    hornclause       = headlessclause / definiteclause
    headlessclause   =          ":-" __ body   __ "."
    definiteclause   = head __ (":-" __ body)? __ "."
    head             = atom
    body             = atom __ ("," __ atom __)*
    atom             = "true" / "false" / predicate / comparison / is_evaluation
    predicate        = predname __ "(" __ term __ ("," __ term __)* ")"
    term             = compoundterm / variable / constant 
    compoundterm     = funcname __ "(" __ term __ ("," __ term __)* ")"
    predname         = word
    funcname         = word
    constant         = value  / value
    constant_number  = number / number
    constant_word    = word   / word
    value            = number / word

    list = "[" __ (term __ ("," __ term __)* ("|" __ (variable / list))? )? __ "]" 

            #-----------------------------------------------------#
            #                 Grammar wrt modes                   #
            #-----------------------------------------------------#

    mode      = modeh / modeb
    modeh     = "modeh" __ "(" __ recall __ "," __ matom __ ")" __ "."
    modeb     = "modeb" __ "(" __ recall __ "," __ matom __ ")" __ "."
    recall    = "*" / integer
    matom     = predname __ "(" __ mterm __ ("," __ mterm __)* ")" 
    mcompterm = funcname __ "(" __ mterm __ ("," __ mterm __)* ")"
    mterm     = type / mcompterm / constant
    type      = sign word
    sign      = ~"[+\-#]"
    
    generator = ((mode / determination) __)* (hornclause __)*
    
    
            #-----------------------------------------------------#
            #                Grammar wrt queries                  #
            #-----------------------------------------------------#
    
    query     = goal __ "."
    goal      = goal_unit __ ("," __ goal_unit __)*
    goal_unit = negation / atom
    negation  = "not" __ "(" __ goal __ ")"
    
    
            #-----------------------------------------------------#
            #         Grammar wrt arithmetic operations           #
            #-----------------------------------------------------#
    
    comparison = arithmetic_comparison / unification_comparison
    unification_comparison = term                  __ unification_comparison_symbol __  term
    arithmetic_comparison  = arithmetic_expression __ arithmetic_comparison_symbol  __  arithmetic_expression
    unification_comparison_symbol = '='   / '\='  / '==' / '\==' / '@<' / '@<=' / '@>' / '@>=' 
    arithmetic_comparison_symbol  = '=:=' / '=\=' / '<'  / '<='  / '>'  / '>=' 
    
    arithmetic_expression = in_parenthesis_arithmetic_expression / basic_arithmetic_expression / trigo_expression / arithmetic_atom
    in_parenthesis_arithmetic_expression = '(' __ arithmetic_expression __ ')'
    basic_arithmetic_expression          = arithmetic_atom __ basic_arithmetic_symbol __ arithmetic_expression
    trigo_expression                     = trigo_symbol __ '(' __ arithmetic_expression __ ')'
    arithmetic_atom         = variable / constant_number
    basic_arithmetic_symbol = '**'  / '//'   / '+'    / '-'     / '/'   /  '*'   / 'mod'
    trigo_symbol            = 'sin' / 'sinh' / 'asin' / 'asinh' / 'tan' / 'tanh' / 'atan' / 'atanh' / 'cos' / 'cosh' / 'acos' / 'acosh'
    
    is_evaluation = arithmetic_atom __ 'is' __ arithmetic_expression
    """ 
)



#---------------------------------------------------------------------------------------------------------------#
#                                                    Visitor                                                    #
#---------------------------------------------------------------------------------------------------------------#

class AloeVisitor(NodeVisitor):
    """ 
    Class implementing the tree visitor for the aloe grammar.
    -----------------------------------------------------------
        
    `tree = grammar.parse(text)´ parses the string 'text' in the form of a tree.
       -> This class allows to navigate the tree obtained. 

    `AloeVisitor().visit(tree)´ 
       -- navigates through the parsed tree
       -- transforms it into a Clause object
    
    def visit_x(self, node, visited_children):
       -- with x, a non-terminal symbol
       -- corresponds to a production rule: x -> ...
       Inputs:
          -- visited_children is the list of returned values from each child
              Ex: headlessclause = ":-" body "."
                 visited_children = [[], val_body, []]
                    -- children of ":-" and "." are []
                    -- val_body is the value returned by body
              Special children:
                 -- `x?´ -> [] or [child_x]
                 -- `x*´ -> [child_x1, ..., child_xn]
                 -- `(x y)´ -> [child_x, child_y]
                 -- x / y -> [child_x] or [child_y]
          -- node: the current node from the parsed tree
       Output:
           -- The transformation for symbol x, given the inputs
           
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
    
    def visit_leaf(self, node, visited_children): 
        """ When visiting a leaf, return the text matched by the regex expression """
        return node.text

        
            #-----------------------------------------------------#
            #                   Basic grammar                     #
            #-----------------------------------------------------#
            
    visit_word    = visit_leaf
    visit_number  = visit_choice
    visit_integer = lambda self, node, _: int(  node.text)
    visit_float   = lambda self, node, _: float(node.text)
    
    def visit_variable(self, node, visited_children):
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
    
    def visit_aloefile(self, node, visited_children):
        _, opt_header, _, background, _, opt_pos_ex, _, opt_neg_ex, _ = visited_children
        if opt_header:
            header = opt_header[0]
            modehandler, options = header['modehandler'], header['options']
        else:
            header, modehandler, options = None, None, None
            
        pos_ex = opt_pos_ex[0] if opt_pos_ex else []
        neg_ex = opt_neg_ex[0] if opt_neg_ex else []
        
        program = AloeProgram(options=options, 
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
    visit_background = lambda self, node, visited_children: LogicProgram([c for c, _ in visited_children[6]])
    visit_pos_ex     = lambda self, node, visited_children: [c for c, _ in visited_children[6]]
    visit_neg_ex     = lambda self, node, visited_children: [c for c, _ in visited_children[6]]    
    
    def visit_determination(self, node, visited_children):
        #     determination = "determination(" predname "/" number ("," predname "/" number)+ ")."    
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
    
    def visit_headlessclause(self, node, visited_children):
        _, _, body, _, _ = visited_children
        if len(body)==1:
            return Clause(None, body[0])
        else:
            return Clause(None, body)
    
    def visit_definiteclause(self, node, visited_children):
        head, _, optional_body, _, _ = visited_children
        if optional_body:
            _, _, body = optional_body[0]
            return Clause(head, body)
        else:
            return Clause(head, [])
    
    def visit_body(self, node, visited_children):
        atom1, _, opt_atoms = visited_children
        atoms = [atom1] + [atom for _, _, atom, _ in opt_atoms]
        return atoms
        
    def visit_predicate(self, node, visited_children):
        predname, _, _, _, term1, _, opt_terms, _ = visited_children
        terms = [term1] + [term for _, _, term, _ in opt_terms]
        return Predicate(predname, terms)
    
    def visit_compoundterm(self, node, visited_children):
        funcname, _, _, _, term1, _, opt_terms, _ = visited_children
        terms = [term1] + [term for _, _, term, _ in opt_terms]
        return CompoundTerm(funcname, terms)

    visit_constant = lambda self, *args: Constant(self.visit_choice(*args))    
    visit_constant_number = visit_constant
    visit_constant_word   = visit_constant
    visit_value           = visit_choice
    
    def visit_list(self, node, visited_children):
        """
        list = "[" __ (term __ ("," __ term __)* ("|" __ (variable / list))? )? __ "]" 
        opt1 = term __ ("," __ term __)* ("|" __ (variable / list))? 
        """
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

    def visit_modeh(self, node, visited_children):
        _, _, _, _, recall, _, _, _, atom, _, _, _, _ = visited_children
        return Modeh(recall, atom)

    def visit_modeb(self, node, visited_children):
        _, _, _, _, recall, _, _, _, atom, _, _, _, _ = visited_children
        return Modeb(recall, atom)
    
    def visit_recall(self, node, visited_children):
        if node.text == '*':
            return SystemParameters.max_recall
        else:
            return int(node.text)
    
    visit_matom = visit_predicate
    
    visit_mcompterm = visit_compoundterm
    
    visit_mterm = visit_choice
    
    def visit_type(self, node, visited_children):
        sign, name = visited_children
        return Type(sign, name)
    
    visit_sign = visit_leaf
    
    def visit_generator(self, node, visited_children):
        """ generator = ((mode / determination) __)* (hornclause __)* """
        l_modes, l_clauses = visited_children
        lmodes = [x for (x,), _ in l_modes]
        knowledge = LogicProgram([x for x, _ in l_clauses])
        return knowledge, lmodes

    
            #-----------------------------------------------------#
            #                Grammar wrt queries                  #
            #-----------------------------------------------------#
   
    visit_query = visit_choice

    def visit_goal(self, node, visited_children):
        el0, _, l_e = visited_children
        g = Goal((el0,))
        g.extend(e for _, _, e, _ in l_e)
        return g
    
    visit_goal_unit = visit_choice
    
    def visit_negation(self, node, visited_children):
        _, _, _, _, goal, _, _ = visited_children
        return Negation(goal)
    

            #-----------------------------------------------------#
            #         Grammar wrt arithmetic operations           #
            #-----------------------------------------------------#

    visit_comparison = visit_choice
    
    def visit_arithmetic_comparison(self, node, visited_children):
        expr1, _, symbol, _, expr2 = visited_children
        return ArithmeticComparison(expr1, expr2, symbol)
    
    def visit_unification_comparison(self, node, visited_children):
        expr1, _, symbol, _, expr2 = visited_children
        return UnificationComparison(expr1, expr2, symbol)
        
    visit_arithmetic_comparison_symbol  = visit_leaf
    visit_unification_comparison_symbol = visit_leaf
    
    visit_basic_arithmetic_symbol = visit_leaf
    visit_trigo_symbol      = visit_leaf
    
    visit_arithmetic_expression = visit_choice
    visit_arithmetic_atom       = visit_choice
    
    def visit_basic_arithmetic_expression(self, node, visited_children):
        expr1, _, symbol, _, expr2 = visited_children
        return BasicArithmeticExpression(expr1, expr2, symbol)
    
    def visit_in_parenthesis_arithmetic_expression(self, node, visited_children):
        _, _, expr, _, _ = visited_children
        return ParenthesisArithmeticExpression(expr)
    
    def visit_trigo_expression(self, node, visited_children):
        symbol, _, _, _, expr, _, _ = visited_children
        return TrigoExpression(expr, symbol)
    
    def visit_is_evaluation(self, node, visited_children):
        arg, _, _, _, expr = visited_children
        return Is(arg, expr)
    

    
#---------------------------------------------------------------------------------------------------------------#
#                                                    Parser                                                     #
#---------------------------------------------------------------------------------------------------------------#
    
class AloeParser:
    def __init__(self):
        self.grammar = grammar
        self.visitor = AloeVisitor()

    def parse(self, string, rule='hornclause'):
        """
        Parses input 'string'
        Input: 
            string: either a path to a file or a text to parse
            rule:   rule on which to parse the text
        Ouput: Object from aloe.clause
        """
        string = string.strip()
        
        # Case where string is the path to a file
        try:    
            full_text = open(string, 'r').read()            
            filename  = string
        except: 
            full_text = string
            filename  = ""
            
        text_no_comments = re.sub(r'%.*\n', '\n', full_text)
        
        try:
            tree   = self.grammar[rule].parse(text_no_comments)
            output = self.visitor.visit(tree)
            return output
        except ParseError as e:
            message = 'Failed to parse rule <%s>' % e.expr.as_rule()
            raise SyntaxError(message, (filename, e.line(), e.column(), full_text))
        except VisitationError as e:
            message = 'Error in the code when visiting the parsed tree. This should not happen. Please report it.'
            raise Exception(message)            
        
    def parse_several(self, string, rule='hornclause'):
        """ Parse string <string> containing multiple times the rule <rule> """
        new_rule = 'l_%s' % rule
        if not new_rule in self.grammar:
            rules, _ = self.grammar._expressions_from_rules('%s = (%s __)*' % (new_rule, rule), self.grammar)
            self.grammar.update(rules)
            
            def visit_new_rule(node, visited_children):
                return [child for child, _ in visited_children]
            setattr(self.visitor, 'visit_%s' % new_rule, visit_new_rule) 
        
        return self.parse(string, rule=new_rule)

    def split_on_dots(self, text):
        text = re.sub(r'%.*\n', '\n', text)
        clauses = [c.strip()+'.' for c in text.split('.') if c]
        return clauses