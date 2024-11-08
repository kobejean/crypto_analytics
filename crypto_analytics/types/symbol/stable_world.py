from .base import (SymbolStandard, Symbol, SymbolPair, SymbolPairConverter,
    SymbolPairConverterError)

class StableWorldSymbolPairConverter(SymbolPairConverter[str]):
    standard = SymbolStandard.STABLE_WORLD
    
    from_pair_map = {
        # to BITCOIN
        SymbolPair(Symbol.JPY, Symbol.BITCOIN): 'JPYBTC',
        SymbolPair(Symbol.USD, Symbol.BITCOIN): 'USDBTC',
        SymbolPair(Symbol.VND, Symbol.BITCOIN): 'VNDBTC',
        # to JPY
        SymbolPair(Symbol.BITCOIN, Symbol.JPY): 'BTCJPY',
        SymbolPair(Symbol.USD, Symbol.JPY): 'USDJPY',
        SymbolPair(Symbol.VND, Symbol.JPY): 'VNDJPY',
        # to USD
        SymbolPair(Symbol.BITCOIN, Symbol.USD): 'BTCUSD',
        SymbolPair(Symbol.JPY, Symbol.USD): 'JPYUSD',
        SymbolPair(Symbol.VND, Symbol.USD): 'VNDUSD',
        # to VND
        SymbolPair(Symbol.BITCOIN, Symbol.VND): 'BTCVND',
        SymbolPair(Symbol.JPY, Symbol.VND): 'JPYVND',
        SymbolPair(Symbol.USD, Symbol.VND): 'USDVND',
    }

    to_pair_map = {
        # to BITCOIN
        'JPYBTC': SymbolPair(Symbol.JPY, Symbol.BITCOIN),
        'USDBTC': SymbolPair(Symbol.USD, Symbol.BITCOIN),
        'VNDBTC': SymbolPair(Symbol.VND, Symbol.BITCOIN),
        # to JPY
        'BTCJPY': SymbolPair(Symbol.BITCOIN, Symbol.JPY),
        'USDJPY': SymbolPair(Symbol.USD, Symbol.JPY),
        'VNDJPY': SymbolPair(Symbol.VND, Symbol.JPY),
        # to USD
        'BTCUSD': SymbolPair(Symbol.BITCOIN, Symbol.USD),
        'JPYUSD': SymbolPair(Symbol.JPY, Symbol.USD),
        'VNDUSD': SymbolPair(Symbol.VND, Symbol.USD),
        # to VND
        'BTCVND': SymbolPair(Symbol.BITCOIN, Symbol.VND),
        'JPYVND': SymbolPair(Symbol.JPY, Symbol.VND),
        'USDVND': SymbolPair(Symbol.USD, Symbol.VND),
    }

    @classmethod
    def from_pair(cls, pair: SymbolPair) -> str:
        try:
            result = cls.from_pair_map[pair]
        except:
            raise SymbolPairConverterError(pair, cls.standard)
        return result

    @classmethod
    def to_pair(cls, value: str) -> SymbolPair:
        try:
            result = cls.to_pair_map[value]
        except:
            raise SymbolPairConverterError(value, cls.standard)
        return result
