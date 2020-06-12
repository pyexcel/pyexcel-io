all: test

test:
	bash test.sh

install_test:
	pip install -r tests/requirements.txt

document:
	sphinx-autogen -o docs/source/generated/ docs/source/*.rst
	sphinx-build -b html docs/source/ docs/build/

format:
	isort -y $(find pyexcel_io -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
	black -l 79 pyexcel_io
	black -l 79 tests

lint:
	bash lint.sh

git-diff-check:
	git diff --exit-code

