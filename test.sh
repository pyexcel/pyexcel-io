#/bin/bash
pip freeze
coverage run -m --source=pyexcel_io pytest --doctest-modules && coverage report --show-missing
