"""Provide a tkinter widget for relationship table management.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from tkinter import ttk

from nvlib.controller.sub_controller import SubController
from nvlib.gui.observer import Observer
from nvmatrix.node import Node
from nvmatrix.nvmatrix_locale import _
from nvmatrix.platform.platform_settings import KEYS
from nvmatrix.platform.platform_settings import MOUSE
from nvmatrix.platform.platform_settings import PLATFORM
from nvmatrix.relations_table import RelationsTable
from nvmatrix.widgets.table_frame import TableFrame
import tkinter as tk


class MatrixView(tk.Toplevel, Observer, SubController):

    def __init__(self, model, controller, prefs):
        tk.Toplevel.__init__(self)

        self._mdl = model
        self.prefs = prefs
        self.isOpen = True
        if controller.isLocked:
            self.lock()

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
        self.tableFrame = TableFrame(self.mainWindow)

        #--- The Relations Table.
        if self._mdl.novel is not None:
            self._relationsTable = RelationsTable(
                self.tableFrame,
                self._mdl.novel,
                self.prefs,
                self._mdl.nvService.new_hovertip,
            )
            self._relationsTable.set_nodes()
        self.tableFrame.pack(fill='both', expand=True, padx=2, pady=2)

        #--- Initialize the view update mechanism.
        self._skipUpdate = False
        self.bind(MOUSE.TOGGLE_STATE, self._on_element_change)

        # "Show plot lines" checkbox.
        self._showPlotlines = tk.BooleanVar(
            value=self.prefs['show_plot_lines'],
        )
        ttk.Checkbutton(
            self,
            text=_('Plot lines'),
            variable=self._showPlotlines,
            onvalue=True,
            offvalue=False,
            command=self._change_show_plot_lines,
        ).pack(side='left', padx=5, pady=5)

        # "Show characters" checkbox.
        self._showCharacters = tk.BooleanVar(
            value=self.prefs['show_characters'],
        )
        ttk.Checkbutton(
            self,
            text=_('Characters'),
            variable=self._showCharacters,
            onvalue=True,
            offvalue=False,
            command=self._change_show_characters,
        ).pack(side='left', padx=5, pady=5)

        # "Show locations" checkbox.
        self._showLocations = tk.BooleanVar(
            value=self.prefs['show_locations'],
        )
        ttk.Checkbutton(
            self,
            text=_('Locations'),
            variable=self._showLocations,
            onvalue=True,
            offvalue=False,
            command=self._change_show_locations,
        ).pack(side='left', padx=5, pady=5)

        # "Show items" checkbox.
        self._showItems = tk.BooleanVar(
            value=self.prefs['show_items'],
        )
        ttk.Checkbutton(
            self,
            text=_('Items'),
            variable=self._showItems,
            onvalue=True,
            offvalue=False,
            command=self._change_show_items,
        ).pack(side='left', padx=5, pady=5)

        # "Major characters only" checkbox.
        self._majorCharactersOnly = tk.BooleanVar(
            value=self.prefs['major_characters_only'],
        )
        ttk.Checkbutton(
            self,
            text=_('Major characters only'),
            variable=self._majorCharactersOnly,
            onvalue=True,
            offvalue=False,
            command=self._change_major_characters_only,
        ).pack(side='left', padx=5, pady=5)

        # "Close" button.
        ttk.Button(
            self,
            text=_('Close'),
            command=self.on_quit,
        ).pack(side='right', padx=5, pady=5)

    def lock(self):
        """Inhibit element change."""
        Node.isLocked = True

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self.isOpen:
            return

        if self._skipUpdate:
            return

        self.tableFrame.pack_forget()
        self.tableFrame.destroy()
        self.tableFrame = TableFrame(self.mainWindow)
        self.tableFrame.pack(fill='both', expand=True, padx=2, pady=2)
        self._relationsTable.draw_matrix(self.tableFrame)
        self._relationsTable.set_nodes()

    def on_quit(self, event=None):
        self.isOpen = False
        self.prefs['window_geometry'] = self.winfo_geometry()
        self.tableFrame.destroy()
        # this is necessary for deleting the event bindings
        self._mdl.delete_observer(self)
        self.destroy()

    def unlock(self):
        """Enable element change."""
        Node.isLocked = False

    def _change_major_characters_only(self):
        self.prefs['major_characters_only'] = (
            self._majorCharactersOnly.get()
        )
        if self.prefs['show_characters']:
            self.refresh()

    def _change_show_characters(self):
        self.prefs['show_characters'] = (
            self._showCharacters.get()
        )
        self.refresh()

    def _change_show_items(self):
        self.prefs['show_items'] = (
            self._showItems.get()
        )
        self.refresh()

    def _change_show_locations(self):
        self.prefs['show_locations'] = (
            self._showLocations.get()
        )
        self.refresh()

    def _change_show_plot_lines(self):
        self.prefs['show_plot_lines'] = (
            self._showPlotlines.get()
        )
        self.refresh()

    def _on_element_change(self, event=None):
        # Update the model, but not the view.
        self._skipUpdate = True
        self._relationsTable.get_nodes()
        self._skipUpdate = False

