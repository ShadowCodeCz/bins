from PyQt6.QtWidgets import *

from bins.v1 import notificator


# from .. import container


class OverviewWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setStyleSheet("""
                background-color: #505050;
                border-width: 2px;
                border-style: solid;
                border-color: black;
        """)

        self.custom_layout = QHBoxLayout()

        self.bin_label = QLabel()
        self.bin_label.setStyleSheet("border-width: 0px;")

        self.oct_label = QLabel()
        self.oct_label.setStyleSheet("border-width: 0px;")

        self.dec_label = QLabel()
        self.dec_label.setStyleSheet("border-width: 0px;")

        self.hex_label = QLabel()
        self.hex_label.setStyleSheet("border-width: 0px;")

        self.custom_layout.addWidget(self.bin_label)
        self.custom_layout.addWidget(self.oct_label)
        self.custom_layout.addWidget(self.dec_label)
        self.custom_layout.addWidget(self.hex_label)

        # self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(self.custom_layout)

    def value_changed(self, notification):
        block = notification.block
        self.bin_label.setText(f"Bin[{len(block.binary()) - 2}]: {block.binary()}")
        self.oct_label.setText(f"Oct[{len(block.octal()) - 2}]: {block.octal()}")
        self.dec_label.setText(f"Dec[{len(block.decimal())}]: {block.decimal()}")
        self.hex_label.setText(f"Hex[{len(block.hexadecimal()) - 2}]: {block.hexadecimal()}")

    def mousePressEvent(self, event):
        # container = container
        notification_provider = notificator.SingletonNotificationProvider()
        notification = notificator.Notification("overview.clicked", self)
        notification_provider.notify(notification)

