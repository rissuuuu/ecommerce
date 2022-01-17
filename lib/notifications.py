import abc


class AbstractNotifications(abc.ABC):
    @abc.abstractmethod
    async def send(self, destination, message):
        raise NotImplementedError
