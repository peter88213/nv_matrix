"""A relationship matrix plugin for novelibre

Requires Python 3.7+
Copyright (c) Peter Triesberger
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
from nvmatrix.nvmatrix_locale import _
from nvlib.controller.plugin.plugin_base import PluginBase
from nvmatrix.matrix_service import MatrixService


class Plugin(PluginBase):
    """novelibre relationship matrix plugin class."""
    VERSION = '@release'
    API_VERSION = '5.63'
    DESCRIPTION = 'A section relationship table'
    URL = 'https://github.com/peter88213/nv_matrix'
    HELP_PAGE = 'nv_matrix'

    FEATURE = _('Matrix')

    def install(self, model, view, controller):
        """Install the plugin at runtime.
        
        Positional arguments:
            model -- Reference to the model instance.
            view -- Reference to the main view instance.
            controller -- Reference to the main controller instance.

        Extends the superclass method.
        """
        super().install(model, view, controller)
        self.matrixService = MatrixService(model, view, controller)
        self._icon = self._get_icon('matrix.png')

        #--- Configure the user interface.

        def start_viewer():
            self.matrixService.start_viewer(self.FEATURE)

        # Add an entry to the Tools menu.
        label = self.FEATURE
        self._ui.toolsMenu.add_command(
            label=label,
            image=self._icon,
            compound='left',
            command=start_viewer,
            state='disabled',
        )
        self._ui.toolsMenu.disableOnClose.append(label)

        self._add_help_menu_entry(_('Matrix plugin help'))

        # Add a button to the toolbar.
        self._ui.toolbar.add_separator(),
        self._ui.toolbar.new_button(
            text=_('Matrix'),
            image=self._icon,
            command=start_viewer,
            disableOnLock=False,
        ).pack(side='left')

    def lock(self):
        self.matrixService.lock()

    def on_close(self):
        self.matrixService.on_close()

    def on_quit(self):
        self.matrixService.on_quit()

    def unlock(self):
        self.matrixService.unlock()

