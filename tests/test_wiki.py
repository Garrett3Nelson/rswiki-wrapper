# tests/test_wiki.py

from pytest import fixture
from rswiki_wrapper import Exchange, Runescape, MediaWiki


@fixture
def exchange_keys():
    # Keys that are returned by a successful query
    return ['id', 'timestamp', 'price', 'volume']


def test_exchange_latest(exchange_keys):
    """Tests an API call to get the latest Grand Exchange price information"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Exchange('rs', 'latest', id='2|453', user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response, dict)
    assert list(response.keys())[0] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response['2'][0].keys()), "All keys should be in the response"


def test_exchange_history(exchange_keys):
    """Tests an API call to get Grand Exchange price history"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Exchange('osrs', 'last90d', id='2', user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response['2'][0], dict)
    assert response['2'][0]['id'] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response['2'][0].keys()), "All keys should be in the response"


@fixture
def vos_keys():
    # Keys that are returned by the vos query
    return['timestamp', 'district1', 'district2']


def test_vos(vos_keys):
    """Tests an API call to get Voice of Seren information"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('vos', user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response, dict)
    assert set(vos_keys).issubset(response.keys()), "All keys should be in the response"


def test_vos_history(vos_keys):
    """Tests an API call to get Voice of Seren History"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('vos/history', page=2, user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response[0], dict)
    assert set(vos_keys).issubset(response[0].keys()), "All keys should be in the response"


@fixture
def social_keys():
    # Keys that are returned by the social query
    return['id', 'url', 'title', 'excerpt', 'author', 'curator', 'source', 'image', 'icon', 'expiryDate',
           'datePublished', 'dateAdded']


def test_social_last(social_keys):
    """Tests an API call to get Social Posts information"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('social/last', user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response, dict)
    assert set(social_keys).issubset(response.keys()), "All keys should be in the response"


def test_social(social_keys):
    """Tests an API call to get Social Posts History"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('social', page=2, user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response[0], dict)
    assert set(social_keys).issubset(response[0].keys()), "All keys should be in the response"


@fixture
def tms_keys():
    # Keys that are returned by the tms query - assuming full is used (otherwise no keys)
    return['id', 'en', 'pt']


def test_tms_current(tms_keys):
    """Tests an API call to get Traveling Merchant Shop information"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('tms/current', lang='full', user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response, list)
    assert set(tms_keys).issubset(response[0].keys()), "All keys should be in the response"


def test_tms_next(tms_keys):
    """Tests an API call to get tomorrow's Traveling Merchant Shop information"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('tms/next', lang='full', user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response, list)
    assert set(tms_keys).issubset(response[0].keys()), "All keys should be in the response"


def test_tms_search(tms_keys):
    """Tests and API call to search Traveling Merchant Shop Information"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = Runescape('tms/search', lang='full', start='today', end='25 November 2022', number=3, user_agent=user_agent)
    response = query_instance.content

    # The above should fail (kwarg check, uses conflicting arguments end & number)
    assert response is None

    # The below should be successful
    query_instance = Runescape('tms/search', lang='full', start='today', number=3, user_agent=user_agent)
    response = query_instance.content

    assert isinstance(response, list)
    assert set(tms_keys).issubset(response[0]['items'][0].keys()), "All keys should be in the response"


def test_media_wiki():
    """Tests the MediaWiki Routes"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = MediaWiki('osrs', action='ask', format='json', query='[[Category:Items]][[Production JSON::+]]|?Production JSON', user_agent=user_agent)
    response = query_instance.response

    assert response.status_code == 200


@fixture
def production_keys():
    # Keys that are returned by the Ask query
    return['ticks', 'materials', 'facilities', 'skills', 'members', 'output']


def test_ask_production(production_keys):
    """Tests the MediaWiki Ask - Production JSON Request"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = MediaWiki('osrs', user_agent=user_agent)

    item = 'Cake'
    query_instance.ask_production(item=item)
    response = query_instance.content

    assert isinstance(response, dict), "Response should be a json item"
    assert item in response.keys(), "Item name should be the key in content"
    assert set(production_keys).issubset(response[item][0].keys()), "All keys should be in the response"


@fixture
def exchange_json_keys():
    # Keys that are returned by the Ask query
    return['historical', 'id', 'lowalch', 'highalch', 'isalchable', 'value', 'limit', 'info', 'name']


def test_ask_exchange(exchange_json_keys):
    """Tests the MediaWiki Ask - Exchange JSON Request"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = MediaWiki('osrs', user_agent=user_agent)

    item = 'Cake'
    query_instance.ask_exchange(item=item)
    response = query_instance.content

    item = 'Exchange:' + item

    assert isinstance(response, dict), "Response should be a json item"
    assert item in response.keys(), "Item name should be the key in content"
    assert set(exchange_json_keys).issubset(response[item][0].keys()), "All keys should be in the response"


def test_browse():
    pass


@fixture
def property_keys():
    # Keys that are returned by the tms query - assuming full is used (otherwise no keys)
    return['All_Image', 'All_Is_members_only', 'All_Item_ID', 'All_Weight', 'Category']


def test_browse_properties(property_keys):
    """Tests the MediaWiki Browse - Properties Request"""

    user_agent = 'RS Wiki API Python Wrapper - Test Suite'
    query_instance = MediaWiki('osrs', user_agent=user_agent)

    item = 'Cake'
    query_instance.browse_properties(item=item)
    query_instance._clean_properties()
    response = query_instance.content

    assert isinstance(response, dict), "Response should be a json item"
    assert item in response.get('Name'), "Item name should be the key in content"
    assert set(property_keys).issubset(response.keys()), "All keys should be in the response"
