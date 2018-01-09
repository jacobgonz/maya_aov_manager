import json

import maya.cmds as cmds

from PySide import QtGui, QtCore

import utils
import pyside_util


class AovTreeItem(QtGui.QTreeWidgetItem):
    """
    Class to create an TreeWidgetItem for the aovs added to the render layers
    tree items
    """
    def __init__(self, aov, parent, tree):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.tree = tree

        font = QtGui.QFont()
        font.setPointSize(10)

        self.setText(0, aov)
        self.setFont(0, font)

        self.setData(0, QtCore.Qt.UserRole, "aov")
        self.setData(1, QtCore.Qt.UserRole, "aiAOV_%s" % aov)
        self.setData(2, QtCore.Qt.UserRole, aov)


class AovLayersTreeView(QtGui.QTreeWidget):
    """
    Class to create an TreeWidget for the render layer aovs tree
    """
    def __init__(self, parent=None):
        """
        Initialise the Tree Widget
        Ui settings and content

        :param parent: parent widget
        """
        super(AovLayersTreeView, self).__init__(parent)
        self.ui = parent

        self._ui_settings()

        self.tree_content()

    def _ui_settings(self):
        """
        UI settings for the tree widget.
        Setup the header text
        Drag an drop mode
        Selection mode

        :return:
        """
        self.headerItem().setText(0, "RENDER LAYERS")

        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.IgnoreAction)

        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        return

    def tree_content(self):
        """
        Set the tree content

        :return:
        """

        self.clear()

        layer_aovs = utils.get_layers_aovs()

        for render_layer in sorted(layer_aovs):
            aov_list = layer_aovs[render_layer]
            self._add_layer_aov_child_items(render_layer, aov_list)

        scene_aovs = utils.get_scene_aovs()

        master_layer_aovs = self._add_layer_aov_child_items("masterLayer",
                                                            scene_aovs)

        master_layer_aovs.setFlags(QtCore.Qt.ItemIsEnabled |
                                   QtCore.Qt.ItemIsDragEnabled)

        master_layer_aovs.setExpanded(True)

        return None

    def _add_layer_aov_child_items(self, render_layer, aov_list):
        """
        Add a layer tree item and it's child aov tree items

        :param render_layer: the name of the render layer as a string
        :param aov_list: a list of aovs
        :return:
        """

        layer_tree_item = QtGui.QTreeWidgetItem(self)

        font = QtGui.QFont()
        font.setPointSize(11)

        layer_tree_item.setText(0, render_layer)
        layer_tree_item.setFont(0, font)

        layer_tree_item.setData(0, QtCore.Qt.UserRole, "layer")
        layer_tree_item.setData(1, QtCore.Qt.UserRole, render_layer)

        layer_tree_item.setFlags(QtCore.Qt.ItemIsEnabled |
                                 QtCore.Qt.ItemIsDragEnabled)

        layer_tree_item.setIcon(0, QtGui.QIcon(":/layerEditor.png"))

        for aov in aov_list:
            if aov == "beauty":
                continue

            AovTreeItem(aov, layer_tree_item, self)

        layer_tree_item.setData(2, QtCore.Qt.UserRole, aov_list)

        return layer_tree_item

    def dragEnterEvent(self, event):
        """
        PySide drag enter event
        :param event:
        :return:
        """
        event.accept()

        return None

    def dropEvent(self, event):
        """
        PySide drop event
        :param event:
        :return:
        """
        drop_parent = self.itemAt(event.pos())
        drop_parent = self.invisibleRootItem() if drop_parent is None else drop_parent

        if drop_parent is None:
            event.ignore()
            return

        if drop_parent.data(0, QtCore.Qt.UserRole) != "layer":
            event.ignore()
            return

        selected_items = [x for x in self.selectedItems()
                          if x.data(0, QtCore.Qt.UserRole) != "layer"] or None

        if selected_items is None:
            mimedata = event.mimeData()

            if mimedata.hasFormat('application/leftdrag'):
                drop_items = str(mimedata.data('application/leftdrag'))
            elif mimedata.hasFormat("application/selfdrop"):
                drop_items = str(mimedata.data('application/selfdrop'))
            else:
                event.ignore()
                return

            drop_list = json.loads(drop_items)

        else:
            drop_list = []

            for item in selected_items:
                if item.data(0, QtCore.Qt.UserRole) == "layer":
                    continue

                aov_dict = dict()

                aov_dict["ui_Name"] = item.text(0)
                aov_dict["aov_Name"] = item.data(1, QtCore.Qt.UserRole)
                aov_dict["type"] = item.data(2, QtCore.Qt.UserRole)
                aov_dict["data"] = item.data(3, QtCore.Qt.UserRole)

                drop_list.append(aov_dict)

        render_layer = drop_parent.data(1, QtCore.Qt.UserRole)
        layer_aovs = drop_parent.data(2, QtCore.Qt.UserRole)

        # FIXME: switch to the master render layer to manage AOVS
        # Need to avoid this
        # Doing this because maya cmds does not return the overrides made
        # on a layer until a layer switch has been made
        user_render_layer = cmds.editRenderLayerGlobals(query=True, crl=True)

        if user_render_layer != "defaultRenderLayer":

            # Warning to the user that we are switching to the master Layer
            msg = ("AOV MANAGER needs to switch to the MASTER LAYER "
                   "to setup your AOVS")

            pyside_util.display_message_box("ARNOLD AOV MANAGER",
                                            msg,
                                            buttons=QtGui.QMessageBox.Ok,
                                            parent=self)

        # Switch to the master layer
        cmds.editRenderLayerGlobals(currentRenderLayer="defaultRenderLayer")

        for aovDict in drop_list:
            ui_name = aovDict.get("ui_Name", None)
            node_name = aovDict.get("aov_Name", None)
            aov_type = aovDict.get("type", None)
            data_type = aovDict.get("data", None)

            if ui_name not in layer_aovs and ui_name is not None:
                AovTreeItem(ui_name, drop_parent, self)
                utils.add_aov_to_render_layer(ui_name,
                                              node_name,
                                              render_layer,
                                              aov_type,
                                              data_type=data_type)

                layer_aovs.append(ui_name)

                if render_layer != "masterLayer":
                    master_layer_item = self.findItems("masterLayer",
                                                       QtCore.Qt.MatchExactly |
                                                       QtCore.Qt.MatchRecursive,
                                                       0)[0]

                    master_layer_aovs = master_layer_item.data(2,
                                                               QtCore.
                                                               Qt.UserRole)

                    if ui_name not in master_layer_aovs:
                        AovTreeItem(ui_name, master_layer_item, self)
                        master_layer_aovs.append(ui_name)
                        master_layer_item.setData(2,
                                                  QtCore.Qt.UserRole,
                                                  master_layer_aovs)

            # Set the drop parent as expanded
            drop_parent.setExpanded(True)

            # Set the drop parent data
            drop_parent.setData(2, QtCore.Qt.UserRole, layer_aovs)

        event.accept()

        return None
