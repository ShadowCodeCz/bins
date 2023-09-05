import sys

import PyQt6
from PyQt6 import QtCore
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import notificator


class ValueInput(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.provider = None
        self.edits_visible = True

        self.custom_layout = QHBoxLayout(self)
        self.edits_frame = QFrame()
        self.edits_frame_layout = QHBoxLayout(self)

        self.application_label = QPushButton("Binary Insight")
        self.value_edit = QLineEdit()
        # self.start_edit = QLineEdit()
        # self.end_edit = QLineEdit()
        self.max_size = QLineEdit()
        self.set_button = QPushButton("SET")

        self.custom_layout.addWidget(self.application_label)

        self.edits_frame_layout.addWidget(self.max_size)
        self.edits_frame_layout.addWidget(self.value_edit, 10)
        # self.edits_frame_layout.addWidget(self.start_edit)
        # self.edits_frame_layout.addWidget(self.end_edit)
        self.edits_frame_layout.addWidget(self.set_button)
        self.edits_frame.setLayout(self.edits_frame_layout)

        self.custom_layout.addWidget(self.edits_frame)

        self.setLayout(self.custom_layout)

    def configure_application_label(self):
        font = QFont("Arial", 18)
        font.setBold(True)
        self.application_label.setFont(font)
        self.application_label.clicked.connect(self.hide_and_show)

    def hide_and_show(self):
        if self.edits_visible:
            self.edits_frame.hide()
            self.edits_visible = False
        else:
            self.edits_frame.show()
            self.edits_visible = True

    def configure_value_edit(self):
        self.value_edit.setMinimumWidth(400)

    # def configure_start_edit(self):
    #     self.start_edit.setMaximumWidth(30)
    #     self.start_edit.setToolTip("start bit")
    #
    # def configure_end_edit(self):
    #     self.end_edit.setMaximumWidth(30)

    def configure(self, provider):
        self.provider = provider

        self.configure_application_label()
        self.configure_value_edit()
        # self.configure_set_button()
        # self.configure_start_edit()
        # self.configure_end_edit()

    # def configure_set_button(self):
    #     self.set_button.clicked.connect(self.set)
    #
    # def set(self):
    #     notification = custom_event.Notification("set", self)
    #     notification.value = self.value_edit.text()
    #     notification.max_bits = self.max_size.text()
    #     self.provider.notify(notification)



class Combiner:
    def __init__(self):
        self.value = 0
        self.max_bits = 32

    def set(self, value, max_bits):
        self.value = value
        self.max_bits = max_bits

    def bin(self):
        return format(int(self.save_value()), f'#0{self.save_max_bits()}b')

    def save_max_bits(self):
        try:
            return int(self.max_bits)
        except Exception as e:
            return 32

    def save_value(self):
        try:
            return int(str(self.value), 0)
        except Exception as e:
            return 0


class MainWindowApp(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.provider = None
        self.drag_position = None

        # self.controller = Controller(self.provider)
        # self.provider.subscribe("set", self.controller)

        layout = QVBoxLayout(self)
        self.value_input = ValueInput(self)

        layout.addWidget(self.value_input)
        self.setLayout(layout)

    # def configure(self, provider):
    #     self.provider = provider
    #     self.value_input.configure(self.provider)

    def mousePressEvent(self, event):
        self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
        self.drag_position = event.globalPosition().toPoint()
        event.accept()


# class Controller(custom_event.Subscriber):
#     def __init__(self):
#         self.provider = custom_event.NotificationProvider()
#         self.combiner = Combiner()
#         self.main_window = MainWindowApp()
#         # self.main_window.configure(self.provider)
#
#         self.provider.subscribe("set", self)
#
#
#     def update(self, notification):
#         if notification.message == "set":
#             self.combiner.set(notification.value, notification.max_bits)
#             print(self.combiner.bin())
#             notification = custom_event.Notification("new value", self)
#             notification.value = self.combiner.bin()
#             notification.max_bits = self.combiner.save_max_bits()
#             self.provider.notify(notification)
#
#     def run(self):
#         app = QApplication(sys.argv)
#         self.main_window.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
#         self.main_window.show()
#         app.exec()
#
#
# controller = Controller()
# controller.run()