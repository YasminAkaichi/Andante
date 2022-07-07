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
    