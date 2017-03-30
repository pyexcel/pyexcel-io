from mock import patch
from nose.tools import eq_


@patch('pkgutil.get_importer')
def test_load_from_pyinstaller(pkgutil_get_importer):
    sample_toc = set(['pyexcel_io', 'pyexcel_xls', 'blah'])
    pkgutil_get_importer.return_value.toc = sample_toc
    from pyexcel_io.manager import load_from_pyinstaller
    module_names = load_from_pyinstaller('pyexcel_', 'path')
    expected = ['pyexcel_io', 'pyexcel_xls']
    eq_(sorted(list(module_names)), sorted(expected))


@patch('pkgutil.get_importer')
@patch('pkgutil.iter_modules')
@patch('pyexcel_io.manager.pre_register')
def test_load_plugins(pre_register,
                      pkgutil_iter_modules,
                      pkgutil_get_importer):
    sample_toc = set(['pyexcel_io'])
    pkgutil_get_importer.return_value.toc = sample_toc
    pkgutil_iter_modules.return_value = [('not used', 'pyexcel_xls', True)]
    from pyexcel_io.manager import load_plugins
    load_plugins('pyexcel_', '.', ['pyexcel_io'])
    plugin_meta = {
        'file_types': ['xls', 'xlsx', 'xlsm'],
        'submodule': 'xls',
        'stream_type': 'binary'
    }
    module_name = 'pyexcel_xls'
    pre_register.assert_called_with(plugin_meta, module_name)


@patch('pkgutil.get_importer')
@patch('pkgutil.iter_modules')
@patch('pyexcel_io.manager.pre_register')
def test_load_plugins_without_pyinstaller(pre_register,
                                          pkgutil_iter_modules,
                                          pkgutil_get_importer):
    sample_toc = set()
    pkgutil_get_importer.return_value.toc = sample_toc
    pkgutil_iter_modules.return_value = [('not used', 'pyexcel_xls', True)]
    from pyexcel_io.manager import load_plugins
    load_plugins('pyexcel_', '.', ['pyexcel_io'])
    plugin_meta = {
        'file_types': ['xls', 'xlsx', 'xlsm'],
        'submodule': 'xls',
        'stream_type': 'binary'
    }
    module_name = 'pyexcel_xls'
    pre_register.assert_called_with(plugin_meta, module_name)


@patch('pkgutil.get_importer')
@patch('pkgutil.iter_modules')
@patch('pyexcel_io.manager.pre_register')
def test_load_plugins_without_any_plugins(pre_register,
                                          pkgutil_iter_modules,
                                          pkgutil_get_importer):
    sample_toc = set()
    pkgutil_get_importer.return_value.toc = sample_toc
    pkgutil_iter_modules.return_value = []
    from pyexcel_io.manager import load_plugins
    load_plugins('pyexcel_', '.', ['pyexcel_io'])
    assert pre_register.called is False


@patch('pkgutil.get_importer')
@patch('pkgutil.iter_modules')
@patch('pyexcel_io.manager.pre_register')
def test_load_plugins_import_error(pre_register,
                                   pkgutil_iter_modules,
                                   pkgutil_get_importer):
    sample_toc = set(['test_non_existent_module'])
    pkgutil_get_importer.return_value.toc = sample_toc
    pkgutil_iter_modules.return_value = [('not used', 'pyexcel_xls', False)]
    from pyexcel_io.manager import load_plugins
    load_plugins('test_', '.', ['pyexcel_io'])
    assert pre_register.called is False
