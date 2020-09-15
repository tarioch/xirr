import pytest
from pytest import approx

from datetime import datetime
from xirr.math import xirr, cleanXirr, xnpv


@pytest.mark.parametrize("valuesPerDateString,expected", [
    ({'2019-12-31': -80005.8, '2020-03-12': 65209.6}, -0.6454),
    ({'2020-03-12': 65209.6, '2019-12-31': -80005.8}, -0.6454),
    ({'2019-12-31': -100082.76, '2020-03-05': 82671.24}, -0.6581),
    ({}, None),
    ({'2019-12-31': -100082.76}, -float("inf")),
    ({'2022-10-12': 200}, float("inf")),
    ({'2019-12-31': -0.00001, '2020-03-05': 0.00001}, 0.0),
    ({'2019-12-31': -100, '2020-03-05': 100}, 0.0),
    ({'2019-12-31': -100, '2020-03-05': 1000}, 412461.6383),
    ({'2017-12-16': -2236.3994659663, '2017-12-26': -47.3417585212, '2017-12-29': -46.52619316339632, '2017-12-31': 10424.74612565936, '2017-12-20': -13.077972551952}, 1.2238535289956518e+16),
    ({'2018-05-09': -200, '2018-06-09': 30, '2018-11-09': 50, '2018-12-09': 20}, -0.8037),
    ({'2011-01-01': -1, '2011-01-02': 0, '2012-01-01': -1}, -float("inf")),
    ({'2011-01-01': 1, '2011-01-02': 0, '2012-01-01': 1}, float("inf")),
    ({'2011-07-01': -10000, '2014-07-01': 1}, -0.9535),
    ({'2011-07-01': 10000, '2014-07-01': -1}, -0.9535),
    ({
        '2015-08-03': 5046,
        '2015-10-20': 5037.3,
        '2016-01-11': 4995.25,
        '2016-04-06': 5795.5,
        '2016-04-26': -1085.6,
        '2016-07-19': 4998,
        '2016-10-11': 4557.8,
        '2017-01-11': 4815,
        '2017-04-11': 4928,
        '2017-04-25': -2197.05,
        '2017-10-12': 5424,
        '2018-04-24': -2565,
        '2019-04-23': -2872.8,
        '2020-02-25': 10085,
        '2020-03-03': 9500,
        '2020-03-09': 9976.8,
        '2020-04-06': 14880,
        '2020-04-23': -6094.7,
        '2020-06-05': 19522.36,
        '2020-08-05': 18035,
        '2020-08-19': 10477.44}, -0.9999),
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
    ({'2011-01-01': 1, '2011-01-02': 0, '2012-01-01': 1}, None),
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
