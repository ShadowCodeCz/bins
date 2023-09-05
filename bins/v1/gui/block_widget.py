from PyQt6.QtWidgets import *

from . import bit_widget

class BlockWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block = None

        self.custom_layout = QHBoxLayout(self)
        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.custom_layout)
        # self.setStyleSheet("border: 1px dotted black")

    def set_block(self, block):
        self.block = block

        # pure_bits = block.binary().replace("0b", "")
        for bit in block.bits[::-1]:
            b = bit_widget.BitWidget()
            b.set_bit(bit)
            self.custom_layout.addWidget(b)
