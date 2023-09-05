import re


class Notification(object):
    def __init__(self, message, publisher=None):
        self.message = message
        self.publisher = publisher


class NotificationProvider(object):
    def __init__(self):
        self.subscription = {}

    def subscribe(self, message, subscriber):
        self.subscription.setdefault(message, []).append(subscriber)

    def unsubscribe(self, message, subscriber):
        self.subscription[message].remove(subscriber)

    def notify(self, notification):
        for subscriber in self.subscription.setdefault(notification.message, []):
            subscriber.new_value_set(notification)

    def notify_by_queue(self, queue):
        for notification in queue:
            self.notify(notification)


class SingletonNotificationProvider:
    subscription = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonNotificationProvider, cls).__new__(cls)
        return cls.instance

    def subscribe(self, message, subscriber):
        self.subscription.setdefault(message, []).append(subscriber)

    def unsubscribe(self, message, subscriber):
        self.subscription[message].remove(subscriber)

    def notify(self, notification):
        for subscriber in self.subscription.setdefault(notification.message, []):
            # subscriber.update(notification)
            subscriber(notification)

    def notify_by_queue(self, queue):
        for notification in queue:
            self.notify(notification)


class ReProvider(NotificationProvider):
    def notify(self, notification):
        for pattern, subscribers in self.subscription:
            if re.match(pattern, notification.message):
                for subscriber in subscribers:
                    subscriber.new_value_set(notification)


class Subscriber(object):
    def update(self, notification):
        raise NotImplemented


class AdvancedSubscriber(Subscriber):
    def __init__(self, provider):
        self.provider = provider

    def update(self, notification):
        raise NotImplemented

    def subscribe(self, message):
        self.provider.subscribe(message, self)

    def unsubscribe(self, message):
        self.provider.unsubscribe(message, self)