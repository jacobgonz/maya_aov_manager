# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/mill3d/users/jacobg/python_projects/maya_aov_manager/aov_manager/designer/main_ui.ui'
#
# Created: Tue Jan  9 16:49:12 2018
#      by: pyside-uic 0.2.14 running on PySide 1.2.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 569)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(750, 0))
        Form.setMaximumSize(QtCore.QSize(750, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.wg_main = QtGui.QWidget(Form)
        self.wg_main.setObjectName("wg_main")
        self.horizontalLayout = QtGui.QHBoxLayout(self.wg_main)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.wg_presets = QtGui.QWidget(self.wg_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_presets.sizePolicy().hasHeightForWidth())
        self.wg_presets.setSizePolicy(sizePolicy)
        self.wg_presets.setMinimumSize(QtCore.QSize(250, 0))
        self.wg_presets.setObjectName("wg_presets")
        self.ly_presets_wg = QtGui.QVBoxLayout(self.wg_presets)
        self.ly_presets_wg.setContentsMargins(0, 0, 0, 0)
        self.ly_presets_wg.setObjectName("ly_presets_wg")
        self.ly_presets = QtGui.QHBoxLayout()
        self.ly_presets.setSpacing(0)
        self.ly_presets.setObjectName("ly_presets")
        self.ly_presets_wg.addLayout(self.ly_presets)
        self.horizontalLayout.addWidget(self.wg_presets)
        self.line = QtGui.QFrame(self.wg_main)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.wg_layers = QtGui.QWidget(self.wg_main)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_layers.sizePolicy().hasHeightForWidth())
        self.wg_layers.setSizePolicy(sizePolicy)
        self.wg_layers.setMinimumSize(QtCore.QSize(300, 0))
        self.wg_layers.setObjectName("wg_layers")
        self.ly_layers_wg = QtGui.QVBoxLayout(self.wg_layers)
        self.ly_layers_wg.setContentsMargins(0, 0, 0, 0)
        self.ly_layers_wg.setObjectName("ly_layers_wg")
        self.ly_scene_layers = QtGui.QHBoxLayout()
        self.ly_scene_layers.setSpacing(0)
        self.ly_scene_layers.setObjectName("ly_scene_layers")
        self.ly_layers_wg.addLayout(self.ly_scene_layers)
        self.fr_btns = QtGui.QFrame(self.wg_layers)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_btns.sizePolicy().hasHeightForWidth())
        self.fr_btns.setSizePolicy(sizePolicy)
        self.fr_btns.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fr_btns.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_btns.setObjectName("fr_btns")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.fr_btns)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ly_btns = QtGui.QHBoxLayout()
        self.ly_btns.setObjectName("ly_btns")
        self.btn_disable = QtGui.QPushButton(self.fr_btns)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_disable.sizePolicy().hasHeightForWidth())
        self.btn_disable.setSizePolicy(sizePolicy)
        self.btn_disable.setMinimumSize(QtCore.QSize(250, 0))
        self.btn_disable.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btn_disable.setFont(font)
        self.btn_disable.setObjectName("btn_disable")
        self.ly_btns.addWidget(self.btn_disable)
        self.btn_disable_all = QtGui.QPushButton(self.fr_btns)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btn_disable_all.setFont(font)
        self.btn_disable_all.setObjectName("btn_disable_all")
        self.ly_btns.addWidget(self.btn_disable_all)
        self.verticalLayout_4.addLayout(self.ly_btns)
        self.ly_layers_wg.addWidget(self.fr_btns)
        self.line_bottom = QtGui.QFrame(self.wg_layers)
        self.line_bottom.setFrameShape(QtGui.QFrame.HLine)
        self.line_bottom.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_bottom.setObjectName("line_bottom")
        self.ly_layers_wg.addWidget(self.line_bottom)
        self.fr_btns_bottom = QtGui.QFrame(self.wg_layers)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fr_btns_bottom.sizePolicy().hasHeightForWidth())
        self.fr_btns_bottom.setSizePolicy(sizePolicy)
        self.fr_btns_bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        self.fr_btns_bottom.setFrameShadow(QtGui.QFrame.Raised)
        self.fr_btns_bottom.setObjectName("fr_btns_bottom")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.fr_btns_bottom)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ly_btns_bottom = QtGui.QHBoxLayout()
        self.ly_btns_bottom.setObjectName("ly_btns_bottom")
        self.btn_remove = QtGui.QPushButton(self.fr_btns_bottom)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_remove.sizePolicy().hasHeightForWidth())
        self.btn_remove.setSizePolicy(sizePolicy)
        self.btn_remove.setMinimumSize(QtCore.QSize(250, 0))
        self.btn_remove.setMaximumSize(QtCore.QSize(250, 40))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.btn_remove.setFont(font)
        self.btn_remove.setObjectName("btn_remove")
        self.ly_btns_bottom.addWidget(self.btn_remove)
        self.btn_refresh = QtGui.QPushButton(self.fr_btns_bottom)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_refresh.sizePolicy().hasHeightForWidth())
        self.btn_refresh.setSizePolicy(sizePolicy)
        self.btn_refresh.setMaximumSize(QtCore.QSize(250, 40))
        self.btn_refresh.setObjectName("btn_refresh")
        self.ly_btns_bottom.addWidget(self.btn_refresh)
        self.verticalLayout_5.addLayout(self.ly_btns_bottom)
        self.ly_layers_wg.addWidget(self.fr_btns_bottom)
        self.horizontalLayout.addWidget(self.wg_layers)
        self.verticalLayout.addWidget(self.wg_main)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "AOV MANAGER", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_disable.setText(QtGui.QApplication.translate("Form", "Disable AOVS on SELECTED Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_disable_all.setText(QtGui.QApplication.translate("Form", "Disable AOVs on All Layers", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_remove.setText(QtGui.QApplication.translate("Form", "Remove AOVS From Scene", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_refresh.setText(QtGui.QApplication.translate("Form", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
