import abc

__all__ = ("BaseCryptographer",)


class BaseCryptographer(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, message: str) -> str | None:
        pass

    @abc.abstractmethod
    def decrypt(self, token: str) -> str | None:
        pass
