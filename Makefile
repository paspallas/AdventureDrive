RM  := rm -rf
RC  := pyrcc5
NSI := makensis
PY 	:= python3.9

.PHONY:
test:
	@$(PY) src/main.py

.PHONY:
app:
	@$(PY) -m pyinstaller app.spec
#	@$(NSI) installer.nsi

.PHONY:
clean:
	@$(RM) __pycache__ *.ini

.PHONY:
distclean: clean
	@$(RM) dist build

.PHONY:
res: src/app/resources.py

src/app/resources.py: resources/resources.qrc
	@$(RC) -no-compress $< -o $@