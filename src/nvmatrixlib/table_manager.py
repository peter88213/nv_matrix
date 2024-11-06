"""Provide a tkinter widget for relationship table management.

Copyright (c) 2024 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from mvclib.controller.sub_controller import SubController
from mvclib.view.observer import Observer
from nvmatrixlib.node import Node
from nvmatrixlib.nvmatrix_globals import _
from nvmatrixlib.platform.platform_settings import KEYS
from nvmatrixlib.platform.platform_settings import MOUSE
from nvmatrixlib.platform.platform_settings import PLATFORM
from nvmatrixlib.relations_table import RelationsTable
from nvmatrixlib.widgets.table_frame import TableFrame
import tkinter as tk


class TableManager(SubController, Observer, tk.Toplevel):

    def __init__(self, model, view, controller, manager, **kwargs):
        SubController.__init__(self, model, view, controller)
        tk.Toplevel.__init__(self)

        self._manager = manager
        self._kwargs = kwargs

        self._statusText = ''

        self.geometry(kwargs['window_geometry'])
        self.lift()
        self.focus()

        #--- Register this view component.
        self._ui.register_client(self)
        if self._ctrl.isLocked:
            self.lock()

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
        self.tableFrame = TableFrame(self.mainWindow)

        #--- The Relations Table.
        if self._mdl.novel is not None:
            self._relationsTable = RelationsTable(self.tableFrame, self._mdl.novel, **self._kwargs)
            self._relationsTable.set_nodes()
        self.isOpen = True
        self.tableFrame.pack(fill='both', expand=True, padx=2, pady=2)

        #--- Initialize the view update mechanism.
        self._skipUpdate = False
        self.bind(MOUSE.TOGGLE_STATE, self.on_element_change)

        # "Close" button.
        ttk.Button(self, text=_('Close'), command=self.on_quit).pack(side='right', padx=5, pady=5)

    def lock(self):
        """Inhibit element change."""
        Node.isLocked = True

    def on_element_change(self, event=None):
        """Update the model, but not the view."""
        self._skipUpdate = True
        self._relationsTable.get_nodes()
        self._skipUpdate = False

    def on_quit(self, event=None):
        self.isOpen = False
        self._manager.kwargs['window_geometry'] = self.winfo_geometry()
        self.tableFrame.destroy()
        # this is necessary for deleting the event bindings
        self._ui.unregister_client(self)
        self.destroy()

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if self.isOpen:
            if not self._skipUpdate:
                self.tableFrame.pack_forget()
                self.tableFrame.destroy()
                self.tableFrame = TableFrame(self.mainWindow)
                self.tableFrame.pack(fill='both', expand=True, padx=2, pady=2)
                self._relationsTable.draw_matrix(self.tableFrame)
                self._relationsTable.set_nodes()

    def unlock(self):
        """Enable element change."""
        Node.isLocked = False

