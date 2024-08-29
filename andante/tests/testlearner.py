from andante.program import AndanteProgram 
from andante.logic_concepts import Clause,Atom
ap1 = AndanteProgram.build_from("data_part1.pl")
H = ap1.induce(update_knowledge=True, logging=True, verbose=0)
text = """
:- begin_bg.

complication(x) :- intubationdifficile(x).

:- end_bg.
"""
rule = AndanteProgram.build_from(text)
ap1.knowledge.add(rule.knowledge)
print(ap1.knowledge)