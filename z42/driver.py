from abc import ABCMeta, abstractmethod


class Driver(metaclass=ABCMeta):

    @abstractmethod
    def get_service_infos(self):
        """
        Yields zeroconf.ServiceInfo
        """
        pass
