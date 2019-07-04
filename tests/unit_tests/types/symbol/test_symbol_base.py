import pytest, re

from crypto_analytics.types.symbol import Symbol, SymbolPair, SymbolStandard, SymbolPairConverterError

# test symbol pair converter error

def test_symbol_pair_converter_error_message():
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    standard = SymbolStandard.KRAKEN
    error_msg_regx = re.compile('(?=.*bitcoin)(?=.*usd)(?=.*kraken)(?=.*failed)', re.IGNORECASE)
    with pytest.raises(SymbolPairConverterError, match=error_msg_regx):
        raise SymbolPairConverterError(pair, standard)

def test_symbol_pair_converter_error_obj():
    pair = SymbolPair(Symbol.LITECOIN, Symbol.USD)
    standard = SymbolStandard.KRAKEN
    with pytest.raises(SymbolPairConverterError) as excinfo:
        raise SymbolPairConverterError(pair, standard)
    assert excinfo.value.obj == pair

def test_symbol_pair_converter_error_standard():
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    standard = SymbolStandard.CRYPTO_COMPARE
    with pytest.raises(SymbolPairConverterError) as excinfo:
        raise SymbolPairConverterError(pair, standard)
    assert excinfo.value.standard == standard
