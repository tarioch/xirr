import pytest
from pytest import approx

from datetime import datetime
from xirr.math import xirr, cleanXirr, xnpv


@pytest.mark.parametrize("valuesPerDateString,expected", [
    ({'2019-12-31': -80005.8, '2020-03-12': 65209.6}, -0.6454),
    ({'2020-03-12': 65209.6, '2019-12-31': -80005.8}, -0.6454),
    ({'2019-12-31': -100082.76, '2020-03-05': 82671.24}, -0.6581),
    ({}, None),
    ({'2019-12-31': -100082.76}, None),
    ({'2019-12-31': -0.00001, '2020-03-05': 0.00001}, 0.0),
    ({'2019-12-31': -100, '2020-03-05': 100}, 0.0),
    ({'2019-12-31': -100, '2020-03-05': 1000}, 412461.6383),
    ({'2017-12-16': -2236.3994659663, '2017-12-26': -47.3417585212, '2017-12-29': -46.52619316339632, '2017-12-31': 10424.74612565936, '2017-12-20': -13.077972551952}, 1.2238535289956518e+16),
    ({'2018-05-09': -200, '2018-06-09': 30, '2018-11-09': 50, '2018-12-09': 20}, -0.8037),
    ({'2011-01-01': -1, '2011-01-02': 0, '2012-01-01': -1}, float("inf")),
    ({'2011-01-01': 1, '2011-01-02': 0, '2012-01-01': 1}, -float("inf"))
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
    ({'2018-05-09': -200, '2018-06-09': 30, '2018-11-09': 50, '2018-12-09': 20}, -0.8037),
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
