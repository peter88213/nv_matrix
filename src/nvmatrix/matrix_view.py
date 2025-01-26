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
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import PL_ROOT


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

    def build_tree(self):
        columns = []
        headings = []
        novel = self._mdl.novel

        # First row: column headers
        for plId in novel.tree.get_children(PL_ROOT):
            columns.append(plId)
            headings.append(novel.plotLines[plId].title)
        for crId in novel.tree.get_children(CR_ROOT):
            columns.append(crId)
            headings.append(novel.characters[crId].title)
        for lcId in novel.tree.get_children(LC_ROOT):
            columns.append(lcId)
            headings.append(novel.locations[lcId].title)
        for itId in novel.tree.get_children(IT_ROOT):
            columns.append(itId)
            headings.append(novel.items[itId].title)
        self.tree.configure(columns=tuple(columns), selectmode='none')
        for i, elemId in enumerate(columns):
            self.tree.column(elemId)
            self.tree.heading(elemId, text=headings[i], anchor='w')

        for chId in novel.tree.get_children(CH_ROOT):
            if self._mdl.novel.chapters[chId].chType != 0:
                continue

            columns.clear()
            for scId in novel.tree.get_children(chId):
                if novel.sections[scId].scType != 0:
                    continue

                for plId in novel.tree.get_children(PL_ROOT):
                    if plId in novel.sections[scId].scPlotLines:
                        columns.append('P')
                    else:
                        columns.append('')
                for crId in novel.tree.get_children(CR_ROOT):
                    if crId in novel.sections[scId].characters:
                        columns.append('C')
                    else:
                        columns.append('')
                for lcId in novel.tree.get_children(LC_ROOT):
                    if lcId in novel.sections[scId].locations:
                        columns.append('L')
                    else:
                        columns.append('')
                for itId in novel.tree.get_children(IT_ROOT):
                    if itId in novel.sections[scId].items:
                        columns.append('I')
                    else:
                        columns.append('')
                self.tree.insert('', 'end', scId, values=columns)

    def refresh(self):
        """Refresh the view after changes have been made "outsides"."""
        if not self.isOpen:
            return

        if self._skipUpdate:
            return

