API changes from 0.1.0 to 0.2.0
================================================================================

pyexcel-io version 0.2.0 is not 100% backward compatible and requires version
0.2.0 of its plugins to function seamlessly. Here are the differences.


get_data returns a dictionary of two dimensional array always
---------------------------------------------------------------

Version 0.1.0 and elder, get_data returns a two dimensional array if there
is only one sheet and returns a dictionary of two dimensional array otherwise.
This behaviour has removed in 0.2.0

load_data is deprecated and should not be used
--------------------------------------------------------------------------------

Version 0.1.0 and elder, load_data was used by pyexcel and maybe by others.
Version 0.2.0 discourage you from using it as it will be removed at some point
in the future.

