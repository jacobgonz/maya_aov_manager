import maya.cmds as cmds

import maya.OpenMayaUI as apiUI

from PySide import QtCore
from PySide import QtGui

from shiboken import wrapInstance


def get_maya_window_by_name(maya_dialog):
    """

    :param maya_dialog: the QtDialog to query
    :return: the parent window
    """

    if cmds.window(maya_dialog, exists=True):
        cmds.deleteUI(maya_dialog, window=True)

    maya_win_name = cmds.window(maya_dialog)

    parent_win_pointer = apiUI.MQtUtil.findWindow(maya_win_name)
    parent_win = wrapInstance(long(parent_win_pointer),
                              QtGui.QWidget)

    return parent_win


def display_message_box(window_title,
                        text,
                        info_text=None,
                        detail_text=None,
                        icon=QtGui.QMessageBox.Information,
                        buttons=QtGui.QMessageBox.Ok,
                        parent=None):

    """

    :param window_title: the window title as a string
    :param text: the text to display as a string
    :param info_text: the info text as a string
    :param detail_text: the detail text as a string
    :param icon: the icon as a Qt object
    :param buttons: the buttons to use as Qt objects
    :param parent: the window parent
    :return: the message box
    """

    message_box = QtGui.QMessageBox(parent)
    message_box.setIcon(icon)
    message_box.setWindowTitle(window_title + "\t\t\t\t")
    message_box.setText(text)

    if info_text is not None:
        message_box.setInformativeText(info_text)

    if detail_text is not None:
        message_box.setDetailedText(detail_text)

    message_box.setStandardButtons(buttons)

    return message_box.exec_()


def move_widget_screen_center(widget_object):
    """

    :param widget_object: the widget to move
    :return:
    """

    active_screen = QtGui.QDesktopWidget().screenNumber(QtGui.QCursor.pos())
    screen = QtGui.QDesktopWidget().screenGeometry(active_screen)

    widget_object.move(screen.center() - widget_object.rect().center())

    return


def set_linux_window_flags(dialog, modal=False):
    """

    :param dialog: the dialog Qt object
    :param modal: bool for the modal option
    :return:
    """

    if modal:
        dialog.setModal(True)
    else:
        # Force Close/Minimize button for linux window
        dialog.setWindowFlags(QtCore.Qt.Window |
                              QtCore.Qt.WindowCloseButtonHint |
                              QtCore.Qt.WindowMinimizeButtonHint)

    # Move to center of the screen
    move_widget_screen_center(dialog)

    return
