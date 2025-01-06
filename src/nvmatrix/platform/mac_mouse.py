"""Provide a class with mouse opersion definitions for the Mac OS.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from nvmatrix.platform.generic_mouse import GenericMouse


class MacMouse(GenericMouse):

    TOGGLE_STATE = '<Command-Button-1>'
