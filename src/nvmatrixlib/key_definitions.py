"""Provide platform specific key definitions for the nv_matrix plugin.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvmatrixlib.nvmatrix_globals import PLATFORM
from nvmatrixlib.generic_keys import GenericKeys
from nvmatrixlib.mac_keys import MacKeys
from nvmatrixlib.linux_keys import LinuxKeys
from nvmatrixlib.windows_keys import WindowsKeys

if PLATFORM == 'win':
    KEYS = WindowsKeys()
elif PLATFORM == 'ix':
    KEYS = LinuxKeys()
elif PLATFORM == 'mac':
    KEYS = MacKeys()
else:
    KEYS = GenericKeys()
