from abc import abstractmethod

import ujson

from dataclasses import dataclass


@dataclass
class BaseEntityClass:

    @property
    @abstractmethod
    def key(self) -> str:
        ...

    @property
    @abstractmethod
    def value(self) -> str:
        ...
