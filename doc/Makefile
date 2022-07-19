zigzag.pdf: zigzag.tex zigzag.bib zz_infinite.pdf zz_bounded.pdf zz_example.pdf

%.pdf: %.tex
	pdflatex -file-line-error -interaction=nonstopmode -halt-on-error $<
	bibtex zigzag.aux
	pdflatex -file-line-error -interaction=nonstopmode -halt-on-error $<
	pdflatex -file-line-error -interaction=nonstopmode -halt-on-error $<

%.pdf: %.svg
	inkscape $< -o $@

tidy:
	rm -rf *.gz *.aux *.log *.fls *.out *.toc *.pages *.fdb* *.bbl *.xml *.blg *-blx.bib zz_*.pdf
clean: tidy
	rm zigzag.pdf
