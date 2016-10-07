# Makefile for blowyournose

.PHONY: default test

default: test

test:
	-rm -f booger_*.png
	nosetests --with-blowyournose --with-boogercheck -v $(ARGS)

clean:
	-rm -rf *.egg-info
	-rm booger_*.png
	-find . -name '__pycache__' -prune -exec rm -rf "{}" \;
	-find . -name '*.pyc' -delete

requirements:
	pip install -r dev-requirements.txt
