RM  := rm -rf
RC  := pyrcc5
PY 	:= python3.9

.PHONY:
test:
	@$(PY) src/main.py

.PHONY:
app:
	@pyinstaller main.spec
#	@makensis installer.nsi

.PHONY:
clean:
	@$(RM) __pycache__ *.ini

.PHONY:
distclean: clean
	@$(RM) dist build

.PHONY:
res:
	@$(RC) -no-compress resources/resources.qrc -o src/app/resources.py 