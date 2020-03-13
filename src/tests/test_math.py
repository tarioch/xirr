import pytest
from datetime import datetime
from xirr.math import xirr


@pytest.mark.parametrize("valuesPerDateString,expected", [({'2019-12-31': -80005.8, '2020-03-12': 65209.6}, -0.6453638827)])
def test_xirr(valuesPerDateString, expected):
    valuesPerDate = {datetime.fromisoformat(k).date: v for k, v in valuesPerDateString.items()}
    assert xirr(valuesPerDate) == expected
