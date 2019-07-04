from .base import (SymbolStandard, Symbol, SymbolPair, SymbolPairConverter,
    SymbolPairConverterError)

class KrakenSymbolPairConverter(SymbolPairConverter[str]):
    from_pair_map = {
        SymbolPair(Symbol.USD, Symbol.BITCOIN): 'XXBTZUSD',
    }

    to_pair_map = {
        'XXBTZUSD': SymbolPair(Symbol.USD, Symbol.BITCOIN),
    }

    @classmethod
    def get_standard(cls) -> SymbolStandard:
        return SymbolStandard.Kraken

    @classmethod
    def from_pair(cls, pair: SymbolPair) -> str:
        try:
            result = cls.from_pair_map[pair]
        except:
            raise SymbolPairConverterError(pair, cls.get_standard())
        return result

    @classmethod
    def to_pair(cls, converted: str) -> SymbolPair:
        try:
            result = cls.to_pair_map[converted]
        except:
            raise SymbolPairConverterError(converted, cls.get_standard())
        return result
