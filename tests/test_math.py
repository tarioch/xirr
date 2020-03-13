import pytest
from pytest import approx

from datetime import datetime
from xirr.math import xirr, cleanXirr, xnpv


@pytest.mark.parametrize("valuesPerDateString,expected", [
    ({'2019-12-31': -80005.8, '2020-03-12': 65209.6}, -0.6454),
    ({'2020-03-12': 65209.6, '2019-12-31': -80005.8}, -0.6454),
    ({'2019-12-31': -100082.76, '2020-03-05': 82671.24}, -0.6581),
    ({}, None),
    ({'2019-12-31': -0.00001, '2020-03-05': 0.00001}, 0.0),
    ({'2019-12-31': -100, '2020-03-05': 100}, 0.0),
    ({'2019-12-31': -100, '2020-03-05': 1000}, 412461.6383),
])
def test_xirr(valuesPerDateString, expected):
    valuesPerDate = {datetime.fromisoformat(k).date(): v for k, v in valuesPerDateString.items()}
    actual = xirr(valuesPerDate)
    if expected:
        assert round(actual, 4) == expected
    else:
        assert actual == expected


@pytest.mark.parametrize("valuesPerDateString,expected", [
    ({'2019-12-31': -80005.8, '2020-03-12': 65209.6}, -0.6454),
    ({'2020-03-12': 65209.6, '2019-12-31': -80005.8}, -0.6454),
    ({'2019-12-31': -100082.76, '2020-03-05': 82671.24}, -0.6581),
    ({}, None),
    ({'2019-12-31': -0.00001, '2020-03-05': 0.00001}, None),
    ({'2019-12-31': -100, '2020-03-05': 100}, None),
    ({'2019-12-31': -100, '2020-03-05': 1000}, None),
])
def test_cleanXirr(valuesPerDateString, expected):
    valuesPerDate = {datetime.fromisoformat(k).date(): v for k, v in valuesPerDateString.items()}
    actual = cleanXirr(valuesPerDate)
    if expected:
        assert round(actual, 4) == expected
    else:
        assert actual == expected


@pytest.mark.parametrize("valuesPerDateString,rate,expected", [
    ({'2019-12-31': -100, '2020-12-31': 110}, -1.0, float('inf')),
    ({'2019-12-31': -100, '2020-12-31': 110}, -0.10, 22.2575),
])
def test_xnpv(valuesPerDateString, rate, expected):
    valuesPerDate = {datetime.fromisoformat(k).date(): v for k, v in valuesPerDateString.items()}
    actual = xnpv(valuesPerDate, rate)
    if expected:
        assert actual == approx(expected, 0.0001)
    else:
        assert actual == expected
