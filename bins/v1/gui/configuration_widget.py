from PyQt6.QtWidgets import *

from . import labeled_combo_box
from . import labeled_spin_box

from bins.v1 import notificator


class ConfigurationWidget(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.notification_provider = notificator.SingletonNotificationProvider()
        self.custom_layout = QHBoxLayout(self)

        self.alignment = labeled_spin_box.LabeledSpinBox(self)
        self.alignment.label.setText("Alignment")
        self.alignment.box.setMinimum(0)
        self.alignment.box.setMaximum(1000)
        self.alignment.box.setValue(32)
        self.alignment.box.valueChanged.connect(self.alignment_change)

        self.direction = labeled_combo_box.LabeledComboBox(self)
        self.direction.label.setText("Direction")
        self.direction.box.addItems(["LSB -> MSB", "MSB -> LSB"])

        self.absolute_position_modifier = labeled_spin_box.LabeledSpinBox(self)
        self.absolute_position_modifier.label.setText("Absolute position modifier")
        self.absolute_position_modifier.box.setMinimum(-1000)
        self.absolute_position_modifier.box.setMaximum(1000)
        self.absolute_position_modifier.box.valueChanged.connect(self.absolute_position_modifier_change)

        self.block_position_modifier = labeled_spin_box.LabeledSpinBox(self)
        self.block_position_modifier.label.setText("Block position modifier")
        self.block_position_modifier.box.setMinimum(-1000)
        self.block_position_modifier.box.setMaximum(1000)
        self.block_position_modifier.box.valueChanged.connect(self.block_position_modifier_change)

        self.custom_layout.addWidget(self.alignment)
        self.custom_layout.addWidget(self.direction)
        self.custom_layout.addWidget(self.absolute_position_modifier)
        self.custom_layout.addWidget(self.block_position_modifier)

        self.setLayout(self.custom_layout)

    def absolute_position_modifier_change(self, event):
        notification = notificator.Notification("absolute.position.modifier.change", self)
        notification.value = self.absolute_position_modifier.box.value()
        self.notification_provider.notify(notification)

    def block_position_modifier_change(self, event):
        notification = notificator.Notification("block.position.modifier.change", self)
        notification.value = self.block_position_modifier.box.value()
        self.notification_provider.notify(notification)

    def alignment_change(self, event):
        notification = notificator.Notification("alignment.change", self)
        notification.value = self.alignment.box.value()
        self.notification_provider.notify(notification)