from dependency_injector import containers, providers


class Configuration:
    theme = "white"


class Container(containers.DeclarativeContainer):
    configuration_provider = providers.Singleton(Configuration)