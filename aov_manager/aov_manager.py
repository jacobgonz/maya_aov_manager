import json
import os

import maya.cmds as cmds

from PySide import QtGui, QtCore

import utils
import pyside_util
import main_ui
import aov_presets_tree
import aov_layers_tree

reload(utils)
reload(pyside_util)
reload(aov_presets_tree)
reload(aov_layers_tree)


class AovManagerDialog(QtGui.QDialog, main_ui.Ui_Form):
    """
    Class for the Aov Manager Dialog
    """
    def __init__(self, parent=None):
        """
        Initialise AovManagerDialog
        Set window flags
        Create content
        :param parent: parent widget
        """
        super(AovManagerDialog, self).__init__(parent)
        self.setupUi(self)

        # Set Window Flags
        pyside_util.set_linux_window_flags(self)

        self._ui_content()

    def _ui_content(self):
        """
        Set the ui content

        :return:
        """

        self.aov_presets = self._get_aov_presets_data()
        self.aov_groups = utils.get_grouped_aovs()

        self.prTreeList = aov_presets_tree.AovPresetsTreeView(self.aov_presets,
                                                              self.aov_groups,
                                                              parent=self)

        self.ly_presets.addWidget(self.prTreeList)

        self.layers_tree = aov_layers_tree.AovLayersTreeView(parent=self)
        self.ly_scene_layers.addWidget(self.layers_tree)

        # Signals
        self.btn_disable.clicked.connect(self._disable_aov_callback)
        self.btn_disable_all.clicked.connect(self._disable_aov_for_all_layers_callback)

        self.btn_refresh.clicked.connect(self._refresh_layers_content)
        self.btn_refresh.setStyleSheet("background-color: #2d8e83")

        self.btn_remove.clicked.connect(self._remove_aov_callback)

        self.prTreeList.connect(self.prTreeList.selectionModel(),
                                QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'),
                                self._select_preset_callback)

        # Icons
        self._set_icons()

        return

    def _set_icons(self):
        """
        Set ui icons

        :return:
        """
        icon_folder = os.path.dirname(os.path.abspath(__file__))
        refresh_path = os.path.join(icon_folder, "icons", "refresh.png")
        trash_path = os.path.join(icon_folder, "icons", "trash.png")

        self.btn_refresh.setIcon(QtGui.QIcon(refresh_path))
        self.btn_remove.setIcon(QtGui.QIcon(trash_path))
        self.btn_remove.setStyleSheet("background-color: #ce2e29")

        return

    def _refresh_layers_content(self):
        """
        Refresh the render layers aov items
        :return:
        """
        self.layers_tree.tree_content()

        return

    def _select_preset_callback(self):
        """
        Callback for selecting a aov preset
        Clear the selection on the render layers tree
        :return:
        """
        self.layers_tree.clearSelection()

        return None

    def _disable_aov_callback(self):
        """
        Callback for disabling an aov on a render layer
        :return:
        """

        selected_items = self.layers_tree.selectedItems()

        if selected_items is None:
            return

        selected_aovs = [x for x in selected_items
                         if x.data(0, QtCore.Qt.UserRole) == "aov"] or None

        if selected_aovs is None:
            return

        invalid_aovs = []

        for aov_item in selected_aovs:
            layer_item = aov_item.parent()
            render_layer = layer_item.data(1, QtCore.Qt.UserRole)

            if render_layer == "masterLayer":
                continue

            aov_name = aov_item.data(1, QtCore.Qt.UserRole)

            # Check the master layer override
            master_value = utils.get_master_layer_value(aov_name)

            # If the aov is Enabled on the master layer we don't disable it
            if master_value:
                invalid_aovs.append(aov_name)
                continue

            # Remove the layer override for the AOV
            cmds.editRenderLayerAdjustment("%s.enabled" % aov_name,
                                           layer=render_layer,
                                           remove=True)

            item_name = aov_item.data(2, QtCore.Qt.UserRole)

            # Remove item from tree
            aov_item.parent().removeChild(aov_item)
            aov_item = None

            layer_data = layer_item.data(2, QtCore.Qt.UserRole)
            layer_data.remove(item_name)
            layer_item.setData(2, QtCore.Qt.UserRole, layer_data)

        if not invalid_aovs:
            return

        # If some AOvs were enabled in the master layer we give
        # the option to fix it
        msg = ("Some AOVS are NOT DISABLED in the master Layer."
               "\n\n AOVS must be disabled in the master Layer to "
               "work with this Tool!")

        pyside_util.display_message_box("ARNOLD AOV MANAGER",
                                        msg,
                                        buttons=QtGui.QMessageBox.Ok,
                                        icon=QtGui.QMessageBox.Warning,
                                        parent=self)

        return

    def _disable_aov_for_all_layers_callback(self):
        """
        Callback for disabling an aov for all the render layers
        :return:
        """

        selected_items = self.layers_tree.selectedItems()

        if selected_items is None:
            return

        selected_aovs = [x for x in selected_items
                         if x.data(0, QtCore.Qt.UserRole) == "aov"] or None

        if selected_aovs is None:
            return

        render_layers = [x for x in cmds.ls(type="renderLayer")
                         if "defaultRenderLayer" not in x]

        for aov_item in selected_aovs:
            aov_name = aov_item.data(1, QtCore.Qt.UserRole)

            # Remove aov layer override for all layers
            for rLayer in render_layers:
                cmds.editRenderLayerAdjustment("%s.enabled" % aov_name,
                                               layer=rLayer,
                                               remove=True)

            # Set the Aov as disabled
            cmds.setAttr("%s.enabled" % aov_name, 0)

        self._refresh_layers_content()

        return

    def _remove_aov_callback(self):
        """
        Callback for removing an aov from the scene
        :return:
        """

        selected_items = self.layers_tree.selectedItems()

        if selected_items is None:
            return

        # Warn the user before going ahead and removing the AOVS from the scene
        title = "DELETE AOVS FROM THE SCENE"
        msg = "Selected AOVS will be DELETED from your scene"
        user_input = pyside_util.display_message_box(title,
                                                     msg,
                                                     buttons=QtGui.QMessageBox.Ok |
                                                             QtGui.QMessageBox.Cancel,
                                                     parent=self)

        if user_input == QtGui.QMessageBox.Cancel:
            return

        selected_aovs = [x for x in selected_items
                         if x.data(0, QtCore.Qt.UserRole) == "aov"] or None

        if selected_aovs is None:
            return

        for aovItem in selected_aovs:
            aov_name = aovItem.data(1, QtCore.Qt.UserRole)

            if cmds.objExists(aov_name):
                cmds.delete(aov_name)

        self._refresh_layers_content()

        return

    def _get_aov_presets_data(self):
        """
        Get the aov presets data used to load presets
        :return:
        """

        presets_folder = os.path.dirname(os.path.abspath(__file__))

        presets_file = os.path.join(presets_folder, "aov_presets_data.json")

        with open(presets_file) as data_file:
            aov_dict = json.load(data_file)

        return aov_dict

    def keyPressEvent(self, event):
        """
        PySide key press event
        Added this to prevent maya shortcut keys to be triggered even
        when we have focus on our widgets
        Example: delete key on system folders was deleting the objects
        selected on maya's outliners

        :param event:
        :return:
        """

        pass


def main():
    """
    Main entry point for the aov manager tool

    :return:
    """

    # Create arnold options before loading the UI
    utils.create_arnold_options()

    parent = pyside_util.get_maya_window_by_name("aov_manager_ui")
    ui = AovManagerDialog(parent=parent)
    ui.show()


if __name__ == '__main__':
    main()
