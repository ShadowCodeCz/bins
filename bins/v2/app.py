import os
import ctypes

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import *
# from PyQt6.QtGui import QFont, QFontDatabase

from . import gui
from . import model
from . import notificator

from . import parser
from . import combiner


class Application:
    def __init__(self):
        self.model = model.Model()
        self.notificator = notificator.SingletonNotificationProvider()
        # self.notificator.subscribe(model.Messages.model_change, self.set_new_value)
        self.notificator.subscribe(notificator.Messages.set_value, self.set_new_value)
        self.notificator.subscribe(notificator.Messages.inject_value, self.inject_new_value)

        self.combiner = combiner.Combiner()
        self.parser = parser.Parser()

        self.app = None
        self.window = None

    def run(self):

        self.app = QApplication([])

        # Taskbar icon fix
        my_app_id = 'mycompany.myproduct.subproduct.version'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

        self.window = gui.AppWidget()

        notification = notificator.Notification(notificator.Messages.parsers_update)
        notification.parsers = self.parser.parsers.keys()
        self.notificator.notify(notification)

        self.window.setStyleSheet("color: white; background-color: black")
        self.window.setWindowTitle("Binary Insight")
        # window.setWindowIcon(QIcon(QPixmap('./resource/logo.png')))
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "resource", 'logo.png')

        self.window.setWindowIcon(QIcon(path))
        self.app.setWindowIcon(QIcon(path))
        self.window.show()

        self.app.exec()

    def set_new_value(self, notification):
        self.combiner.set(self.model.get(model.VariableName.value, 0), self.model.get(model.VariableName.bit_size, 8))
        block = self.parser.parse(self.model.get(model.VariableName.parser), self.combiner.bin())

        notification = notificator.Notification(notificator.Messages.new_block)
        notification.block = block
        notification.model = self.model
        self.notificator.notify(notification)
        self.window.resize(self.window.minimumSizeHint())

    def inject_new_value(self, notification):
        pass



def run():
    app = Application()
    app.run()