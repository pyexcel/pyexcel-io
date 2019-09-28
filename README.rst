{%extends "BASIC-README.rst.jj2"%}

{%block features%}

**{{name}}** provides **one** application programming interface(API) to read
and write the data in excel format, import the data into and export the data
from database. It provides support for csv(z) format, django database and
sqlalchemy supported databases. Its supported file formats are extended to cover
"xls", "xlsx", "ods" by the following extensions:

{% include "io-plugins-list.rst.jj2" %}

If you need to manipulate the data, you might do it yourself or use its brother
library `pyexcel <https://github.com/pyexcel/pyexcel>`__ .

If you would like to extend it, you may use it to write your own
extension to handle a specific file format.

{%endblock%}
