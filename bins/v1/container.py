from dependency_injector import containers, providers
from bins.v1 import notificator, core


class Container(containers.DeclarativeContainer):
    event_provider = providers.Singleton(notificator.SingletonNotificationProvider)
    app_core = providers.Singleton(core.AppCore)

