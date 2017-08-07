Packaging with PyInstaller
================================================================================

With pyexcel-io v0.4.0, the way to package it has been changed because it
uses lml for all plugins.

Built-in plugins of pyexcel-io
-------------------------------

In order to package every built-in plugins of pyexcel-io, you need to specify::

    --hidden-import pyexcel_io.readers.csvr
    --hidden-import pyexcel_io.readers.csvz
    --hidden-import pyexcel_io.readers.tsv
    --hidden-import pyexcel_io.readers.tsvz
    --hidden-import pyexcel_io.writers.csvw
    --hidden-import pyexcel_io.readers.csvz
    --hidden-import pyexcel_io.readers.tsv
    --hidden-import pyexcel_io.readers.tsvz
    --hidden-import pyexcel_io.database.importers.django
    --hidden-import pyexcel_io.database.importers.sqlalchemy
    --hidden-import pyexcel_io.database.exporters.django
    --hidden-import pyexcel_io.database.exporters.sqlalchemy

pyexcel-xlsx
----------------

In order to package pyexcel-xlsx, you need to specify::

    --hidden-import pyexcel_xlsx
    --hidden-import pyexcel_xlsx.xlsxr
    --hidden-import pyexcel_xlsx.xlsxw

pyexcel-xlsxw
----------------

In order to package pyexcel-xlsxw, you need to specify::

    --hidden-import pyexcel_xlsxw
    --hidden-import pyexcel_xlsxw.xlsxw

pyexcel-xls
----------------

In order to package pyexcel-xls, you need to specify::

    --hidden-import pyexcel_xls
    --hidden-import pyexcel_xls.xlsr
    --hidden-import pyexcel_xls.xlsw


pyexcel-ods
----------------

In order to package pyexcel-ods, you need to specify::

    --hidden-import pyexcel_ods
    --hidden-import pyexcel_ods.odsr
    --hidden-import pyexcel_ods.odsw

pyexcel-ods3
----------------

In order to package pyexcel-ods3, you need to specify::

    --hidden-import pyexcel_ods3
    --hidden-import pyexcel_ods3.odsr
    --hidden-import pyexcel_ods3.odsw

pyexcel-odsr
----------------

In order to package pyexcel-odsr, you need to specify::

    --hidden-import pyexcel_odsr
    --hidden-import pyexcel_odsr.odsr


