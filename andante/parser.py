import re
from parsimonious.exceptions import ParseError, VisitationError
from andante.grammar import GRAMMAR
from andante.grammar_tree_visitor import Visitor

class Parser:
    """ Parser that can interpret any grammar rules present in andante/grammar.py
    
    Attributes
    ----------
    grammar : parsimonious.grammar.Grammar
        Defines all rules that can be parsed
    visitor : andante.grammar_tree_visitor.Visitor
        Navigates through the grammatical tree outputed by the grammar object into a useful Python object
    """
    def __init__(self):
        self.grammar = GRAMMAR
        self.visitor = Visitor()

    def parse(self, string, rule='hornclause'):
        """ Transforms the input string according to the specified rule

        Parameters
        ----------
        string : str
            Either some text or the path to a file
        rule : str
            The rule on which to parse the input string

        Returns
        -------
        object
            Object from the andante package whose class depends on input rule
        """
        string = string.strip()
        
        # Case where string is the path to a file
        try:    
            full_text = open(string, 'r').read()            
            filename  = string
        except: 
            full_text = string
            filename  = ""
            
        # Remove all comments
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
        """ Parses the input string that contains multiple occurences of some rule 
        
        Parameters
        ----------
        string : str
            Either some text or the path to a file
        rule : str
            The rule that is repeated in the input string

        Returns
        -------
        list
            List of objects
        """
        new_rule = 'l_%s' % rule
        if not new_rule in self.grammar:
            rules, _ = self.grammar._expressions_from_rules('%s = (%s __)*' % (new_rule, rule), self.grammar)
            self.grammar.update(rules)
            
            def visit_new_rule(node, visited_children):
                return [child for child, _ in visited_children]
            setattr(self.visitor, 'visit_%s' % new_rule, visit_new_rule) 
        
        return self.parse(string, rule=new_rule)

    def split_on_dots(self, text):
        """ Split the input text on the dots """
        text = re.sub(r'%.*\n', '\n', text)
        clauses = [c.strip()+'.' for c in text.split('.') if c]
        return clauses
