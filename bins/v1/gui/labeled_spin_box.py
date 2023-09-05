import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *


class LabeledSpinBox(QWidget):
    # https://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qpushbutton
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_layout = QVBoxLayout(self)

        self.label = QLabel()
        self.label.setStyleSheet("""
                    font-weight: bold;
                    font-size: 10px;
                    font-family: Arial;
                """)
        self.box = QSpinBox()
        self.box.setStyleSheet("""
            QSpinBox {
                border-width: 2px;
                border-style: solid;
                border-color : black;
            }
        """)

        self.custom_layout.addWidget(self.label)
        self.custom_layout.addWidget(self.box)

        self.setLayout(self.custom_layout)

