import re
import bisect 
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from parsimonious.exceptions import ParseError, VisitationError
from aloe.clause    import Clause, Predicate, CompoundTerm, Variable, Constant, Negation, Goal, Type
from aloe.mode      import ModeCollection, Mode, Modeh, Modeb
from aloe.options   import Options, SystemParameters
from aloe.program   import AloeProgram
from aloe.knowledge import LogicProgram
from aloe.utils     import red

grammar = Grammar(
    r"""    
    aloefile         = header? background pos_ex? neg_ex?
    header           = hclause+
    hclause          = mode / determination / set
    background       = ":-begin_bg." bclause+ ":-end_bg."
    bclause          = hornclause
    pos_ex           = ":-begin_in_pos." pclause+ ":-end_in_pos."
    pclause          = hornclause
    neg_ex           = ":-begin_in_neg." nclause+ ":-end_in_neg."
    nclause          = hornclause

    determination = "determination(" predname "/" number ("," predname "/" number)+ ")."    
    set           = "set(" word "," value ")."
    
    hornclause       = headlessclause / definiteclause
    headlessclause   =       ":-" body   "."
    definiteclause   = head (":-" body)? "."
    head             = atom
    body             = atom ("," atom)*
    atom             = "true" / "false" / predicate
    predicate        = predname "(" term ("," term)* ")"
    term             = compoundterm / variable / constant 
    compoundterm     = funcname "(" term ("," term)* ")"
    predname         = word
    funcname         = word
    constant         = value / value
    value            = number / word
    word             = ~"[a-z]\w*"
    variable         = ~"[A-Z]\w*"
    number           = ~"\d+"

    mode      = modeh / modeb
    modeh     = "modeh(" recall "," matom ")."
    modeb     = "modeb(" recall "," matom ")."
    recall    = "*" / number
    matom     = predname "(" mterm ("," mterm)* ")" 
    mcompterm = funcname "(" mterm ("," mterm)* ")"
    mterm     = type / mcompterm / constant
    type      = sign word
    sign      = ~"[+\-#]"
    
    query     = goal "."
    goal      = goal_unit ("," goal_unit)*
    goal_unit = negation / atom
    negation  = "not(" goal ")"
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
        _, body, _ = visited_children
        if len(body)==1:
            return Clause(None, body[0])
        else:
            return Clause(None, body)
    
    def visit_definiteclause(self, node, visited_children):
        head, optional_body, _ = visited_children
        if optional_body:
            _, body = optional_body[0]
            return Clause(head, body)
        else:
            return Clause(head, [])
    
    def visit_body(self, node, visited_children):
        atom1, opt_atoms = visited_children
        atoms = [atom1] + [atom for _, atom in opt_atoms]
        return atoms
    
    def visit_atom(self, node, visited_children):
        return visited_children[0]
    
    def visit_predicate(self, node, visited_children):
        predname, _, term1, opt_terms, _ = visited_children
        terms = [term1] + [term for _, term in opt_terms]
        return Predicate(predname, terms)
    
    def visit_compoundterm(self, node, visited_children):
        funcname, _, term1, opt_terms, _ = visited_children
        terms = [term1] + [term for _, term in opt_terms]
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
        _, recall, _, atom, _ = visited_children
        return Modeh(recall, atom)

    def visit_modeb(self, node, visited_children):
        _, recall, _, atom, _ = visited_children
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
        opt_header, background, opt_pos_ex, opt_neg_ex = visited_children
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
        for node_child, visited_child in zip(node, visited_children):
            header[node_child.children[0].expr_name].append(visited_child)
            
        mhandler = ModeCollection(header['mode'], header['determination'])
        options  = Options(header['set'])
        return {'modehandler':mhandler, 'options':options}
        
    def visit_hclause(self, node, visited_children):
        return visited_children[0]

    def visit_background(self, node, visited_children):
        _, bclauses, _ = visited_children
        return LogicProgram(bclauses)
    
    def visit_pos_ex(self, node, visited_children):
        _, pclauses, _ = visited_children
        return pclauses
    
    def visit_neg_ex(self, node, visited_children):
        _, nclauses, _ = visited_children
        return nclauses
    
    def visit_determination(self, node, visited_children):
        #     determination = "determination(" predname "/" number ("," predname "/" number)+ ")."    
        _, modeh_name, _, modeh_nargs, l_modeb, _ = visited_children
        deterh = '%s/%d'%(modeh_name, modeh_nargs)
        l_deterb = ['%s/%d'%(modeb_name, modeb_nargs) for _, modeb_name, _, modeb_nargs in l_modeb]
        return (deterh, l_deterb)
        
    def visit_set(self, node, visited_children):
        _, attr, _, value, _ = visited_children
        return (attr, value)
    
    def visit_query(self, node, visited_children):
        return visited_children[0]

    def visit_goal(self, node, visited_children):
        el0, l_e = visited_children
        g = Goal((el0,))
        g.extend(e for _, e in l_e)
        return g
    
    def visit_goal_unit(self, node, visited_children):
        return visited_children[0]
    
    def visit_negation(self, node, visited_children):
        _, goal, _ = visited_children
        return Negation(goal)

class AloeParser:
    def __init__(self):
        self.grammar = grammar
        self.visitor = AloeVisitor()
        
    def parse_file(self, filepath):
        """
        Parses aloe files
        Input: filepath: path to the file to parse
        Ouput: list of Clause
        """
        with open(filepath, 'r') as file:
            orig_text = file.read()
            
        return self.parse(orig_text)
            
    def parse(self, string):
        """
        Parses aloe text
        Input: string: either a path to a file or a text to parse
        Ouput: list of Clause
        """
        
        # Case where string is the path to a file
        try:    orig_text = open(string, 'r').read()            
        except: orig_text = string
        
        at = AloeText(orig_text)
        
        # Remove spaces and comments from text
        at.preprocess()
        
        # Build nchar2lign function
        at.build_nchar2lign()
        
        # Remove line breaks
        at.remove_linebreaks()
        
        try:
            program = self.parse_rule(at.text,'aloefile')
        except ParseError as e:
            line    = at.nchar2lign(e.pos)
            c1, c2  = at.nchar2clause(e.pos)
            message = 'Error:\n%2d. %s%s' % (line,c1,red(c2))
            raise Exception(message)
        except VisitationError as e:
            message = 'Error in the code when visiting the parsed tree. This should not happen. Please report it.'
            raise Exception(message)
        except Exception as e:
            raise e
            
        return program
        
                        
    def parse_rule(self, text, rule_name):
        """
        Parses aloe expression
        Input: text: string representing the expression to parse
        Ouput: ouput: the expression parsed and transformed 
        """
        self.grammar.default_rule = self.grammar[rule_name]        
        tree   = self.grammar.parse(text)
        output = self.visitor.visit(tree)
        return output
    
    def parse_clauses(self, text):
        at = AloeText(text)
        at.preprocess()
        clauses = at.get_clauses()
        for clause in clauses:            
            try:
                yield self.parse_rule(clause,'hornclause')
            except ParseError as e:
                message = 'Parsing error\nClause:%s' % (str(clause))
                raise Exception(message)
            except VisitationError as e:
                message = 'Error in the code when visiting the parsed tree. This should not happen. Please report it.'
                raise Exception(message)
            except Exception as e:
                raise e
    
    def parse_query(self, text):
        text = ''.join(text.split())
        return self.parse_rule(text, 'query')
    
    
class AloeText:
    def __init__(self, orig_text):
        self.orig_text = orig_text
        self.text = orig_text
        
    def preprocess(self):
        """ Spaces and comments are removed from file """
        # Remove all spaces
        self.text = self.text.replace(' ','')
        # Remove all comments
        self.text = re.sub(r'%.*\n', '\n', self.text)
        
    def remove_linebreaks(self):
        self.text = self.text.replace('\n','')
        
    def build_nchar2lign(self):
        """
        For 'text' build a correspondance between the character count and the lign in text
        """
        # self._correspondance:
        #    -- ['lign'][i]:    lign number
        #    -- ['numchar'][i]: cumulative number of characters before lign ['lign'][i] is finished
        self._correspondance = {'lign':list(), 'numchar':list()}
        
        char_count = 0 # count for the number of characters
        for l, line in enumerate(self.text.split("\n"), 1):
            if line:
                char_count += len(line)
                self._correspondance['lign'].append(l)
                self._correspondance['numchar'].append(char_count)
                
    def nchar2lign(self, nchar):
        """
        Searches in self._correspondance to which lign corresponds the 'nchar'-th character
        """
        if not hasattr(self, '_correspondance'):
            raise Exception("build_nchar2lign needs to be called before using this method")

        if nchar>=len(self.text):
            raise Exception("nchar is bigger than the size of the text. nchar=%d and len(text)=%d" % (nchar, len(self.text)))

        i = bisect.bisect_right(self._correspondance['numchar'],nchar)        
        return self._correspondance['lign'][i]
    
    def nchar2clause(self, nchar):
        beg = 0
        for i in range(nchar,-1,-1):
            if self.text[i]=='.':
                beg = i+1
                break
        end = len(self.text)
        for i in range(nchar,len(self.text)):
            if self.text[i]=='.':
                end = i+1
                break
        return self.text[beg:i], self.text[i:end]
        
    def get_clauses(self):
        """ Split text into clauses """
        # Remove linebreaks from text
        text = self.text.replace('\n','')
        
        # Split text in a list of clauses (split on ".")
        text = text.replace('.','.\n')
        clauses = text.split('\n')[:-1]        
        
        return clauses