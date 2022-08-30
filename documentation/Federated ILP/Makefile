#! /usr/bin/make -f 

pdf: presentation-100122.tex
	pdflatex presentation-100122.tex; pdflatex presentation-100122.tex

handout-pdf: presentation-100122.tex
	pdfnup --nup 2x2 --a5paper --delta "0.5cm 0.5cm" --trim "-0.5cm -0.5cm -0.5cm -0.5cm" presentation-100122.pdf
	mv presentation-100122-nup.pdf handout.pdf
