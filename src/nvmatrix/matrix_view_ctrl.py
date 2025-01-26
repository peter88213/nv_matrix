"""Provide a mixin class for a matrix view controller.

Copyright (c) 2025 Peter Triesberger
For further information see https://github.com/peter88213/nv_matrix
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from mvclib.controller.sub_controller import SubController
from nvmatrix.node import Node


class MatrixViewCtrl(SubController):

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

