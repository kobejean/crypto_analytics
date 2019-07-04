import pytest, re

from crypto_analytics.types.symbol import Symbol, SymbolPair, SymbolStandard, SymbolPairConverterError

# test symbol pair converter error

def test_symbol_pair_converter_error_message():
    # given
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    standard = SymbolStandard.KRAKEN
    # when/then
    error_msg_regx = re.compile('(?=.*bitcoin)(?=.*usd)(?=.*kraken)(?=.*failed)', re.IGNORECASE)
    with pytest.raises(SymbolPairConverterError, match=error_msg_regx):
        raise SymbolPairConverterError(pair, standard)

def test_symbol_pair_converter_error_obj():
    # given
    pair = SymbolPair(Symbol.LITECOIN, Symbol.USD)
    standard = SymbolStandard.KRAKEN
    # when/then
    with pytest.raises(SymbolPairConverterError) as excinfo:
        raise SymbolPairConverterError(pair, standard)
    # then
    expected = pair
    assert excinfo.value.obj == expected

def test_symbol_pair_converter_error_standard():
    # given
    pair = SymbolPair(Symbol.BITCOIN, Symbol.USD)
    standard = SymbolStandard.CRYPTO_COMPARE
    # when/then
    with pytest.raises(SymbolPairConverterError) as excinfo:
        raise SymbolPairConverterError(pair, standard)
    # then
    expected = standard
    assert excinfo.value.standard == expected
