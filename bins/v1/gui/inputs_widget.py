from PyQt6.QtWidgets import *

from . import configuration_widget
from . import value_set_widget


class InputsWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inputs_visible = True

        self.custom_layout = QVBoxLayout(self)
        # self.button = QPushButton("Binary Insight")
        # self.button.clicked.connect(self.hide_and_show)
        # self.button.setStyleSheet("""
        #     background-color: gray;
        #     border-style: outset;
        #     border-width: 0px;
        #     border-color: black;
        #     font-weight: bold;
        #     font-size: 30px;
        #     font-family: Arial;
        # """)
        # self.custom_layout.addWidget(self.button)

        self.inputs_frame = QFrame(self)
        self.inputs_frame_layout = QVBoxLayout(self)

        self.configuration = configuration_widget.ConfigurationWidget(self)
        self.set_value = value_set_widget.ValueSetWidget(self)

        self.inputs_frame_layout.addWidget(self.configuration)
        self.inputs_frame_layout.addWidget(self.set_value)
        self.inputs_frame.setLayout(self.inputs_frame_layout)

        self.custom_layout.addWidget(self.inputs_frame)

        self.setLayout(self.custom_layout)

    def hide_and_show(self, notification):
        if self.inputs_visible:
            self.inputs_frame.hide()
            self.inputs_visible = False
        else:
            self.inputs_frame.show()
            self.inputs_visible = True