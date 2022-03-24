import re
import bisect 
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from parsimonious.exceptions import ParseError, VisitationError
from aloe.clause    import Clause, Predicate, CompoundTerm, Variable, Constant, Negation, Goal, Type
from aloe.clause    import Not, Any, All, Comparison, Assignment, Expression
from aloe.mode      import ModeCollection, Mode, Modeh, Modeb
from aloe.options   import Options, SystemParameters
from aloe.program   import AloeProgram
from aloe.knowledge import LogicProgram
from aloe.utils     import red
import parser

grammar = Grammar(
    r"""    
    aloefile         = ws header? ws background ws pos_ex? ws neg_ex? ws
    header           =                       (hclause ws)+
    background       = ":-" ws "begin_bg"     ws "." ws (bclause ws)+ ws ":-" ws "end_bg" ws "."
    pos_ex           = ":-" ws "begin_in_pos" ws "." ws (pclause ws)+ ws ":-" ws "end_in_pos" ws "."
    neg_ex           = ":-" ws "begin_in_neg" ws "." ws (nclause ws)+ ws ":-" ws "end_in_neg" ws "."
    hclause          = mode / determination / set
    bclause          = hornclause
    pclause          = hornclause
    nclause          = hornclause
    ws = ~"\s*"

    determination = "determination" ws "(" ws predname ws "/" ws number ws ("," ws predname ws "/" ws number ws)+ ")" ws "."    
    set           = "set" ws "(" ws word ws "," ws value ws ")" ws "."
    
    hornclause       = headlessclause / definiteclause
    headlessclause   =          ":-" ws body   ws "."
    definiteclause   = head ws (":-" ws body)? ws "."
    head             = atom
    body             = atom ws ("," ws atom ws)*
    atom             = "true" / "false" / predicate / statement
    predicate        = predname ws "(" ws term ws ("," ws term ws)* ")"
    term             = compoundterm / variable / constant 
    compoundterm     = funcname ws "(" ws term ws ("," ws term ws)* ")"
    predname         = word
    funcname         = word
    constant         = value / value
    value            = number / word
    word             = ~"[a-z]\w*"
    variable         = ~"[A-Z]\w*"
    number           = ~"\d+"

    mode      = modeh / modeb
    modeh     = "modeh" ws "(" ws recall ws "," ws matom ws ")" ws "."
    modeb     = "modeb" ws "(" ws recall ws "," ws matom ws ")" ws "."
    recall    = "*" / number
    matom     = predname ws "(" ws mterm ws ("," ws mterm ws)* ")" 
    mcompterm = funcname ws "(" ws mterm ws ("," ws mterm ws)* ")"
    mterm     = type / mcompterm / constant
    type      = sign word
    sign      = ~"[+\-#]"
    
    query     = goal ws "."
    goal      = goal_unit ws ("," ws goal_unit ws)*
    goal_unit = negation / atom
    negation  = "not" ws "(" ws goal ws ")"
    
    generator = (modee ws)* (hornclause ws)*
    modee = "mode" ws atom "."
    
    statement        = not_statement / combi_statement / assignment / comparison 
    not_statement    = "not" ws "(" ws statement ws ")"
    combi_statement  = ("all" / "any") ws "(" ws statement ws ("," ws statement ws)+ ")"
    comparison       = expression ws comparison_symbol ws expression
    comparison_symbol = "<" / ">" / "=<" / "=>" / "!=" / "=="
    assignment       = variable ws "=" ws expression
    expression       = ~"[^<>=!,\.\)]*"    
    """ 
)

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
    # 0. In general
    def generic_visit(self, node, visited_children):
        """ The default visit method. """
        return visited_children
    
    # 1. For clauses
    def visit_hornclause(self, node, visited_children):
        return visited_children[0]
    
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
    
    def visit_atom(self, node, visited_children):
        return visited_children[0]
    
    def visit_predicate(self, node, visited_children):
        predname, _, _, _, term1, _, opt_terms, _ = visited_children
        terms = [term1] + [term for _, _, term, _ in opt_terms]
        return Predicate(predname, terms)
    
    def visit_compoundterm(self, node, visited_children):
        funcname, _, _, _, term1, _, opt_terms, _ = visited_children
        terms = [term1] + [term for _, _, term, _ in opt_terms]
        return CompoundTerm(funcname, terms)
    
    def visit_term(self, node, visited_children):
        return visited_children[0]
        
    def visit_constant(self, node, visited_children):
        return Constant(visited_children[0])
    
    def visit_variable(self, node, visited_children):
        return Variable(node.text)
    
    def visit_value(self, node, visited_children):
        return visited_children[0]
    
    def visit_word(self, node, visited_children):
        return node.text

    def visit_number(self, node, visited_children):
        return int(node.text)
        
    # 2. For modes    
    def visit_mode(self, node, visited_children):
        return visited_children[0]

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
    
    def visit_matom(self, node, visited_children):
        return self.visit_predicate(node, visited_children)
    
    def visit_mcompterm(self, node, visited_children):
        return self.visit_compoundterm(node, visited_children)
    
    def visit_mterm(self, node, visited_children):
        return visited_children[0]
    
    def visit_type(self, node, visited_children):
        sign, name = visited_children
        return Type(sign, name)
    
    def visit_sign(self, node, visited_children):
        return node.text
    
    
    # 3. For aloe file as a whole
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
        
    def visit_hclause(self, node, visited_children):
        return visited_children[0]

    def visit_background(self, node, visited_children):
        bclauses = [c for c, _ in visited_children[6]]
        return LogicProgram(bclauses)
    
    def visit_pos_ex(self, node, visited_children):
        pclauses = [c for c, _ in visited_children[6]]
        return pclauses
    
    def visit_neg_ex(self, node, visited_children):
        nclauses = [c for c, _ in visited_children[6]]
        return nclauses
    
    def visit_determination(self, node, visited_children):
        #     determination = "determination(" predname "/" number ("," predname "/" number)+ ")."    
        _, _, _, _, modeh_name, _, _, _, modeh_nargs, _, l_modeb, _, _, _ = visited_children
        deterh = '%s/%d'%(modeh_name, modeh_nargs)
        l_deterb = ['%s/%d'%(modeb_name, modeb_nargs) for _, _, modeb_name, _, _, _, modeb_nargs, _ in l_modeb]
        return (deterh, l_deterb)
        
    def visit_set(self, node, visited_children):
        _, _, _, _, attr, _, _, _, value, _, _, _, _ = visited_children
        return (attr, value)
    
    def visit_query(self, node, visited_children):
        return visited_children[0]

    def visit_goal(self, node, visited_children):
        el0, _, l_e = visited_children
        g = Goal((el0,))
        g.extend(e for _, _, e, _ in l_e)
        return g
    
    def visit_goal_unit(self, node, visited_children):
        return visited_children[0]
    
    def visit_negation(self, node, visited_children):
        _, _, _, _, goal, _, _ = visited_children
        return Negation(goal)
    
    def visit_generator(self, node, visited_children):
        l_modee, l_clauses = visited_children
        example_modes = [x for x, _ in l_modee]
        knowledge = LogicProgram([x for x, _ in l_clauses])
        return knowledge, example_modes
    
    def visit_modee(self, node, visited_children):
        _, _, atom, _ = visited_children
        return atom

    # 4. For statements
    def visit_statement(self, node, visited_children):
        choice, = visited_children
        return choice
    
    def visit_not_statement(self, node, visited_children):
        _, _, _, _, eq, _, _ = visited_children
        return Not(eq)
        
    def visit_combi_statement(self, node, visited_children):
        _, _, _, _, arg1, _, l_arg, _ = visited_children
        args = [arg1] + [arg for _, _, arg, _ in l_arg]
        combi = node.children[0].text
        if combi=='all':
            return All(args)
        else: # combi=='any'
            return Any(args)
    
    def visit_comparison(self, node, visited_children):
        return Comparison(node.text)
    
    def visit_assignment(self, node, visited_children):
        var, _, _, _, expression = visited_children
        return Assignment(var, expression)
    
    def visit_expression(self, node, visited_children):
        return Expression(node.text)

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
        new_rule = 'l_%s' % rule
        if not new_rule in self.grammar:
            rules, _ = self.grammar._expressions_from_rules('%s = (%s ws)*' % (new_rule, rule), self.grammar)
            self.grammar.update(rules)
            
            def visit_new_rule(node, visited_children):
                return [child for child, _ in visited_children]
            setattr(self.visitor, 'visit_%s' % new_rule, visit_new_rule) 
        
        return self.parse(string, rule=new_rule)

    def split_on_dots(self, text):
        text = re.sub(r'%.*\n', '\n', text)
        clauses = [c.strip()+'.' for c in text.split('.') if c]
        return clauses