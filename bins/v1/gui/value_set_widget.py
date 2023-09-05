from PyQt6.QtWidgets import *

from . import labeled_line_edit
from . import labeled_spin_box

from bins.v1 import notificator


class ValueSetWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_layout = QHBoxLayout(self)

        self.bits_size = labeled_spin_box.LabeledSpinBox(self)
        self.bits_size.label.setText("Bit size")
        self.bits_size.box.setMinimum(0)
        self.bits_size.box.setMaximum(1000)
        self.bits_size.box.setValue(50)

        self.value = labeled_line_edit.LabeledLineEdit(self)
        self.value.label.setText("Value")

        self.set_button = QPushButton("set")
        self.set_button.clicked.connect(self.set)
        self.set_button.setStyleSheet("""
                border-width: 2px;
                border-style: solid;
                border-color : black;
        """)

        self.revert_button = QPushButton("revert")
        self.revert_button.setStyleSheet("""
                border-width: 2px;
                border-style: solid;
                border-color : black;
        """)

        self.custom_layout.addWidget(self.bits_size)
        self.custom_layout.addWidget(self.value)
        self.custom_layout.addWidget(self.revert_button)
        self.custom_layout.addWidget(self.set_button)

        self.setLayout(self.custom_layout)

    def set(self):
        # c = container.Container()
        notification_provider = notificator.SingletonNotificationProvider()

        notification = notificator.Notification("new.value.set", self)
        notification.bits_size = self.bits_size.box.value()
        notification.value = self.value.edit.text()

        notification_provider.notify(notification)

