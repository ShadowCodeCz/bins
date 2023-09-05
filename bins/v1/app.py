from PyQt6.QtWidgets import *

from bins.v1 import combiner, notificator, parser, container

from .gui import main_window

class Application:
    def __init__(self):
        self.combiner = combiner.Combiner()
        self.app_data_updater = AppDataUpdater()
        # templates = [
        #     parser.BlockTemplate(range(0, 4), "Part 0 - 4", ""),
        #     parser.BlockTemplate(range(7, 9), "Part 7 - 9", ""),
        #     parser.BlockTemplate(range(10, 32), "Part 10 - 32", ""),
        # ]

        templates = [
            parser.BlockTemplate(range(0, 8), "Label", ""),
            parser.BlockTemplate(range(8, 10), "SDI", ""),
            parser.BlockTemplate(range(10, 29), "Data", ""),
            parser.BlockTemplate(range(29, 31), "SSM", ""),
            parser.BlockTemplate(range(31, 32), "P", ""),
        ]

        self.parser = parser.Parser(templates)
        self.container = container.Container()

        self.notification_provider = notificator.SingletonNotificationProvider()
        self.app_core = self.container.app_core()
        self.app_core.set_standard_logger()
        self.logger = self.app_core.logger()

        self.notification_provider.subscribe("new.value.set", self.new_value_set)

    def run(self):
        app = QApplication([])

        window = main_window.MainWindow()
        self.notification_provider.subscribe("value.changed", window.overview.value_changed)
        self.notification_provider.subscribe("value.changed", window.detail.value_changed)
        self.notification_provider.subscribe("overview.clicked", window.title.hide_and_show)
        self.notification_provider.subscribe("absolute.position.modifier.change", self.app_data_updater.absolute_position_modifier_change)
        self.notification_provider.subscribe("block.position.modifier.change", self.app_data_updater.block_position_modifier_change)
        self.notification_provider.subscribe("alignment.change", self.app_data_updater.alignment_change)
        # self.notification_provider.subscribe("alignment.change", window.detail.app_data_change)
        # window.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        window.show()

        app.exec()

    def new_value_set(self, notification):
        self.combiner.set(notification.value, notification.bits_size)
        block = self.parser.parse(self.combiner.bin())

        notification = notificator.Notification("value.changed")
        notification.block = block
        notification.app_data = self.app_data_updater.data
        self.notification_provider.notify(notification)


class AppData:
    def __init__(self):
        self.absolute_position_modifier = 0
        self.block_position_modifier = 0
        self.alignment = 32


class AppDataUpdater:
    def __init__(self):
        self.data = AppData()

    def absolute_position_modifier_change(self, notification):
        try:
            self.data.absolute_position_modifier = int(notification.value)
        except Exception as e:
            self.data.absolute_position_modifier = 0

    def block_position_modifier_change(self, notification):
        try:
            self.data.block_position_modifier = int(notification.value)
        except Exception as e:
            self.data.block_position_modifier = 0

    def alignment_change(self, notification):
        try:
            self.data.alignment = int(notification.value)
        except Exception as e:
            self.data.alignment = 32

def run():
    app = Application()
    app.run()
