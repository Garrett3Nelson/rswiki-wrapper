# tests/test_osrs.py

from pytest import fixture
from collections import OrderedDict

from rswiki_wrapper import Latest, Mapping, AvgPrice, TimeSeries


@fixture
def latest_keys():
    # Responsible for returning the latest price data
    return ['high', 'highTime', 'low', 'lowTime']


def test_latest_price(latest_keys):
    """Tests an API call to get the latest realtime Grand Exchange price information"""

    query_instance = Latest(id=2)
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert list(response.keys())[0] == '2', "The ID should be in the response"
    assert set(latest_keys).issubset(response['2'].keys()), "All keys should be in the response"


@fixture
def mapping_keys():
    # Returns relevant item mapping information
    return ['examine', 'id', 'members', 'lowalch', 'limit', 'value', 'highalch', 'icon', 'name']


def test_mapping_keys(mapping_keys):
    """Tests an API call to get Grand Exchange mapping information"""

    query_instance = Mapping()
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert set(mapping_keys).issubset(response.keys()), "All keys should be in the response"


@fixture
def price_keys():
    # Responsible for returning the latest price data
    return ['avgHighPrice', 'highPriceVolume', 'avgLowPrice', 'lowPriceVolume']


def test_average_price(price_keys):
    """Tests an API call to get the last 5m average Grand Exchange prices"""

    query_instance = AvgPrice('5m')
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert list(response.keys())[0] == '2', "The ID should be in the response"
    assert set(price_keys).issubset(response['2'].keys()), "All keys should be in the response"


@fixture
def timeseries_keys():
    # Responsible for returning the latest price data
    return ['timestamp', 'avgHighPrice', 'highPriceVolume', 'avgLowPrice', 'lowPriceVolume']


def test_timeseries(timeseries_keys):
    """Tests an API call to get the last 5m average Grand Exchange prices"""

    query_instance = TimeSeries(id=2, timestep='5m')
    response = query_instance.content

    assert isinstance(response[0], OrderedDict)
    assert set(timeseries_keys).issubset(response[0].keys()), "All keys should be in the response"

