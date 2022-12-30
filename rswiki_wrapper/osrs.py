# rswiki_wrapper/osrs.py
# Contains all functions for OSRS Wiki API calls

from .wiki import WikiQuery
from collections import OrderedDict


class RealTimeQuery(WikiQuery):
    """
    A class for making real-time price queries to the RuneScape Wiki API.
    
    This class extends the `WikiQuery` class and provides specific functionality for making queries to the real-time
    price endpoints of the RuneScape Wiki API. The class provides options for querying the latest prices, mapping item
    IDs to names, querying average prices over given time periods, and requesting timeseries data for specific items.

    For using each route, it is best practice to use the respective child classes.

    Args:
        route (str, optional): The specific route to query within the endpoint. Can be one of ``'latest'``,
            ``'mapping'``, ``'5m'``, `'1h'``, or ``'timeseries'``.
        game (str, optional): The specific game mode to query. Can be one of ``'osrs'``, ``'dmm'``, or ``'fsw'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.
        ``**kwargs``: Additional keyword arguments to include in the query. Varies by route.

    Attributes:
        headers (dict): The headers sent with the request object. Created from ``user_agent``
        response (:obj:`Response`): The response object provided by the ``requests`` library.
        json (dict): The raw JSON formatted response from the API. Formatted as OrderedDict for all Real-Time queries.
    """
    def __init__(self, route="", game="osrs", user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        base_url = 'https://prices.runescape.wiki/api/v1/' + game + '/' + route
        super().__init__(base_url, user_agent=user_agent, **kwargs)

        self.json = self.response.json()


class Latest(RealTimeQuery):
    """
    A class for querying the latest real-time prices from the RuneScape Wiki API. This class extends the `RealTimeQuery`
    class and provides specific functionality for making queries to the ``'latest'`` route of the real-time price API.

    Args:
        game (str, optional): The specific game mode to query. Can be one of ``'osrs'``, ``'dmm'``, or ``'fsw'``.
            Default ``'osrs'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Keyword Args:
        id (str, optional): The itemID to query if only one itemID is desired.

    Note:
        It is best practice to query all item ids (do not provide a kwarg) and to loop through the `.content` object
        for specific IDs you require. This requires only one query to the RSWiki API.

    Attributes:
        content (dict): A dict obj where the keys are all itemIDs and the values are dicts

            content format::

                {
                    item_id :
                        {
                            'high': insta_buy_price (int),
                            'highTime': insta_buy_time_unix (int),
                            'low': insta_sell_price (int),
                            'lowTime': insta_sell_time_unix (int)
                        },
                    # New key for next item_id
                }

    Example:
        Example to get a specific item ID::

            >>> query = Latest('osrs', user_agent='My Project - me@example.com')
            >>> query.content['2']
            {'high': 152, 'highTime': 1672437534, 'low': 154, 'lowTime': 1672437701}
    """
    def __init__(self, game='osrs', user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        super().__init__(route="latest", game=game, user_agent=user_agent, **kwargs)

        # Response is {'data': {}}
        self.content = self.json['data']


class Mapping(RealTimeQuery):
    """
    A class for querying the item mappings from the RuneScape Wiki API.
    
    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the
    ``'mapping'`` route of the real-time API.
    
    Args:
        game (str, optional): The specific game mode to query. Can be one of ``'osrs'``, ``'dmm'``, or ``'fsw'``.
            Default ``'osrs'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Attributes:
        content (list): A list of all item mapping information

            content format::

                [
                    {
                        'examine': examine_text (str),
                        'highalch': high_alch (int),
                        'icon': icon_name (str),
                        'id': item_id (int),
                        'limit': ge_limit (int),
                        'lowalch': low_alch (int),
                        'members': members (bool),
                        'name': name (str),
                        'value': ge_price (int)
                    }
                    # Next index is next item
                ]

    Example:
        Example to get mapping information for an item::

            >>> query = Mapping('osrs', user_agent='My Project - me@example.com')
            >>> query.content[0]
            {'examine': 'Fabulously ancient mage protection enchanted in the 3rd Age.', 'id': 10344, 'members': True,
            'lowalch': 20200, 'limit': 8, 'value': 50500, 'highalch': 30300, 'icon': '3rd age amulet.png', 'name': '3rd age amulet'}

        Example to create an item hash map::

            >>> query = Mapping('osrs', user_agent='My Project - me@example.com')
            >>> item_map = {}
            >>> for d in query.content:
            >>>     item_map[str(d['id'])] = d
            >>>     item_map[d['name']] = d
            >>> item_map['Coal']['id']
            453
    """
    def __init__(self, game='osrs', user_agent='RS Wiki API Python Wrapper - Default'):
        super().__init__(route="mapping", game=game, user_agent=user_agent)

        self.content = self.json


class AvgPrice(RealTimeQuery):
    """
    A class for querying the average real-time prices from the RuneScape Wiki API.

    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the
    ``'5m'`` or ``'1h'`` routes of the real-time API.

    Args:
        route (str): The route to query. Must be '5m' or '1h'.
        game (str, optional): The specific game mode to query. Can be one of ``'osrs'``, ``'dmm'``, or ``'fsw'``.
            Default ``'osrs'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Keyword Args:
        timestamp (str, optional): The timestamp (UNIX formatted) to begin the average calculation at.

    Attributes:
        content (dict): A dict obj where the keys are all itemIDs and the values are dicts

            content format::

                {
                    item_id :
                        {
                            'avgHighPrice': average_instabuy_price (int),
                            'avgLowPrice': average_instasell_price (int),
                            'highPriceVolume': instabuy_volume (int),
                            'lowPriceVolume': instasell_volume (int)
                        },
                    # New key for next item_id
                }

    Example:
        Example to get a specific item ID::

            >>> query = AvgPrice('5m', 'osrs', user_agent='My Project - me@example.com')
            >>> query.content['2']
            {'avgHighPrice': 158, 'highPriceVolume': 127372, 'avgLowPrice': 159, 'lowPriceVolume': 11785}
    """
    def __init__(self, route, game='osrs', user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # Valid routes are '5m' or '1h'
        assert route in ['5m', '1h'], 'Invalid route selected'

        # TODO Validate the timestamp is valid if the kwarg is used
        super().__init__(route, game=game, user_agent=user_agent, **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class TimeSeries(RealTimeQuery):
    """
    A class for querying the time-series real-time prices from the RuneScape Wiki API.

    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the
     ``'timeseries'`` route of the real-time price API. This provides timeseries information for a single Item. This
     basically provides AvgPrice information over a series of points. Length of content provided is dependent on
     continuity of data and timestep selected.

    Args:
        game (str, optional): The specific game mode to query. Can be one of ``'osrs'``, ``'dmm'``, or ``'fsw'``.
            Default ``'osrs'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Keyword Args:
        id (str, required): The itemID to provide timeseries data for.
        timestep (str, required): The period of the time-series data to retrieve. Valid values are ``'5m'``,
            ``'1h'``, or ``'6h'``.

    Attributes:
        content (dict): A dict obj where the keys are all itemIDs and the values are dicts

            content format::

                [
                    {
                        'avgHighPrice': average_instabuy_price (int),
                        'avgLowPrice': average_instasell_price (int),
                        'highPriceVolume': instabuy_volume (int),
                        'lowPriceVolume': instasell_volume (int),
                        'timestamp': unix_timestamp (int)
                    },
                    # New index for next timestep
                ]

    Example:
        Example to get a specific item ID::

            >>> query = TimeSeries('osrs', user_agent='My Project - me@example.com', id='2', timestep='5m')
            >>> query.content[0]
            {'timestamp': 1672330200, 'avgHighPrice': 162, 'avgLowPrice': 155, 'highPriceVolume': 204403, 'lowPriceVolume': 11966}
    """
    def __init__(self, game='osrs', user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # TODO Validate the timestep is valid (5m, 1h, 6h)
        super().__init__(route="timeseries", game=game, user_agent=user_agent, **kwargs)

        # Response is {'data': [{OrderedDict()}]}
        self.content = self.json['data']
