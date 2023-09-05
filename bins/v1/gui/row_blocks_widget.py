from PyQt6.QtWidgets import *

from . import labeled_block_widget


class RowBlocksWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.blocks_widgets = []
        self.custom_layout = QHBoxLayout()
        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.custom_layout)

    def set_new_row(self, row):
        # block = notification.block

        # for w in self.blocks_widgets:
        #     w.deleteLater()

        # self.blocks_widgets = []

        for block in row[::-1]:
            w = labeled_block_widget.LabeledBlockWidget()
            w.set_block(block)
            # self.blocks_widgets.append(w)
            self.custom_layout.addWidget(w)

        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)
