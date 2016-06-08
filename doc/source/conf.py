# -*- coding: utf-8 -*-
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

intersphinx_mapping = {
    'pyexcel': ('http://pyexcel.readthedocs.org/en/latest/', None)
}

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pyexcel-io'
copyright = u'2015-2016 Onni Software Ltd.'
version = '0.2.1'
release = '0.2.1'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
def setup(app):
    app.add_stylesheet('theme_overrides.css')
html_static_path = ['_static']
htmlhelp_basename = 'pyexcel-iodoc'
latex_elements = {}
latex_documents = [
    ('index', 'pyexcel-io.tex', u'pyexcel-io Documentation',
     'Onni Software Ltd.', 'manual'),
]
man_pages = [
    ('index', 'pyexcel-io', u'pyexcel-io Documentation',
     [u'Onni Software Ltd.'], 1)
]
texinfo_documents = [
    ('index', 'pyexcel-io', u'pyexcel-io Documentation',
     'Onni Software Ltd.', 'pyexcel-io', 'One line description of project.',
     'Miscellaneous'),
]
