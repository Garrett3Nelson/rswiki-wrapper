# tests/test_wiki.py

from pytest import fixture
from collections import OrderedDict

from wikiwrapper import Exchange


@fixture
def exchange_keys():
    # Responsible for returning the latest price data
    return ['id', 'timestamp', 'price', 'volume']


def test_exchange_latest(exchange_keys):
    """Tests an API call to get the latest realtime Grand Exchange price information"""

    query_instance = Exchange('osrs', 'latest', id='2|6')
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert list(response.keys())[0] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response['2'].keys()), "All keys should be in the response"


def test_exchange_history(exchange_keys):
    """Tests an API call to get the latest realtime Grand Exchange price information"""

    query_instance = Exchange('osrs', 'last90d', id='2')
    response = query_instance.content

    assert isinstance(response[0], OrderedDict)
    assert response[0]['id'] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response[0].keys()), "All keys should be in the response"