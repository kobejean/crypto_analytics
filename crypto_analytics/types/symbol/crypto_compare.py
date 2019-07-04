from typing import NamedTuple, Any, TypeVar, Generic

from .base import (SymbolStandard, Symbol, SymbolPair, SymbolPairConverter,
    SymbolPairConverterError)

CryptoCompareSymbolPair = NamedTuple('CryptoCompareSymbolPair', [('tsym', str), ('fsym', str)])

class CryptoCompareSymbolPairConverter(SymbolPairConverter[CryptoCompareSymbolPair]):
    from_symbol_map = {
        Symbol.USD: 'USD',
        Symbol.BITCOIN: 'BTC',
    }

    to_symbol_map = {
        'USD': Symbol.USD,
        'BTC': Symbol.BITCOIN,
    }

    @classmethod
    def get_standard(cls) -> SymbolStandard:
        return SymbolStandard.CryptoCompare

    @classmethod
    def from_pair(cls, pair: SymbolPair) -> CryptoCompareSymbolPair:
        try:
            fsym = cls.from_symbol_map[pair.fsym]
            tsym = cls.from_symbol_map[pair.tsym]
        except:
            raise SymbolPairConverterError(pair, cls.get_standard())
        return CryptoCompareSymbolPair(fsym, tsym)

    @classmethod
    def to_pair(cls, converted: CryptoCompareSymbolPair) -> SymbolPair:
        try:
            fsym = cls.to_symbol_map[converted.fsym]
            tsym = cls.to_symbol_map[converted.tsym]
        except:
            raise SymbolPairConverterError(converted, cls.get_standard())
        return SymbolPair(fsym, tsym)
