# rswiki_wrapper/osrs.py
# Contains all functions for OSRS Wiki API calls

from .wiki import WikiQuery
from collections import OrderedDict


class RealTimeQuery(WikiQuery):
    """
    A class for making real-time price queries to the RuneScape Wiki API.
    
    This class extends the `WikiQuery` class and provides specific functionality for making queries to the real-time price endpoints of the RuneScape Wiki API. The class provides options for querying the latest prices, mapping item IDs to names, and requesting time-series data for specific items.
    
    :param route: The specific route to query within the endpoint. Can be one of 'latest', 'mapping', 'price-query', or 'time-series'.
    :type route: str, optional
    :param endpoint: The specific endpoint to query. Can be one of 'osrs', 'dmm', or 'fsw'.
    :type endpoint: str, optional
    :param user_agent: The user agent string to include in the HTTP request headers.
    :type user_agent: str, optional
    :param \**kwargs: Additional keyword arguments to include in the query parameters. Valid arguments depend on the route and endpoint being queried.
    :type \**kwargs: Any, optional
    
    .. attribute:: json
       :type: dict
    
        The raw JSON response from the API.
    """
    def __init__(self, route="", endpoint="osrs", user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        base_url = 'https://prices.runescape.wiki/api/v1/' + endpoint + '/' + route
        super().__init__(base_url, user_agent=user_agent, **kwargs)

        self.json = self.response.json(object_pairs_hook=OrderedDict)


class Latest(RealTimeQuery):
    """
    A class for querying the latest real-time prices from the RuneScape Wiki API.
    
    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the 'latest' route of the real-time price endpoints of the RuneScape Wiki API. The class provides options for querying the latest prices for specific items.
    
    :param user_agent: The user agent string to include in the HTTP request headers.
    :type user_agent: str, optional
    :param game: The game type to provide prices. Valid games 'osrs', 'dmm', and 'fsw'. Default OSRS
    :type game: str, optional
    :param \**kwargs: For this endpoint, the optional keyword is 'id' and the value is the itemID to query.
    :type \**kwargs: str, optional

    .. note:: It is best practice to query all item ids (do not provide a kwarg) and to loop through the `.content` object for specific IDs you require. This requires only one query to the RSWiki API.
    
    .. attribute:: content
       :type: dict
    
        The real-time prices for the items specified in the query.
        
    """
    def __init__(self, game='osrs', user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        super().__init__(route="latest", endpoint=game, user_agent=user_agent, **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class Mapping(RealTimeQuery):
    """
    A class for querying the item mappings from the RuneScape Wiki API.
    
    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the 'mapping' route of the real-time price endpoints of the RuneScape Wiki API. The class provides options for querying the item mappings available in the API.
    
    :param game: The game type to provide prices. Valid games 'osrs', 'dmm', and 'fsw'. Default OSRS
    :type game: str, optional
    :param user_agent: The user agent string to include in the HTTP request headers.
    :type user_agent: str, optional
    
    .. attribute:: content
       :type: list
    
        The item mappings available in the API.
    
    .. note:: No additional keyword arguments are required for this class.
    
    """
    def __init__(self, game='osrs', user_agent='RS Wiki API Python Wrapper - Default'):
        super().__init__(route="mapping", endpoint=game, user_agent=user_agent)

        # Response is [OrderedDict()]
        self.content = self.json


class AvgPrice(RealTimeQuery):
    """
    A class for querying the average real-time prices from the RuneScape Wiki API.

    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the '5m' or '1h' routes of the real-time price endpoints of the RuneScape Wiki API. The class provides options for querying the average prices for specific items at different time intervals.

    :param route: The route to query. Must be '5m' or '1h'.
    :type route: str
    :param game: The game type to provide prices. Valid games 'osrs', 'dmm', and 'fsw'. Default OSRS
    :type game: str, optional
    :param user_agent: The user agent string to include in the HTTP request headers.
    :type user_agent: str, optional
    :param \**kwargs: For both endpoints, 'timestamp' is the keyword and the value is the UNIX formatted timestamp to begin the average.
    :type \**kwargs: str, optional

    .. attribute:: content
       :type: dict

        The average real-time prices for items.

    """
    def __init__(self, route, game='osrs', user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # Valid routes are '5m' or '1h'

        # TODO Validate the timestamp is valid if the kwarg is used
        # TODO Validate the route is valid (5m, 1h)
        super().__init__(route, endpoint=game, user_agent=user_agent, **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class TimeSeries(RealTimeQuery):
    """
    A class for querying the time-series real-time prices from the RuneScape Wiki API.

    This class extends the `RealTimeQuery` class and provides specific functionality for making queries to the 'timeseries' route of the real-time price endpoints of the RuneScape Wiki API. The class provides options for querying the time-series data for specific items.

    :param game: The game type to provide prices. Valid games 'osrs', 'dmm', and 'fsw'. Default OSRS
    :type game: str, optional
    :param user_agent: The user agent string to include in the HTTP request headers.
    :type user_agent: str, optional
    :param \**kwargs: Additional keyword arguments to include in the query parameters. See note below for description of required kwargs
    :type \**kwargs: str, required

    .. attribute:: content
       :type: list

        The time-series real-time prices for the item specified in the query.

    .. note:: Keyword arguments are required as follows:

       - Required keyword argument 'id' with a value of the item ID for which to retrieve time-series data.
       - Required keyword argument 'timestep' with a value of the period of the time-series data to retrieve. Valid values are '5m', '1h', or '6h'.

    """
    def __init__(self, game='osrs', user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # TODO Validate the timestep is valid (5m, 1h, 6h)
        super().__init__(route="timeseries", endpoint=game, user_agent=user_agent, **kwargs)

        # Response is {'data': [{OrderedDict()}]}
        self.content = self.json['data']
