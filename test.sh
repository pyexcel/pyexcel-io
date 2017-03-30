pip freeze
nosetests --with-cov --cover-package pyexcel_io --cover-package tests --with-doctest --doctest-extension=.rst README.rst tests docs/source pyexcel_io && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
