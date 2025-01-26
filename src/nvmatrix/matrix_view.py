"""Provide a tkinter widget for relationship table management.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvmatrix.matrix_view_ctrl import MatrixViewCtrl
from mvclib.view.observer import Observer
from nvmatrix.nvmatrix_locale import _
from nvmatrix.platform.platform_settings import KEYS
from nvmatrix.platform.platform_settings import MOUSE
from nvmatrix.platform.platform_settings import PLATFORM
import tkinter as tk


class MatrixView(tk.Toplevel, Observer, MatrixViewCtrl):

    def __init__(self, model, view, controller, prefs):
        tk.Toplevel.__init__(self)

        MatrixViewCtrl.initialize_controller(self, model, view, controller, prefs)

        self.geometry(self.prefs['window_geometry'])
        self.lift()
        self.focus()

        #--- Register this view component.
        self._mdl.add_observer(self)

        #--- Event bindings.
        if PLATFORM != 'win':
            self.bind(KEYS.QUIT_PROGRAM[0], self.on_quit)
        self.protocol("WM_DELETE_WINDOW", self.on_quit)

        #--- Main menu.
        self.mainMenu = tk.Menu(self)
        self.config(menu=self.mainMenu)

        #--- Main window and table frame.
        self.mainWindow = ttk.Frame(self)
        self.mainWindow.pack(fill='both', expand=True)

        #--- The Relations tree.
        if self._mdl.novel is None:
            return

        # Create a novel tree.
        self.tree = ttk.Treeview(self.mainWindow)
        scrollX = ttk.Scrollbar(self.mainWindow, orient='horizontal', command=self.tree.xview)
        scrollY = ttk.Scrollbar(self.tree, orient='vertical', command=self.tree.yview)
        self.tree.configure(xscrollcommand=scrollX.set)
        self.tree.configure(yscrollcommand=scrollY.set)
        scrollX.pack(side='bottom', fill='x')
        scrollY.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

        #--- Add columns to the tree.
        self.build_tree()

        #--- Initialize the view update mechanism.
        self._skipUpdate = False
        # self.bind(MOUSE.TOGGLE_STATE, self.on_element_change)

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self.isOpen:
            return

        if self._skipUpdate:
            return

