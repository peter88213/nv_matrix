"""Provide a service class for the relationship matrix viewer.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from pathlib import Path

from nvlib.controller.sub_controller import SubController
from nvlib.gui.set_icon_tk import set_icon
from nvmatrix.matrix_view import MatrixView


class MatrixService(SubController):
    INI_FILENAME = 'matrix.ini'
    INI_FILEPATH = '.novx/config'
    SETTINGS = dict(
        window_geometry='600x800',
        color_bg_00='gray80',
        color_bg_01='gray85',
        color_bg_10='gray95',
        color_bg_11='white',
        color_plotline_heading='deepSkyBlue',
        color_plotline_node='deepSkyBlue3',
        color_character_heading='goldenrod1',
        color_character_node='goldenrod3',
        color_location_heading='coral1',
        color_location_node='coral3',
        color_item_heading='aquamarine1',
        color_item_node='aquamarine3',
    )
    OPTIONS = {}

    def __init__(self, model, view, controller):
        self._mdl = model
        self._ui = view
        self._ctrl = controller
        self._matrixViewer = None

        #--- Load configuration.
        try:
            homeDir = str(Path.home()).replace('\\', '/')
            configDir = f'{homeDir}/{self.INI_FILEPATH}'
        except:
            configDir = '.'
        self.iniFile = f'{configDir}/{self.INI_FILENAME}'
        self.configuration = self._mdl.nvService.new_configuration(
            settings=self.SETTINGS,
            options=self.OPTIONS
            )
        self.configuration.read(self.iniFile)
        self.prefs = {}
        self.prefs.update(self.configuration.settings)
        self.prefs.update(self.configuration.options)

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
        for keyword in self.prefs:
            if keyword in self.configuration.options:
                self.configuration.options[keyword] = self.prefs[keyword]
            elif keyword in self.configuration.settings:
                self.configuration.settings[keyword] = self.prefs[keyword]
        self.configuration.write(self.iniFile)

    def unlock(self):
        """Enable changes on the model.
        
        Overrides the superclass method.
        """
        if self._matrixViewer:
            self._matrixViewer.unlock()

    def start_viewer(self, windowTitle):
        if not self._mdl.prjFile:
            return

        if self._matrixViewer:
            if self._matrixViewer.isOpen:
                if self._matrixViewer.state() == 'iconic':
                    self._matrixViewer.state('normal')
                self._matrixViewer.lift()
                self._matrixViewer.focus()
                return

        self._matrixViewer = MatrixView(
            self._mdl,
            self._ctrl,
            self.prefs,
        )
        self._matrixViewer.title(f'{self._mdl.novel.title} - {windowTitle}')
        set_icon(self._matrixViewer, icon='mLogo32', default=False)

