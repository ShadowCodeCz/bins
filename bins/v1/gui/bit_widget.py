from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from bins.v1 import notificator


class BitWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notification_provider = notificator.SingletonNotificationProvider()
        self.notification_provider.subscribe("absolute.position.modifier.change", self.absolute_position_modifier_change)
        self.notification_provider.subscribe("block.position.modifier.change", self.block_position_modifier_change)

        self.absolute_position_modifier = 0
        self.block_position_modifier = 0

        self.color_index = 0
        self.colors = ["gray", "red", "green", "blue", "violet", "orange"]

        self.block = None
        self.bit = None
        self.custom_layout = QVBoxLayout(self)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.absolute_position = QLabel()
        self.value = QLabel()

        font = QFont("Arial", 18)
        # font = QFont("Arial", 12)
        font.setBold(True)
        self.value.setFont(font)

        self.block_position = QLabel()

        self.custom_layout.addWidget(self.absolute_position)
        self.custom_layout.addWidget(self.value)
        self.custom_layout.addWidget(self.block_position)

        self.setLayout(self.custom_layout)

    def set_bit(self, bit):
        self.bit = bit
        self.absolute_position.setText(str(bit.absolute_position + self.absolute_position_modifier))
        self.value.setText(str(bit.value))
        self.block_position.setText(str(bit.block_position + self.block_position_modifier))

    def mousePressEvent(self, event):
        self.color_index += 1
        self.color_index = self.color_index % len(self.colors)
        self.color = self.colors[self.color_index]

        width = 0 if self.color_index == 0 else 1

        self.setStyleSheet(f"background-color:{self.color}; border: {width}px solid black")
        self.absolute_position.setStyleSheet("border-width: 0px")
        self.value.setStyleSheet("border-width: 0px")
        self.block_position.setStyleSheet("border-width: 0px")

    def absolute_position_modifier_change(self, notification):
        try:
            self.absolute_position_modifier = int(notification.value)
            self.absolute_position.setText(str(self.bit.absolute_position + self.absolute_position_modifier))
        except Exception as e:
            self.absolute_position_modifier = 0

    def block_position_modifier_change(self, notification):
        try:
            self.block_position_modifier = int(notification.value)
            self.block_position.setText(str(self.bit.block_position + self.block_position_modifier))
        except Exception as e:
            self.block_position_modifier = 0