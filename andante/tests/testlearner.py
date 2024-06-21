from andante.program import AndanteProgram 
ap1 = AndanteProgram.build_from("data_part1.pl")
H = ap1.induce(update_knowledge=True, logging=True, verbose=0)
print(H)