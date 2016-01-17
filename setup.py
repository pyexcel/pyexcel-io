try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages
import sys

with open("README.rst", 'r') as readme:
    README_txt = readme.read()

with open("VERSION", "r") as version:
    version_txt = version.read().rstrip()

dependencies = []

if sys.version_info[0] == 2 and sys.version_info[1] < 7:
    dependencies.append('ordereddict')

extras = {
    'xls': ['pyexcel-xls>=0.1.0'],
    'xlsx': ['pyexcel-xlsx>=0.1.0'],
    'ods': ['pyexcel-ods3>=0.1.0']
}

setup(
    name='pyexcel-io',
    author="C. W.",
    version=version_txt,
    author_email="wangc_2011@hotmail.com",
    url="https://github.com/chfw/pyexcel-io",
    description='A python library to read and write structured data in csv, zipped csv format and to/from databases',
    install_requires=dependencies,
    extras_require=extras,
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    long_description=README_txt,
    zip_safe=False,
    tests_require=['nose'],
    license='New BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Office/Business',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
