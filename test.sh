#/bin/bash
pip freeze
nosetests --rednose --with-cov --cov pyexcel_io --cov tests --with-doctest --doctest-extension=.rst doc/source tests pyexcel_io
rm tmp.db

