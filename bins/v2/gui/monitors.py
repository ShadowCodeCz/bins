from .. import notificator
from .. import model


class Monitor:
    def __init__(self, variable_name, gui_item):
        self.variable_name = variable_name
        self.gui_item = gui_item
        # self.following = following
        self.notificator = notificator.SingletonNotificationProvider()

        self.bind()

    def bind(self):
        pass

    def monitor(self, event):
        self.notify()

    def notify(self):
        notification = notificator.Notification(model.Messages.variable_change)
        notification.variable = model.Variable(self.variable_name, self.read_value())
        # notification.following_notify = self.following
        self.notificator.notify(notification)

    def read_value(self):
        pass


class LineEditMonitor(Monitor):

    def bind(self):
        self.gui_item.textChanged.connect(self.monitor)

    def read_value(self):
        return self.gui_item.text()


class ComboBoxMonitor(Monitor):
    def bind(self):
        self.gui_item.currentTextChanged.connect(self.monitor)

    def read_value(self):
        return self.gui_item.currentText()


class SpinBoxMonitor(Monitor):
    def bind(self):
        self.gui_item.valueChanged.connect(self.monitor)

    def read_value(self):
        return self.gui_item.value()
