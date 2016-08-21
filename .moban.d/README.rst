{%extends "BASIC-README.rst.jj2"%}

{%block features%}

**{{name}}** provides **one** application programming interface(API) to read
and write the data in excel format, import the data into and export the data
from database. It provides support for csv(z) format, django database and
sqlalchemy supported databases. Its supported file formats are extended to cover
"xls", "xlsx", "ods" by the following extensions:

================ ==================================
Plugins          Supported file formats            
================ ==================================
`pyexcel-xls`_   xls, xlsx(r), xlsm(r)
`pyexcel-xlsx`_  xlsx
`pyexcel-ods3`_  ods
`pyexcel-ods`_   ods (python 2.6, 2.7 only)        
================ ==================================

.. _pyexcel-xls: https://github.com/pyexcel/pyexcel-xls
.. _pyexcel-xlsx: https://github.com/pyexcel/pyexcel-xlsx
.. _pyexcel-ods: https://github.com/pyexcel/pyexcel-ods
.. _pyexcel-ods3: https://github.com/pyexcel/pyexcel-ods3

If you need to manipulate the data, you might do it yourself or use its brother
library `pyexcel <https://github.com/pyexcel/pyexcel>`__ .

If you would like to extend it, you may use it to write your own
extension to handle a specific file format.

{%endblock%}
