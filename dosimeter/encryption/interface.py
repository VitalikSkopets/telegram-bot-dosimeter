import abc

__all__ = ("BaseCryptographer",)


class BaseCryptographer(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, message: str | None = None) -> str | None:
        """Method for encrypting string objects."""
        pass

    @abc.abstractmethod
    def decrypt(self, token: str) -> str | None:
        """Method for decrypting string objects."""
        pass
