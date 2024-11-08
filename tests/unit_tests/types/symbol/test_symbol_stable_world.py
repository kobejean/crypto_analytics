import pytest, re

from crypto_analytics.types.symbol import (Symbol, SymbolPair, SymbolStandard,
    StableWorldSymbolPairConverter, SymbolPairConverterError)

# test stable_world symbol pair converter

def test_stable_world_symbol_pair_converter_map_bijection():
    # given
    pairs = list(StableWorldSymbolPairConverter.from_pair_map.keys())
    # when
    values = [StableWorldSymbolPairConverter.from_pair_map[pair] for pair in pairs]
    recovered_pairs = [StableWorldSymbolPairConverter.to_pair_map[value] for value in values]
    # then
    expected = pairs
    assert recovered_pairs == expected

def test_stable_world_symbol_pair_converter_get_standard():
    # when
    standard = StableWorldSymbolPairConverter.standard
    # then
    expected = SymbolStandard.STABLE_WORLD
    assert standard == expected


# test from_pair

def test_stable_world_symbol_pair_converter_from_pair_success():
    # given
    pair = SymbolPair(Symbol.VND, Symbol.JPY)
    # when
    converted = StableWorldSymbolPairConverter.from_pair(pair)
    # then
    expected = 'VNDJPY'
    assert converted == expected

def test_stable_world_symbol_pair_converter_from_pair_failure():
    # given
    pair = SymbolPair(None, None)
    # when/then
    with pytest.raises(SymbolPairConverterError) as excinfo:
        converted = StableWorldSymbolPairConverter.from_pair(pair)
    # then
    expected = SymbolPairConverterError(pair, SymbolStandard.STABLE_WORLD)
    assert str(excinfo.value) == str(expected)


# test to_pair

def test_stable_world_symbol_pair_converter_to_pair_success():
    # given
    value = 'VNDJPY'
    # when
    converted = StableWorldSymbolPairConverter.to_pair(value)
    # then
    expected = SymbolPair(Symbol.VND, Symbol.JPY)
    assert converted == expected

def test_stable_world_symbol_pair_converter_to_pair_failure():
    # given
    value = None
    # when/then
    with pytest.raises(SymbolPairConverterError) as excinfo:
        converted = StableWorldSymbolPairConverter.to_pair(value)
    # then
    expected = SymbolPairConverterError(value, SymbolStandard.STABLE_WORLD)
    assert str(excinfo.value) == str(expected)
