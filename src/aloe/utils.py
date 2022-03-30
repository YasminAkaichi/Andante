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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
    def green(text): return bcolors.OKGREEN + text + bcolors.ENDC
    def red(text):   return bcolors.FAIL    + text + bcolors.ENDC
    
    def ipygreen(text): return r'\(\color{green} {' + text  + '}\)'
    def ipyred(text):   return r'\(\color{red} {'   + text  + '}\)'
    
def red(text):
    return bcolors.BOLD + text + bcolors.ENDC