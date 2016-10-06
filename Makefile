# Makefile for blowyournose

.PHONY: default test

default: test

test:
	nosetests --with-blowyournose --with-boogercheck -v

clean:
	-rm -rf *.egg-info
	-find . -name '__pycache__' -prune -exec rm -rf "{}" \;
	-find . -name '*.pyc' -delete

requirements:
	pip install -r dev-requirements.txt
