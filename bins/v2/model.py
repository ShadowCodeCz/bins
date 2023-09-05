from . import notificator


class VariableName:
    alignment = "alignment"
    endian = "endian"
    absolute_position_modifier = "absolute.position.modifier"
    block_position_modifier = "block.position.modifier"
    parser = "parser"
    view = "view"
    file_endian = "file.endian"

    bit_size = "bit.size"
    value = "value"

    start_bit = "start.bit"
    inject = "inject"


class Messages:
    variable_change = "variable.change"
    model_change = "model.change"


class Model:
    def __init__(self):
        self.variables = {}
        self.notificator = notificator.SingletonNotificationProvider()
        self.notificator.subscribe(Messages.variable_change, self.variable_change)

    def variable_change(self, notification):
        # self.update(notification.variable, self.following(notification))
        self.update(notification.variable)

    # def following(self, notification):
    #     try:
    #         return bool(notification.following_notify)
    #     except Exception as e:
    #         return False

    def update(self, variable, notify=False):
        self.variables[variable.name] = variable.value

        # if notify:
        #     notification = notificator.Notification(Messages.model_change)
        #     notification.variable = variable
        #     self.notificator.notify(notification)

    def get(self, variable_name, default=0):
        try:
            return self.variables[variable_name]
        except Exception as e:
            return default


class Variable:
    def __init__(self, name, value):
        self.name = name
        self.value = value


