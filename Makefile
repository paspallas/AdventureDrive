RM  := rm -rf
RC  := pyrcc5
PY 	:= python

.PHONY:
test:
	@$(PY) src/main.py

.PHONY:
app:
	@pyinstaller main.spec

.PHONY:
clean:
	@$(RM) __pycache__ *.ini

.PHONY:
distclean: clean
	@$(RM) dist build

.PHONY:
res:
	@$(RC) -no-compress resources/resources.qrc -o src/app/resources.py 
