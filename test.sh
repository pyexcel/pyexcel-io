#/bin/bash

nosetests --rednose --with-cov --cov pyexcel_io --cov tests --with-doctest --doctest-extension=.rst doc/source tests pyexcel_io

