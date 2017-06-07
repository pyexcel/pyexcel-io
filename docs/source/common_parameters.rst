Common parameters
================================================================================

auto_dectect_datetime
--------------------------------------------------------------------------------

The datetime formats are:

#. %Y-%m-%d
#. %Y-%m-%d %H:%M:%S
#. %Y-%m-%d %H:%M:%S.%f

Any other datetime formats will be thrown as ValueError

'library' option is added
--------------------------------------------------------------------------------

In order to have overlapping plugins co-exit, 'library' option is added to
get_data and save_data.
