"""A relationship matrix plugin for novelibre

Requires Python 3.6+
Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
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
from pathlib import Path
from tkinter import ttk
import webbrowser

from mvclib.view.set_icon_tk import set_icon
from nvlib.plugin.plugin_base import PluginBase
from nvmatrixlib.nvmatrix_globals import _
from nvmatrixlib.table_manager import TableManager
import tkinter as tk


class Plugin(PluginBase):
    """novelibre relationship matrix plugin class."""
    VERSION = '@release'
    API_VERSION = '5.0'
    DESCRIPTION = 'A section relationship table'
    URL = 'https://github.com/peter88213/nv_matrix'
    _HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_matrix/'

    FEATURE = _('Matrix')
    INI_FILENAME = 'matrix.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        window_geometry='600x800',
        color_bg_00='gray80',
        color_bg_01='gray85',
        color_bg_10='gray95',
        color_bg_11='white',
        color_arc_heading='deepSkyBlue',
        color_arc_node='deepSkyBlue3',
        color_character_heading='goldenrod1',
        color_character_node='goldenrod3',
        color_location_heading='coral1',
        color_location_node='coral3',
        color_item_heading='aquamarine1',
        color_item_node='aquamarine3',
    )
    OPTIONS = {}

    def install(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- Reference to the model instance of the application.
            view -- Reference to the main view instance of the application.
            controller -- Reference to the main controller instance of the application.

        Optional arguments:
            prefs -- deprecated. Please use controller.get_preferences() instead.
        
        Extends the superclass method.
        """
        super().install(model, view, controller)
        self._matrixViewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.make_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.kwargs = {}
        self.kwargs.update(self.configuration.settings)
        self.kwargs.update(self.configuration.options)

        # Create an entry to the Tools menu.
        self._ui.toolsMenu.add_command(label=self.FEATURE, command=self._start_viewer)
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(label=_('Matrix plugin Online help'), command=lambda: webbrowser.open(self._HELP_URL))

        #--- Configure the toolbar.
        self._configure_toolbar()

    def disable_menu(self):
        """Disable menu entries when no project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='disabled')
        self._matrixButton.config(state='disabled')

    def enable_menu(self):
        """Enable menu entries when a project is open.
        
        Overrides the superclass method.
        """
        self._ui.toolsMenu.entryconfig(self.FEATURE, state='normal')
        self._matrixButton.config(state='normal')

    def lock(self):
        """Inhibit changes on the model.
        
        Overrides the superclass method.
        """
        if self._matrixViewer:
            self._matrixViewer.lock()

    def on_close(self):
        """Apply changes and close the window.
        
        Overrides the superclass method.
        """
        self.on_quit()

    def on_quit(self):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                self._matrixViewer.on_quit()

        #--- Save configuration
        for keyword in self.kwargs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.kwargs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.kwargs[keyword]
        self.configuration.write(self.iniFile)

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        if self._matrixViewer:
            self._matrixViewer.unlock()

    def _configure_toolbar(self):

        # Get the icons.
        prefs = self._ctrl.get_preferences()
        if prefs.get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
        except:
            iconPath = None
        try:
            matrixIcon = tk.PhotoImage(file=f'{iconPath}/matrix.png')
        except:
            matrixIcon = None

        # Put a Separator on the toolbar.
        tk.Frame(self._ui.toolbar.buttonBar, bg='light gray', width=1).pack(side='left', fill='y', padx=4)

        # Initialize the operation.
        self._matrixButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=_('Matrix'),
            image=matrixIcon,
            command=self._start_viewer
            )
        self._matrixButton.pack(side='left')
        self._matrixButton.image = matrixIcon

        # Initialize tooltip.
        if not prefs['enable_hovertips']:
            return

        try:
            from idlelib.tooltip import Hovertip
        except ModuleNotFoundError:
            return

        Hovertip(self._matrixButton, self._matrixButton['text'])

    def _start_viewer(self):
        if not self._mdl.prjFile:
            return

        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                if self._matrixViewer.state() == 'iconic':
                    self._matrixViewer.state('normal')
                self._matrixViewer.lift()
                self._matrixViewer.focus()
                return

        self._matrixViewer = TableManager(self._mdl, self._ui, self._ctrl, self, **self.kwargs)
        self._matrixViewer.title(f'{self._mdl.novel.title} - {self.FEATURE}')
        set_icon(self._matrixViewer, icon='mLogo32', default=False)

