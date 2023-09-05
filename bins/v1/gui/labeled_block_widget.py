from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

from . import block_widget


class LabeledBlockWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block = None
        self.custom_layout = QVBoxLayout(self)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.custom_layout.setContentsMargins(10, 1, 10, 1)

        # self.label = QLabel()
        # self.label.setStyleSheet("""
        #     font-size: 9px;
        #     font-family: Arial;
        # """)

        # self.labels_frame = QFrame(self)
        # self.labels_layout = QVBoxLayout()

        self.title_frame = QFrame()
        self.title_layout = QVBoxLayout()

        self.name_label = QLabel()
        self.name_label.setStyleSheet("""
                    font-weight: bold;
                    font-size: 15px;
                    font-family: Arial;
                """)
        self.bin_label = QLabel()
        self.bin_label.setStyleSheet("font-size: 9px; font-family: Arial;")
        self.oct_label = QLabel()
        self.oct_label.setStyleSheet("font-size: 9px; font-family: Arial;")
        self.dec_label = QLabel()
        self.dec_label.setStyleSheet("font-size: 9px; font-family: Arial;")
        self.hex_label = QLabel()
        self.hex_label.setStyleSheet("font-size: 9px; font-family: Arial;")

        self.bits = block_widget.BlockWidget()

        self.title_layout.addWidget(self.name_label)
        self.name_label.setStyleSheet("border-width: 0px")
        self.title_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title_frame.setStyleSheet("border: 2px solid black; background-color: #606060")
        self.title_frame.setLayout(self.title_layout)

        self.labels_layout = QVBoxLayout()
        self.labels_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # self.labels_layout.addWidget(self.name_label)

        self.labels_layout.addWidget(self.bin_label)
        self.labels_layout.addWidget(self.oct_label)
        self.labels_layout.addWidget(self.dec_label)
        self.labels_layout.addWidget(self.hex_label)

        self.custom_layout.addWidget(self.title_frame)
        self.custom_layout.addLayout(self.labels_layout)
        self.custom_layout.addWidget(self.bits)

        self.setLayout(self.custom_layout)

    def set_block(self, block):
        self.block = block
        # self.label.setText(f"{self.block.name}\n"
        #                    f"Bin: {self.block.binary()}\n"
        #                    f"Oct: {self.block.octal()}\n"
        #                    f"Dec: {self.block.decimal()}\n"
        #                    f"Hex: {self.block.hexadecimal()}")

        self.name_label.setText(self.block.name)
        self.bin_label.setText(f"Bin: {self.block.binary()}")
        self.oct_label.setText(f"Oct: {self.block.octal()}")
        self.dec_label.setText(f"Dec: {self.block.decimal()}")
        self.hex_label.setText(f"Hex: {self.block.hexadecimal()}")
        self.bits.set_block(block)