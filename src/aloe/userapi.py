from aloe.program import AloeProgram

p = None

def induce(theory):
    bckg_th = theory['background']
    pos_ex = theory['positive_examples']
    neg_ex = theory['negative_examples']
    modes = theory['modes']
    
    text = '%s :-begin_bg. %s :-end_bg. \n :-begin_in_pos. %s :-end_in_pos. :-begin_in_neg. %s :-end_in_neg. ' % (modes, bckg_th, pos_ex, neg_ex)
    p = AloeProgram.build_from_text(text)
    c = p.induce()
    
    p = AloeProgram.build_from_text(':-begin_bg. %s %s :-end_bg.' % (bckg_th, c))
    
    return c

def induce(t): return 'daughter(V0,V1):-parent(V1,V0),female(V0).'

def deduce(theory, q):
    return p.deduce(q)

def deduce(a,b): return '{X:ann}'