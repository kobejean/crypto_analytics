"""
Contains symbol, symbol standard, and symbol pair definitions as well as
an abstract base class for symbol pair converters.
"""
from abc import ABCMeta, abstractmethod
from typing import NamedTuple, Any, TypeVar, Generic
from enum import Enum

class Symbol(Enum):
    # Fiat (ISO 4217)
    USD = 'USD'
    # Crypto (full name in UPPER_CASE, until we have an official standard)
    BITCOIN = 'BITCOIN'
    LITECOIN = 'LITECOIN'
    ETHERIUM = 'ETHERIUM'


class SymbolStandard(Enum):
    CryptoCompare = 'CryptoCompare'
    Kraken = 'Kraken'


SymbolPair = NamedTuple('SymbolPair', [('tsym', Symbol), ('fsym', Symbol)])


# used for generic in SymbolPairConverter
ConvertedType = TypeVar('ConvertedType')
class SymbolPairConverter(Generic[ConvertedType], metaclass=ABCMeta):

    @classmethod
    @abstractmethod
    def get_standard(cls) -> SymbolStandard:
        pass

    @classmethod
    @abstractmethod
    def from_pair(cls, pair: SymbolPair) -> ConvertedType:
        pass

    @classmethod
    @abstractmethod
    def to_pair(cls, converted: ConvertedType) -> SymbolPair:
        pass


class SymbolPairConverterError(Exception):
    def __init__(self, obj: Any, standard: SymbolStandard):
        self.obj = obj
        self.standard = standard
        message = 'Conversion from: {0} failed with standard {1}'.format(obj, standard)
        super().__init__(message)
