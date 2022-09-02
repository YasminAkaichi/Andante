"""
Defines the grammar used by the andante.parser.Parser object.

This grammar allows input strings to be converted to so-called grammar trees.

License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.

Acknowlegment
-------------

This software has benefited from the support of Wallonia thanks to the funding of 
the ARIAC project (https://trail.ac), a project part of the DigitalWallonia4.ai 
initiative (https://www.digitalwallonia.be).

It was done by Simon Jacquet at the University of Namur (https://www.unamur.be) in the period of October 1st 2021 to August 31st 2022 under the supervision of Isabelle Linden, Jean-Marie Jacquet and Wim Vanhoof. 
"""

import parsimonious
from parsimonious.grammar import Grammar

GRAMMAR = Grammar(
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
            
    andantefile         = __ header? __ background __ pos_ex? __ neg_ex? __
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
