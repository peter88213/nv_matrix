"""A relationship matrix plugin for noveltree

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/noveltree_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import gettext
import locale
import os
from pathlib import Path
import sys
import webbrowser

from novxlib.config.configuration import Configuration
from novxlib.novx_globals import CURRENT_LANGUAGE
from novxlib.novx_globals import _
from novxlib.ui.set_icon_tk import set_icon
from nvmatrixlib.table_manager import TableManager

SETTINGS = dict(
        window_geometry='600x800',
        color_bg_00='gray80',
        color_bg_01='gray85',
        color_bg_10='gray95',
        color_bg_11='white',
        color_arc_heading='royalblue1',
        color_arc_node='royalblue3',
        color_character_heading='goldenrod1',
        color_character_node='goldenrod3',
        color_location_heading='coral1',
        color_location_node='coral3',
        color_item_heading='aquamarine1',
        color_item_node='aquamarine3',
        )
OPTIONS = dict(
        )

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('nv_matrix', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPLICATION = _('Matrix')
PLUGIN = f'{APPLICATION} plugin v@release'


class Plugin:
    """noveltree relationship matrix plugin class."""
    VERSION = '@release'
    NOVELYST_API = '1.0'
    DESCRIPTION = 'A section relationship table'
    URL = 'https://peter88213.github.io/noveltree_matrix'
    _HELP_URL = 'https://peter88213.github.io/noveltree_matrix/usage'

    def install(self, model, view, controller, prefs):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- Reference to the model instance of the application.
            view -- Reference to the main view instance of the application.
            controller -- Reference to the main controller instance of the application.
        """
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._matrixViewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/.noveltree/config'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/matrix.ini'
        self.configuration = Configuration(SETTINGS, OPTIONS)
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Create an entry to the Tools menu.
        position = self._ui.mainMenu.index('end')
        self._ui.mainMenu.insert_command(position, label=APPLICATION, command=self._start_ui)
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Matrix plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

    def _start_ui(self):
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.lift()
                self._matrixViewer.focus()
                return

        self._matrixViewer = TableManager(self._mdl, self._ui, self._ctrl, self, **self.kwargs)
        self._matrixViewer.title(f'{self._mdl.novel.title} - {PLUGIN}')
        set_icon(self._matrixViewer, icon='mLogo32', default=False)

    def disable_menu(self):
        """Disable menu entries when no project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open."""
        self._ui.mainMenu.entryconfig(APPLICATION, state='normal')

    def on_close(self):
        """Apply changes and close the window."""
        self.on_quit()

    def on_quit(self):
        """Actions to be performed when noveltree is closed."""
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.on_quit()

        #--- Save project specific configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)
