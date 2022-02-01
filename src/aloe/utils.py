from itertools import product
def generate_variable_names():
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for nchar in range(1,5):
        for letters in product(alphabet, repeat=nchar):
            name = ''.join(letters)
            yield name


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

def red(text):
    return bcolors.BOLD + text + bcolors.ENDC