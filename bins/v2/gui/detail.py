import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from .. import parser
from .. import model
from .. import dependecy


class DetailWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.block = None
        self.model = None

        self.rows_widgets = []
        self.custom_layout = QVBoxLayout()

        self. init_layout()

    def init_layout(self):
        self.custom_layout.setSpacing(1)
        self.custom_layout.setContentsMargins(0, 1, 0, 1)
        self.setLayout(self.custom_layout)

    def update_data(self, block, data_model):
        self.block = block
        self.model = data_model

        self.update_gui()

    def update_gui(self):
        # TODO: Consider remove
        for w in self.rows_widgets:
            w.deleteLater()

        for row in self.blocks_by_endian():
            r = RowBlocksWidget(self)
            r.set_data(row, self.model)
            self.rows_widgets.append(r)
            self.custom_layout.addWidget(r)

    def blocks_by_endian(self):
        blocks = self.parse_block_for_gui(self.block, int(self.model.get(model.VariableName.alignment)))
        if self.model.get(model.VariableName.endian, "MSB -> LSB") == "MSB -> LSB":
            return blocks[::-1]
        else:
            return blocks

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


class RowBlocksWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.row = []
        self.model = None
        self.block = None
        self.custom_layout = QHBoxLayout()

        self.init_layout()

    def init_layout(self):
        self.custom_layout.setSpacing(10)
        self.custom_layout.setContentsMargins(0, 1, 0, 1)

        self.setLayout(self.custom_layout)

    def set_data(self, row, data_model):
        self.row = row
        self.model = data_model

        for block in self.blocks_by_endian():
            w = LabeledBlockWidget()
            w.set_data(block, self.model)
            self.custom_layout.addWidget(w)

        # self.custom_layout.setSpacing(50)
        # self.custom_layout.setContentsMargins(1, 1, 1, 1)

    def blocks_by_endian(self):
        if self.model.get(model.VariableName.endian, "MSB -> LSB") == "MSB -> LSB":
            return self.row[::-1]
        else:
            return self.row


class LabeledBlockWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block = None
        self.model = None
        self.custom_layout = QVBoxLayout(self)
        self.title = BlockTitleWidget(self)
        self.extended = BlockExtendedDetailWidget()
        self.bits = BlockWidget()

        self.init_layout()
        self.extended.hide()

    def init_layout(self):
        self.custom_layout.setContentsMargins(0, 1, 0, 1)
        self.custom_layout.addWidget(self.title)
        self.custom_layout.addWidget(self.extended)
        self.custom_layout.addWidget(self.bits)

        self.setLayout(self.custom_layout)

    def set_data(self, block, data_model):
        self.block = block
        self.model = data_model

        self.title.set_data(block, data_model)
        self.extended.set_data(block, data_model)
        self.bits.set_data(block, data_model)

        if self.model.get(model.VariableName.view) == "Extended":
            self.extended.show()
        else:
            self.extended.hide()


class BlockTitleWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.block = None
        self.model = None
        self.custom_layout = QVBoxLayout(self)
        self.label = QLabel()

        self.init_layout()
        self.init_styles()

    def init_layout(self):
        self.custom_layout.addWidget(self.label)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)
        self.setLayout(self.custom_layout)


    def set_data(self, block, data_model):
        self.block = block
        self.model = data_model

        self.label.setText(self.block.name)

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        self.setStyleSheet("border: 1px solid gray; background-color: #E5E7E9")
        self.label.setStyleSheet("border-width: 0px; font-weight: bold; color: gray")

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()


class BlockExtendedDetailWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.block = None
        self.model = None
        self.custom_layout = QVBoxLayout(self)
        self.label = QLabel()

        self.init_layout()
        self.init_styles()

    def init_layout(self):
        self.custom_layout.addWidget(self.label)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.custom_layout)


    def set_data(self, block, data_model):
        self.block = block
        self.model = data_model

        self.label.setText(f"""
        {self.block.binary()}
        {self.block.octal()}
        {self.block.decimal()}
        {self.block.hexadecimal()}
        """)

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        self.setStyleSheet("border: 0px solid gray; background-color: white")
        self.label.setStyleSheet("border-width: 0px; font-weight: bold; color: gray")

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()


class BlockWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block = None
        self.model = None

        self.custom_layout = QHBoxLayout(self)
        self.custom_layout.setSpacing(1)
        # self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.custom_layout.setContentsMargins(0, 1, 0, 1)
        # self.setStyleSheet("border: 0px dashed gray; background-color: #E5E7E9")
        self.setLayout(self.custom_layout)

    def set_data(self, block, data_model):
        self.block = block
        self.model = data_model

        for bit in self.bits_by_endian():
            b = BitWidget()
            b.set_data(bit, data_model)
            self.custom_layout.addWidget(b)


    def bits_by_endian(self):
        if self.model.get(model.VariableName.endian, "MSB -> LSB") == "MSB -> LSB":
            return self.block.bits[::-1]
        else:
            return self.block.bits


class BitWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.absolute_position_modifier = 0
        self.block_position_modifier = 0

        # self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.click_style = {
            "white": [
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid white",
                    "value": "border-width: 0px; color: #6495ED",
                    "modifier": "color: gray; border-width: 0px"
                },

                # Gray
                # {
                #     "frame": "background-color: #E5E7E9; color: #6495ED; border: 1px solid gray",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid gray",
                    "value": "border-width: 0px; color: #6495ED",
                    "modifier": "color: gray; border-width: 0px"
                },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid white",
                    "value": "border-width: 0px; color: gray",
                    "modifier": "color: gray; border-width: 0px"
                },

                #  Green
                # {
                #     "frame": "background-color: #A3E4D7; color: #6495ED; border: 1px solid green",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                # {
                #     "frame": "background-color: white; color: #6495ED; border: 3px solid #5EB857",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid white",
                    "value": "border-width: 0px; color: #5EB857",
                    "modifier": "color: #5EB857; border-width: 0px"
                },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid #5EB857",
                    "value": "border-width: 0px; color: #5EB857",
                    "modifier": "color: #5EB857; border-width: 0px"
                },

                # Red
                # {
                #     "frame": "background-color: #F9AAAA; color: #6495ED; border: 1px solid red",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                # {
                #     "frame": "background-color: white; color: #6495ED; border: 3px solid #FF5050",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid white",
                    "value": "border-width: 0px; color: #FF5050",
                    "modifier": "color: #FF5050; border-width: 0px"
                },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid #FF5050",
                    "value": "border-width: 0px; color: #FF5050",
                    "modifier": "color: #FF5050; border-width: 0px"
                },

                # Blue
                # {
                #     "frame": "background-color: #85C1E9; color: #6495ED; border: 1px solid blue",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                # {
                #     "frame": "background-color: white; color: #6495ED; border: 3px solid #6495ED",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid #6495ED",
                    "value": "border-width: 0px; color: #6495ED",
                    "modifier": "color: #6495ED; border-width: 0px"
                },


                # Violet
                # {
                #     "frame": "background-color: #EBDEF0; color: #6495ED; border: 1px solid violet",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                # {
                #     "frame": "background-color: white; color: #6495ED; border: 3px solid #AF7AC5",
                #     "value": "border-width: 0px; color: #6495ED",
                #     "modifier": "color: gray; border-width: 0px"
                # },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid white",
                    "value": "border-width: 0px; color: #AF7AC5 ",
                    "modifier": "color: #AF7AC5; border-width: 0px"
                },
                {
                    "frame": "background-color: white; color: #6495ED; border: 3px solid #AF7AC5",
                    "value": "border-width: 0px; color: #AF7AC5",
                    "modifier": "color: #AF7AC5; border-width: 0px"
                },
            ]
        }

        self.styles_index = 0
        # self.color_index = 0
        # self.colors = ["white", "#E5E7E9", "red", "green", "blue", "violet", "orange"]

        self.block = None
        self.bit = None
        self.model = None
        self.custom_layout = QVBoxLayout(self)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.custom_layout.setContentsMargins(3, 3, 3, 3)

        self.absolute_position = QLabel()
        self.value = QLabel()

        font = QFont("Arial", 17)
        font.setBold(True)
        self.value.setFont(font)

        self.block_position = QLabel()

        self.custom_layout.addWidget(self.absolute_position)
        self.custom_layout.addWidget(self.value)
        self.custom_layout.addWidget(self.block_position)

        # self.absolute_position.setStyleSheet("color: gray")
        # self.value.setStyleSheet("color: violet")
        # self.block_position.setStyleSheet()

        self.setStyleSheet(f"border: 3px solid white")
        self.absolute_position.setStyleSheet("color: gray; border-width: 0px")
        self.value.setStyleSheet("color: #6495ED; border-width: 0px")
        self.block_position.setStyleSheet("color: gray; border-width: 0px")

        self.setLayout(self.custom_layout)

    def set_data(self, bit, data_model):
        self.bit = bit
        self.model = data_model

        absolute_modifier = int(self.model.get(model.VariableName.absolute_position_modifier, 0))
        block_modifier = int(self.model.get(model.VariableName.block_position_modifier, 0))

        self.absolute_position.setText(str(int(bit.absolute_position) + absolute_modifier))
        self.value.setText(str(bit.value))
        self.block_position.setText(str(int(bit.block_position) + int(block_modifier)))

    def mousePressEvent(self, event):
        if event.button() & Qt.MouseButton.LeftButton:
            self.styles_index += 1
        else:
            self.styles_index -= 1
        self.styles_index %= len(self.click_style[self.cfg.theme])
        style = self.click_style[self.cfg.theme][self.styles_index]

        self.absolute_position.setStyleSheet(style["modifier"])
        self.value.setStyleSheet(style["value"])
        self.block_position.setStyleSheet(style["modifier"])

        self.setStyleSheet(style["frame"])

