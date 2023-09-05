import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from . import monitors
from .. import dependecy


class LineEdit(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.custom_layout = None
        self.label = None
        self.box = None
        self.monitor = None

        self.init_layout()
        self.init_styles()

    def init_layout(self):
        self.custom_layout = QVBoxLayout(self)

        self.label = QLabel()
        self.box = QLineEdit()

        self.custom_layout.addWidget(self.label)
        self.custom_layout.addWidget(self.box)

        self.setLayout(self.custom_layout)

    def set_monitor(self, variable_name):
        self.monitor = monitors.LineEditMonitor(variable_name, self.box)

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        # self.setStyleSheet("border: 0px solid black")
        # self.label.setStyleSheet("font-weight: bold; color: gray")
        # self.value.setStyleSheet("font-weight: bold; color: #6495ED")

        self.label.setStyleSheet("font-weight: bold; color: gray")
        self.box.setStyleSheet("border: 1px solid black")

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()

class ComboBox(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.custom_layout = None
        self.label = None
        self.box = None

        self.init_layout()
        self.init_styles()

    def init_layout(self):
        self.custom_layout = QVBoxLayout(self)

        self.label = QLabel()
        self.box = QComboBox()

        self.custom_layout.addWidget(self.label)
        self.custom_layout.addWidget(self.box)

        self.setLayout(self.custom_layout)

    def set_monitor(self, variable_name):
        self.monitor = monitors.ComboBoxMonitor(variable_name, self.box)

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        # self.setStyleSheet("border: 0px solid black")
        # self.label.setStyleSheet("font-weight: bold; color: gray")
        # self.value.setStyleSheet("font-weight: bold; color: #6495ED")

        self.label.setStyleSheet("font-weight: bold; color: gray")
        self.box.setStyleSheet("border: 1px solid black")
        # TODO: Button styling
        self.box.setMinimumWidth(100)

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()


class SpinBox(QWidget):
    # https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qpushbutton
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.custom_layout = None
        self.label = None
        self.box = None

        self.init_layout()
        self.init_styles()

    def init_layout(self):
        self.custom_layout = QVBoxLayout(self)

        self.label = QLabel()
        self.box = QSpinBox()

        self.custom_layout.addWidget(self.label)
        self.custom_layout.addWidget(self.box)

        self.setLayout(self.custom_layout)

        self.box.setMinimum(-1000)
        self.box.setMaximum(1000)
        self.box.setMinimumWidth(50)

    def set_monitor(self, variable_name):
        self.monitor = monitors.SpinBoxMonitor(variable_name, self.box)

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        # self.setStyleSheet("border: 0px solid black")
        # self.label.setStyleSheet("font-weight: bold; color: gray")
        # self.value.setStyleSheet("font-weight: bold; color: #6495ED")

        self.label.setStyleSheet("font-weight: bold; color: gray")
        self.box.setStyleSheet("border: 1px solid black")
        # TODO: Arrows styling
        # self.box.setMinimumWidth(100)

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()


class ValueWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_layout = QHBoxLayout(self)

        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.label = QLabel()
        self.value = QLabel()

        self.init_layout()
        self.init_styles()

    def init_layout(self):
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        # self.setContentsMargins(1, 1, 1, 1)
        # self.custom_layout.setSpacing(1)
        self.custom_layout.addWidget(self.label)
        self.custom_layout.addWidget(self.value)

        self.setLayout(self.custom_layout)

    # def set_styles(self):
    #     # font = QFont("Arial", 10)
    #     # font.setBold(True)
    #     # self.value.setFont(font)

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        self.setStyleSheet("border: 0px solid black")
        self.label.setStyleSheet("font-weight: bold; color: gray")
        self.value.setStyleSheet("font-weight: bold; color: #6495ED")

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()



class PushButton(QPushButton):
    # TODO: Button monitor
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.setContentsMargins(0,0,0,0)

        self.setStyleSheet("""
            QPushButton {
                background-color: #E5E7E9;
                border-style: solid;
                border-width: 1px;
                border-color: gray;
                padding: 10px 30px 10px 30px;
                margin: 0px;
            }
        """)

