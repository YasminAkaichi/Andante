"""
License
-------

This software is distributed under the terms of both the MIT license and the
Apache License (Version 2.0).

See LICENSE for details.

Acknowlegment
-------------

This software has benefited from the support of Wallonia thanks to the funding
of the ARIAC project (https://trail.ac), a project part of the
DigitalWallonia4.ai initiative (https://www.digitalwallonia.be).

It was done by Simon Jacquet at the University of Namur (https://www.unamur.be)
in the period of October 1st 2021 to August 31st 2022 under the supervision of
Isabelle Linden, Jean-Marie Jacquet and Wim Vanhoof. 
"""

from itertools import product
import re 

def generate_variable_names():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for nchar in range(1,5):
        for letters in product(alphabet, repeat=nchar):
            name = ''.join(letters)
            yield name

def multiple_replace(dict, text):
    """ source: https://stackoverflow.com/questions/15175142/how-can-i-do-multiple-substitutions-using-regex """
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    return regex.sub(lambda mo: dict[mo.string[mo.start():mo.end()]], text) 
    
