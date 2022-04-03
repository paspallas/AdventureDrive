# adventure drive project makefile

RM  := rm -rf
RC  := pyrrc5
NSI := makensis
PYI := pyinstaller

.PHONY:
app:
	@$(PYI) app.spec
#	@$(NSI) installer.nsi

.PHONY:
clean:
	@$(RM) __pycache__ *.ini

.PHONY:
distclean: clean
	@$(RM) dist build

.PHONY:
res: src/resources.py

*.py: *.qrc
	@$(RC) $< -o $@