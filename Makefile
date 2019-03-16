all: test

test:
	bash test.sh

document:
	sphinx-autogen -o docs/source/generated/ docs/source/*.rst
	sphinx-build -b html docs/source/ docs/build/

lint:
	bash lint.sh

