from PyQt6.QtWidgets import *

from . import row_blocks_widget
from bins.v1 import parser


class DetailWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block = None
        self.app_data = None

        self.rows_widgets = []
        self.custom_layout = QVBoxLayout()
        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(1,1,1,1)
        self.setLayout(self.custom_layout)

    def value_changed(self, notification):
        self.block = notification.block
        self.app_data = notification.app_data

        self.update_detail()

    def app_data_change(self, notification):
        self.app_data = notification.app_data
        self.update_detail()

    def update_detail(self):
        for w in self.rows_widgets:
            w.deleteLater()

        for row in self.parse_block_for_gui(self.block, self.app_data.alignment)[::-1]:
            r = row_blocks_widget.RowBlocksWidget(self)
            r.set_new_row(row)
            self.rows_widgets.append(r)
            self.custom_layout.addWidget(r)

    def parse_block_for_gui(self, full_block, alignment=32):
        rows = []
        row = []
        block = parser.Block()

        r = 1
        for position, bit in enumerate(full_block.bits):
            if position >= alignment * r:
                r += 1

                rows.append(row)
                row = []

                block = parser.Block()
                block.full_bin_value = bit.block.full_bin_value
                block.name = bit.block.name
                block.blocks = bit.block.blocks
                block.bits.append(bit)
                block.range = range(block.bits[0].absolute_position, block.bits[-1].absolute_position + 1)

                row.append(block)

            if bit.block.name != block.name:
                block = parser.Block()
                block.full_bin_value = bit.block.full_bin_value
                block.name = bit.block.name
                block.blocks = bit.block.blocks
                block.bits.append(bit)
                block.range = range(block.bits[0].absolute_position, block.bits[-1].absolute_position + 1)

                row.append(block)

            else:
                block.bits.append(bit)
                block.range = range(block.bits[0].absolute_position, block.bits[-1].absolute_position + 1)

        rows.append(row)
        return rows


    # def parse_block_for_gui(self, blocks, alignment=15):
    #     counter = 0
    #     rows = []
    #     r = 1
    #     row = []
    #     for block in blocks:
    #         counter += len(block.range)
    #
    #         threshold = r * alignment
    #         if threshold > counter:
    #             row.append(block)
    #             print(f"Block: {block.range} [{len(block.range)}]")
    #         else:
    #             b1 = copy.deepcopy(block)
    #             b1.range = range(b1.range.start, b1.range.start + (threshold - b1.range.start))
    #             b1.bits = [bit for bit in b1.bits if bit.absolute_position in b1.range]
    #
    #             b2 = copy.deepcopy(block)
    #             b2.range = range(threshold, threshold + (counter - threshold))
    #             b2.bits = [bit for bit in b2.bits if bit.absolute_position in b2.range]
    #
    #             print(f"Block: {block.range}[{len(block.range)}] -> split B1.range:{b1.range}, B1.bits.length: {len(b1.bits)},   B2.range: {b2.range}, B2.bits.length: {len(b2.bits)}")
    #
    #             row.append(b1)
    #             rows.append([block for block in row if len(block.range) > 0])
    #
    #             row = [b2]
    #             r += 1
    #
    #     rows.append([block for block in row if len(block.range) > 0])
    #     return rows