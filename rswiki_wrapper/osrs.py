# rswiki_wrapper/osrs.py
# Contains all functions for OSRS Wiki API calls

from .wiki import WikiQuery
from collections import OrderedDict


class RealTimeQuery(WikiQuery):
    def __init__(self, route="", endpoint="osrs", user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # Valid endpoints are 'osrs', 'dmm', and 'fsw'
        # https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices for full documentation

        # Valid kwargs match API endpoint
        # Latest - Optional kwargs id=X where X is the item ID
        # Mapping - No kwargs allowed
        # Price Query - Optional timestamp=X where X is the unix timestamp to return prices for
        # Time-Series - Required id=X where X is the item ID
        # Time-Series - Required timestep=X where X is any valid period ('5m', '1hr', '6hr')

        base_url = 'https://prices.runescape.wiki/api/v1/' + endpoint + '/' + route
        super().__init__(base_url, user_agent=user_agent, **kwargs)

        self.json = self.response.json(object_pairs_hook=OrderedDict)


class Latest(RealTimeQuery):
    def __init__(self, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        super().__init__(route="latest", user_agent=user_agent, **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class Mapping(RealTimeQuery):
    def __init__(self, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        super().__init__(route="mapping", user_agent=user_agent)

        # Response is [OrderedDict()]
        self.content = self.json


class AvgPrice(RealTimeQuery):
    def __init__(self, route, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # Valid routes are '5m' or '1h'

        # TODO Validate the timestamp is valid if the kwarg is used
        # TODO Validate the route is valid (5m, 1h)
        super().__init__(route, user_agent=user_agent, **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class TimeSeries(RealTimeQuery):
    def __init__(self, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # TODO Validate the timestep is valid (5m, 1h, 6h)
        super().__init__(route="timeseries", user_agent=user_agent, **kwargs)

        # Response is {'data': [{OrderedDict()}]}
        self.content = self.json['data']

