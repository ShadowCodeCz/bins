import os

from PyQt6.QtGui import QDoubleValidator, QFont
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from . import basic
from . import monitors
from .. import model
from .. import notificator
from .. import dependecy

from . import detail


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setCentralWidget(AppWidget())


class AppWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(AppWidget, self).__init__(*args, **kwargs)
        # self.drag_position = None

        self.themes_map = {"white": self.white_styles}

        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.custom_layout = QVBoxLayout(self)
        self.custom_layout.setSpacing(2)

        self.overview = OverviewWidget()
        self.control_panel = ControlPanelWidget()
        self.display = DisplayWidget()

        self.custom_layout.addWidget(self.overview)
        self.custom_layout.addWidget(self.control_panel)
        self.custom_layout.addWidget(self.display)

        self.setLayout(self.custom_layout)

        self.setAutoFillBackground(True)
        self.init_styles()

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        self.setStyleSheet('background-color: white; color: black')

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()


class OverviewWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = None
        self.block = None
        self.themes_map = {"white": self.white_styles}
        self.dependency = dependecy.Container()
        self.cfg = self.dependency.configuration_provider()

        self.notificator = notificator.SingletonNotificationProvider()
        self.notificator.subscribe(notificator.Messages.new_block, self.new_data)
        self.custom_layout = QHBoxLayout(self)

        # self.app_label = AppTitleWidget()
        self.bin_label = basic.ValueWidget()
        self.oct_label = basic.ValueWidget()
        self.dec_label = basic.ValueWidget()
        self.hex_label = basic.ValueWidget()

        self.bin_label.value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.oct_label.value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.dec_label.value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.hex_label.value.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

        self.counter = 0
        self.actions = [
            self.show_all,
            self.bin_label.show,
            self.oct_label.show,
            self.dec_label.show,
            self.hex_label.show,
        ]

        self.init_layout()
        self.init_values()
        self.init_styles()

    def init_layout(self):
        # self.custom_layout.addWidget(self.app_label)
        self.custom_layout.setContentsMargins(1, 1, 1, 1)
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.custom_layout.addWidget(self.bin_label)
        self.custom_layout.addWidget(self.oct_label)
        self.custom_layout.addWidget(self.dec_label)
        self.custom_layout.addWidget(self.hex_label)

        self.setLayout(self.custom_layout)

    def init_values(self):
        self.bin_label.label.setText("Binary")
        self.oct_label.label.setText("Octal")
        self.dec_label.label.setText("Decimal")
        self.hex_label.label.setText("Hexadecimal")

    def mousePressEvent(self, event):
        if event.button() & Qt.MouseButton.LeftButton:
            notification_provider = notificator.SingletonNotificationProvider()
            notification = notificator.Notification(notificator.Messages.overview_clicked, self)
            notification_provider.notify(notification)
        if event.button() & Qt.MouseButton.RightButton:
            self.counter += 1
            self.counter %= len(self.actions)
            self.hide_all()
            self.actions[self.counter]()

    def new_data(self, notification):
        self.block = notification.block
        self.model = model
        self.update_values()

    def update_values(self):
        self.bin_label.value.setText(self.block.binary())
        self.oct_label.value.setText(self.block.octal())
        self.dec_label.value.setText(self.block.decimal())
        self.hex_label.value.setText(self.block.hexadecimal())

    def init_styles(self):
        self.set_styles()

    def white_styles(self):
        self.setStyleSheet("border: 1px solid gray; background-color: #E5E7E9")

    def set_styles(self):
        return self.themes_map[self.cfg.theme]()

    def show_all(self):
        self.bin_label.show()
        self.oct_label.show()
        self.dec_label.show()
        self.hex_label.show()

    def hide_all(self):
        self.bin_label.hide()
        self.oct_label.hide()
        self.dec_label.hide()
        self.hex_label.hide()


class AppTitleWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.custom_layout = QVBoxLayout(self)
        self.title = QLabel()

        self.init_layout()
        self.init_values()
        self.init_styles()

    def init_layout(self):
        self.custom_layout.addWidget(self.title)
        self.setLayout(self.custom_layout)

    def init_values(self):
        self.title.setText("Binary Insight")

    def init_styles(self):
        font = QFont("Verdana", 20)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setStyleSheet("color: red")


class ControlPanelWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.visible = True
        self.notificator = notificator.SingletonNotificationProvider()
        self.notificator.subscribe(notificator.Messages.overview_clicked, self.hide_and_show)
        self.custom_layout = QVBoxLayout(self)

        self.configuration = ConfigurationWidget()
        self.set_value = SetValueWidget()
        # self.inject_value = InjectValueWidget()

        self.init_layout()

    def init_layout(self):
        self.custom_layout.addWidget(self.configuration)
        self.custom_layout.addWidget(self.set_value)
        # self.custom_layout.addWidget(self.inject_value)

        self.setLayout(self.custom_layout)

    def hide_and_show(self, notification):
        if self.visible:
            self.hide()
            self.visible = False
        else:
            self.show()
            self.visible = True


class ConfigurationWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notificator = notificator.SingletonNotificationProvider()
        self.notificator.subscribe(notificator.Messages.parsers_update, self.update_parsers)

        self.custom_layout = QHBoxLayout(self)
        self.alignment = basic.SpinBox()
        self.endian = basic.ComboBox()
        self.absolute_position_modifier = basic.SpinBox()
        self.block_position_modifier = basic.SpinBox()
        self.parser = basic.ComboBox()
        self.view = basic.ComboBox()
        self.file_endian = basic.ComboBox()
        # self.fonts = QFontComboBox()

        # TODO: Font
        # TODO: Color Schema
        # TODO: Display
        # TODO: Text size


        self.init_layout()
        self.init_monitors()
        self.init_values()
        self.init_setting()

    def init_layout(self):
        self.custom_layout.addWidget(self.alignment)
        self.custom_layout.addWidget(self.endian)
        self.custom_layout.addWidget(self.absolute_position_modifier)
        self.custom_layout.addWidget(self.block_position_modifier)
        self.custom_layout.addWidget(self.parser)
        self.custom_layout.addWidget(self.view)
        self.custom_layout.addWidget(self.file_endian)
        # self.custom_layout.addWidget(self.fonts)

        self.setLayout(self.custom_layout)

    def init_values(self):
        self.alignment.label.setText("Alignment")
        self.alignment.box.setValue(0)

        self.endian.label.setText("Display direction")
        self.endian.box.addItems(["MSB -> LSB", "LSB -> MSB"])

        self.absolute_position_modifier.label.setText("Absolute position modifier")
        self.absolute_position_modifier.box.setValue(0)

        self.block_position_modifier.label.setText("Block position modifier")
        self.block_position_modifier.box.setValue(0)

        self.parser.label.setText("Parser")
        self.parser.box.addItems([])

        self.view.label.setText("View")
        self.view.box.addItems(["Basic", "Extended"])

        self.file_endian.label.setText("File Endian")
        self.file_endian.box.addItems(["little", "big"])

    def init_monitors(self):
        self.alignment.set_monitor(model.VariableName.alignment)
        self.endian.set_monitor(model.VariableName.endian)
        self.absolute_position_modifier.set_monitor(model.VariableName.absolute_position_modifier)
        self.block_position_modifier.set_monitor(model.VariableName.block_position_modifier)
        self.block_position_modifier.set_monitor(model.VariableName.block_position_modifier)
        self.parser.set_monitor(model.VariableName.parser)
        self.view.set_monitor(model.VariableName.view)
        self.file_endian.set_monitor(model.VariableName.file_endian)

    def init_setting(self):
        self.alignment.box.setValue(32)

    def update_parsers(self, notification):
        self.parser.box.addItems(notification.parsers)


class SetValueWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notificator = notificator.SingletonNotificationProvider()
        self.notificator.subscribe(model.Messages.variable_change, self.update_endian)
        self.custom_layout = QHBoxLayout(self)

        self.endian_value = "little"
        self.bit_size = basic.SpinBox()
        self.value = basic.LineEdit()
        self.string_revert = basic.PushButton("revert string")
        self.value_revert = basic.PushButton("revert value")
        self.read_file = basic.PushButton("read file")
        self.set = basic.PushButton("set")

        self.init_layout()
        self.init_values()
        self.init_monitors()
        self.init_connections()
        self.init_setting()

    def init_layout(self):
        self.custom_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.custom_layout.addWidget(self.bit_size)
        self.custom_layout.addWidget(self.value)
        self.custom_layout.addWidget(self.string_revert)
        self.custom_layout.addWidget(self.value_revert)
        self.custom_layout.addWidget(self.read_file)
        self.custom_layout.addWidget(self.set)

        self.setLayout(self.custom_layout)

    def init_values(self):
        self.bit_size.label.setText("Min Bit size")
        self.value.label.setText("Value")

    def init_monitors(self):
        self.bit_size.set_monitor(model.VariableName.bit_size)
        self.value.set_monitor(model.VariableName.value)

    def init_connections(self):
        self.string_revert.clicked.connect(self.revert_string)
        self.value_revert.clicked.connect(self.revert_value)
        self.read_file.clicked.connect(self.read_bin_file)
        self.set.clicked.connect(self.set_new_value)

    def read_bin_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), "")
        with open(file_path[0], "rb") as f:
            if self.endian_value == "little":
                v = bin(int.from_bytes(f.read(), byteorder="little"))
            else:
                v = bin(int.from_bytes(f.read(), byteorder="big"))
            self.value.box.setText(f"{v}")

    def init_setting(self):
        self.bit_size.box.setValue(32)

    def revert_string(self, event):
        self.value.box.setText(self.value.box.text()[::-1])

    def revert_value(self, event):
        try:
            original_value = self.value.box.text()
            binary_value = bin(int(original_value, 0))
            reverted_bin_value = binary_value.replace("0b", "")[::-1]
            reverted_bin_value = int(reverted_bin_value, 2)
            reverted_value = 0
            if "0b" in original_value:
                reverted_value = f"0b{reverted_bin_value:b}"
            elif "0o" in original_value:
                reverted_value = f"0o{reverted_bin_value:o}"
            elif "0d" in original_value:
                reverted_value = f"{reverted_bin_value:d}"
            elif "0x" in original_value:
                reverted_value = f"0x{reverted_bin_value:x}"
            else:
                reverted_value = f"{reverted_bin_value:d}"

            self.value.box.setText(reverted_value)
        except Exception as e:
            print(e)

    def set_new_value(self, event):
        notification = notificator.Notification(notificator.Messages.set_value)
        self.notificator.notify(notification)

    def update_endian(self, notification):
        if notification.variable.name == model.VariableName.file_endian:
            self.endian_value = notification.variable.value


class InjectValueWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notificator = notificator.SingletonNotificationProvider()
        self.custom_layout = QHBoxLayout(self)

        self.start_bit = basic.SpinBox()
        self.value = basic.LineEdit()
        self.revert = QPushButton("revert")
        self.inject = QPushButton("inject")

        self.init_layout()
        self.init_values()
        self.init_monitors()
        self.init_connections()

    def init_layout(self):
        self.custom_layout.addWidget(self.start_bit)
        self.custom_layout.addWidget(self.value)
        self.custom_layout.addWidget(self.revert)
        self.custom_layout.addWidget(self.inject)

        self.setLayout(self.custom_layout)

    def init_values(self):
        self.start_bit.label.setText("Start bit")
        self.value.label.setText("Value")

    def init_monitors(self):
        self.start_bit.set_monitor(model.VariableName.start_bit)
        self.value.set_monitor(model.VariableName.inject)

    def init_connections(self):
        self.revert.clicked.connect(self.revert_value)
        self.inject.clicked.connect(self.inject_new_value)

    def revert_value(self, event):
        self.value.box.setText(self.value.box.text()[::-1])

    def inject_new_value(self, event):
        notification = notificator.Notification(notificator.Messages.set_value)
        self.notificator.notify(notification)


class DisplayWidget(QFrame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notificator = notificator.SingletonNotificationProvider()
        self.notificator.subscribe(notificator.Messages.new_block, self.new_data)
        self.custom_layout = QHBoxLayout(self)

        self.detail = detail.DetailWidget()

        # self.start_bit = basic.SpinBox()
        # self.value = basic.LineEdit()
        # self.revert = QPushButton("revert")
        # self.inject = QPushButton("inject")

        self.init_layout()
        # self.init_monitors()
        # self.init_connections()

    def init_layout(self):
        # self.custom_layout.addWidget(self.start_bit)
        # self.custom_layout.addWidget(self.value)
        # self.custom_layout.addWidget(self.revert)
        # self.custom_layout.addWidget(self.inject)

        self.custom_layout.setContentsMargins(0, 0, 0, 0)
        self.custom_layout.addWidget(self.detail)
        self.setLayout(self.custom_layout)

    def new_data(self, notification):
        self.detail.deleteLater()
        self.detail = detail.DetailWidget()
        self.custom_layout.addWidget(self.detail)

        self.detail.update_data(notification.block, notification.model)
