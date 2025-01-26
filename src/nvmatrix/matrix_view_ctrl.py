"""Provide a mixin class for a matrix view controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvmatrix.node import Node
from nvlib.novx_globals import CH_ROOT
from nvlib.novx_globals import CR_ROOT
from nvlib.novx_globals import IT_ROOT
from nvlib.novx_globals import LC_ROOT
from nvlib.novx_globals import PL_ROOT


class MatrixViewCtrl(SubController):

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

    def initialize_controller(self, model, view, controller, prefs):
        SubController.initialize_controller(self, model, view, controller)
        self.prefs = prefs
        self.isOpen = True
        if self._ctrl.isLocked:
            self.lock()

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
        self.prefs['window_geometry'] = self.winfo_geometry()
        self.tree.destroy()
        # this is necessary for deleting the event bindings
        self._mdl.delete_observer(self)
        self.destroy()

    def unlock(self):
        """Enable element change."""
        Node.isLocked = False

