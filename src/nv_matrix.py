"""A relationship matrix plugin for novelibre

Requires Python 3.7+
Copyright (c) 2025 Peter Triesberger
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

from nvmatrix.nvmatrix_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvmatrix.matrix_service import MatrixService
import tkinter as tk


class Plugin(PluginBase):
    """novelibre relationship matrix plugin class."""
    VERSION = '@release'
    API_VERSION = '5.35'
    DESCRIPTION = 'A section relationship table'
    URL = 'https://github.com/peter88213/nv_matrix'
    HELP_URL = f'{_("https://peter88213.github.io/nvhelp-en")}/nv_matrix/'

    FEATURE = _('Matrix')

    def install(self, model, view, controller):
        """Add a submenu to the 'Tools' menu.
        
        Positional arguments:
            model -- Reference to the model instance.
            view -- Reference to the main view instance.
            controller -- Reference to the main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.matrixService = MatrixService(model, view, controller)
        self._icon = self._get_icon('matrix.png')

        # Create an entry to the Tools menu.
        self._ui.toolsMenu.add_command(
            label=self.FEATURE,
            image=self._icon,
            compound='left',
            command=self.start_viewer,
            state='disabled',
        )

        # Add an entry to the Help menu.
        self._ui.helpMenu.add_command(
            label=_('Matrix plugin Online help'),
            image=self._icon,
            compound='left',
            command=self.open_help,
        )

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
        self.matrixService.lock()

    def on_close(self):
        """Apply changes and close the window.
        
        Overrides the superclass method.
        """
        self.matrixService.on_close()

    def on_quit(self):
        """Actions to be performed when novelibre is closed.
        
        Overrides the superclass method.
        """
        self.matrixService.on_quit()

    def open_help(self):
        webbrowser.open(self.HELP_URL)

    def start_viewer(self):
        self.matrixService.start_viewer(self.FEATURE)

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        self.matrixService.unlock()

    def _configure_toolbar(self):

        # Put a Separator on the toolbar.
        tk.Frame(
            self._ui.toolbar.buttonBar,
            bg='light gray',
            width=1,
        ).pack(side='left', fill='y', padx=4)

        # Initialize the operation.
        self._matrixButton = ttk.Button(
            self._ui.toolbar.buttonBar,
            text=_('Matrix'),
            image=self._icon,
            command=self.start_viewer
            )
        self._matrixButton.pack(side='left')
        self._matrixButton.image = self._icon

        # Initialize tooltip.
        if not self._ctrl.get_preferences()['enable_hovertips']:
            return

        self._mdl.nvService.new_hovertip(
            self._matrixButton, self._matrixButton['text']
        )

    def _get_icon(self, fileName):
        # Return the icon for the main view.
        if self._ctrl.get_preferences().get('large_icons', False):
            size = 24
        else:
            size = 16
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            iconPath = f'{homeDir}/.novx/icons/{size}'
            icon = tk.PhotoImage(file=f'{iconPath}/{fileName}')
        except:
            icon = None
        return icon
