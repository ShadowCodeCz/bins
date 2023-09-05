from . import app


from PyQt6.QtWidgets import *


class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.drag_position = None

        self.custom_layout = QVBoxLayout(self)
        self.custom_layout.setSpacing(2)
        # self.title = inputs_widget.InputsWidget(self)
        # self.overview = overview_widget.OverviewWidget(self)
        # self.detail = detail_widget.DetailWidget(self)

        # self.custom_layout.addWidget(self.overview)
        # self.custom_layout.addWidget(self.title)
        # self.custom_layout.addWidget(self.detail)

        self.setLayout(self.custom_layout)

        self.setAutoFillBackground(True)
        self.setStyleSheet('background-color: white;')