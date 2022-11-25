# tests/test_wiki.py

from pytest import fixture
from collections import OrderedDict

from wikiwrapper import Exchange, Runescape, MediaWiki


@fixture
def exchange_keys():
    # Keys that are returned by a successful query
    return ['id', 'timestamp', 'price', 'volume']


def test_exchange_latest(exchange_keys):
    """Tests an API call to get the latest Grand Exchange price information"""

    query_instance = Exchange('rs', 'latest', id='2|6')
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert list(response.keys())[0] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response['2'].keys()), "All keys should be in the response"


def test_exchange_history(exchange_keys):
    """Tests an API call to get Grand Exchange price history"""

    query_instance = Exchange('osrs', 'last90d', id='2')
    response = query_instance.content

    assert isinstance(response[0], OrderedDict)
    assert response[0]['id'] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response[0].keys()), "All keys should be in the response"


@fixture
def vos_keys():
    # Keys that are returned by the vos query
    return['timestamp', 'district1', 'district2']


def test_vos(vos_keys):
    """Tests an API call to get Voice of Seren information"""

    query_instance = Runescape('vos')
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert set(vos_keys).issubset(response.keys()), "All keys should be in the response"


def test_vos_history(vos_keys):
    """Tests an API call to get Voice of Seren History"""

    query_instance = Runescape('vos/history', page=2)
    response = query_instance.content

    assert isinstance(response[0], OrderedDict)
    assert set(vos_keys).issubset(response[0].keys()), "All keys should be in the response"


@fixture
def social_keys():
    # Keys that are returned by the social query
    return['id', 'url', 'title', 'excerpt', 'author', 'curator', 'source', 'image', 'icon', 'expiryDate',
           'datePublished', 'dateAdded']


def test_social_last(social_keys):
    """Tests an API call to get Social Posts information"""

    query_instance = Runescape('social/last')
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert set(social_keys).issubset(response.keys()), "All keys should be in the response"


def test_social(social_keys):
    """Tests an API call to get Social Posts History"""

    query_instance = Runescape('social', page=2)
    response = query_instance.content

    assert isinstance(response[0], OrderedDict)
    assert set(social_keys).issubset(response[0].keys()), "All keys should be in the response"


@fixture
def tms_keys():
    # Keys that are returned by the tms query - assuming full is used (otherwise no keys)
    return['id', 'en', 'pt']


def test_tms_current(tms_keys):
    """Tests an API call to get Traveling Merchant Shop information"""

    query_instance = Runescape('tms/current', lang='full')
    response = query_instance.content

    assert isinstance(response, list)
    assert set(tms_keys).issubset(response[0].keys()), "All keys should be in the response"


def test_tms_next(tms_keys):
    """Tests an API call to get tomorrow's Traveling Merchant Shop information"""

    query_instance = Runescape('tms/next', lang='full')
    response = query_instance.content

    assert isinstance(response, list)
    assert set(tms_keys).issubset(response[0].keys()), "All keys should be in the response"


def test_tms_search(tms_keys):
    """Tests and API call to search Traveling Merchant Shop Information"""

    query_instance = Runescape('tms/search', lang='full', start='today', end='25 November 2022', number=3)
    response = query_instance.content

    # The above should fail (kwarg check, uses conflicting arguments end & number)
    assert response is None

    # The below should be successful
    query_instance = Runescape('tms/search', lang='full', start='today', number=3)
    response = query_instance.content

    assert isinstance(response, list)
    assert set(tms_keys).issubset(response[0]['items'][0].keys()), "All keys should be in the response"


def test_media_wiki():
    """Tests the MediaWiki Routes"""

    query_instance = MediaWiki('osrs', action='ask', format='json', query='[[Category:Items]][[Production JSON::+]]|?Production')
    response = query_instance.response

    assert response.status_code == 200
