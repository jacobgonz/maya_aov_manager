import json

from PySide import QtGui, QtCore


class AovPresetItem(QtGui.QTreeWidgetItem):
    """
    Class to create an TreeWidgetItem for the aovs added to the presets
    tree view

    """
    def __init__(self,
                 ui_name,
                 aov_name,
                 aov_type,
                 data_type,
                 edit,
                 parent,
                 tree):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.tree = tree

        font = QtGui.QFont()
        font.setPointSize(10)

        self.setText(0, ui_name)
        self.setText(1, aov_type)
        self.setFont(0, font)

        self.setData(0, QtCore.Qt.UserRole, "aov_pr")
        self.setData(1, QtCore.Qt.UserRole, aov_name)
        self.setData(2, QtCore.Qt.UserRole, aov_type)
        self.setData(3, QtCore.Qt.UserRole, data_type)

        if edit:
            self.setFlags(QtCore.Qt.ItemIsEditable |
                          QtCore.Qt.ItemIsEnabled |
                          QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsDragEnabled)
        else:
            self.setFlags(QtCore.Qt.ItemIsEnabled |
                          QtCore.Qt.ItemIsSelectable |
                          QtCore.Qt.ItemIsDragEnabled)


class AovPresetsTreeView(QtGui.QTreeWidget):
    """
    Tree Widget Class to create the aov presets tree
    """
    def __init__(self, aov_presets, aov_groups, parent=None):
        """
        Initialise Tree Widget
        Create variables
        Ui settings and tree content

        :param aov_presets: dictionary for the aov presets data
        :param aov_groups: dictionary for the aov groups data
        :param parent: parent widget
        """
        super(AovPresetsTreeView, self).__init__(parent)

        self.ui = parent

        self.aov_presets = aov_presets
        self.aov_groups = aov_groups

        self._ui_settings()

        self._tree_content()

    def _ui_settings(self):
        """
        UI settings for the tree widget.
        Setup the header text and size
        Drag an drop mode
        Selection mode

        :return:
        """

        # Header text
        self.headerItem().setText(0, "AOV PRESETS")

        # Header size
        self.header().resizeSection(0, 180)

        self.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.IgnoreAction)

        # Selection mode
        self.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

        return

    def _tree_content(self):
        """
        Set the tree content

        :return:
        """

        self.clear()

        font = QtGui.QFont()
        font.setPointSize(10)

        for aov_group in self.aov_presets.keys():
            self._add_aov_group_item(self.aov_presets, aov_group)

        for aov_group in self.aov_groups.keys():
            self._add_aov_group_item(self.aov_groups, aov_group)

        return

    def _add_aov_group_item(self, aov_list, aov_group):
        """


        :param aov_list:
        :param aov_group:
        :return:
        """

        group_item = QtGui.QTreeWidgetItem(self)

        group_item.setText(0, aov_group)

        for aov_data in aov_list[aov_group]:
            ui_name = aov_data.get("ui_Name", None)
            aov_name = aov_data.get("aov_Name", None)
            edit = aov_data.get("edit", False)
            aov_type = aov_data.get("type", "")
            data_type = aov_data.get("data", None)

            if ui_name is None or aov_name is None:
                continue

            AovPresetItem(ui_name,
                          aov_name,
                          aov_type,
                          data_type,
                          edit,
                          group_item,
                          self)

        return

    def dragEnterEvent(self, event):
        """
        PySide drag enter event

        :param event:
        :return:
        """

        md = event.mimeData()

        selected_aov_items = [x for x in self.selectedItems()
                              if "aov" in x.data(0, QtCore.Qt.UserRole)] or None

        if selected_aov_items is None:
            event.ignore()
            return

        aov_list = []

        for aov in selected_aov_items:
            aov_dict = dict()

            ui_name = aov.text(0)

            # FIXME: temp solution for id aov name changed
            aov_name = "aiAOV_%s" % aov.text(0)
            # aov_name = aov.data(1, QtCore.Qt.UserRole)\

            aov_type = aov.data(2, QtCore.Qt.UserRole)
            data_type = aov.data(3, QtCore.Qt.UserRole)

            aov_dict["ui_Name"] = ui_name
            aov_dict["aov_Name"] = aov_name
            aov_dict["type"] = aov_type
            aov_dict["data"] = data_type

            aov_list.append(aov_dict)

        ba = QtCore.QByteArray(json.dumps(aov_list))
        md.setData("application/leftdrag", ba)
        event.accept()

    def dropEvent(self, event):
        """
        PySide drop event
        :param event:
        :return:
        """

        mimedata = event.mimeData()

        if mimedata.hasFormat('application/leftdrag'):
            drop_name = str(mimedata.data('application/leftdrag'))
        elif mimedata.hasFormat("application/selfdrop"):
            drop_name = str(mimedata.data('application/selfdrop'))
        else:
            event.ignore()
            return

        json.loads(drop_name)

        event.accept()

        return None
