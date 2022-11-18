# wikiwrapper/osrs.py
# Contains all functions for OSRS Wiki API calls

from .wiki import WikiQuery
from collections import OrderedDict


def create_url(base_url, **kwargs):
    # TODO: Validate kwargs against valid options

    if len(kwargs) == 0:
        return base_url

    # Use f-strings to format the kwargs properly
    return base_url + '?' + '&'.join(f'{k}={v}' for k, v in kwargs.items())


class RealTimeQuery(WikiQuery):
    def __init__(self, route="", endpoint="osrs", **kwargs):
        # Valid endpoints are 'osrs', 'dmm', and 'fsw'
        # https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices for full documentation

        # Valid kwargs match API endpoint
        # Latest - Optional kwargs id=X where X is the item ID
        # Mapping - No kwargs allowed
        # Price Query - Optional timestamp=X where X is the unix timestamp to return prices for
        # Time-Series - Required id=X where X is the item ID
        # Time-Series - Required timestep=X where X is any valid period ('5m', '1hr', '6hr')

        base_url = 'https://prices.runescape.wiki/api/v1/' + endpoint + '/' + route
        url = create_url(base_url, **kwargs)
        super().__init__(url)

        self.json = self.response.json(object_pairs_hook=OrderedDict)


class Latest(RealTimeQuery):
    def __init__(self, **kwargs):
        super().__init__(route="latest", **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class Mapping(RealTimeQuery):
    def __init__(self, **kwargs):
        super().__init__(route="mapping")

        # Response is [OrderedDict()] so the content is the first index in the list
        self.content = self.json[0]


class AvgPrice(RealTimeQuery):
    def __init__(self, route, **kwargs):
        # Valid routes are '5m' or '1h'

        # TODO Validate the timestamp is valid if the kwarg is used
        # TODO Validate the route is valid (5m, 1h)
        super().__init__(route, **kwargs)

        # Response is {'data': {OrderedDict()}}
        self.content = self.json['data']


class TimeSeries(RealTimeQuery):
    def __init__(self, **kwargs):
        # TODO Validate the timestep is valid (5m, 1h, 6h)
        super().__init__(route="timeseries", **kwargs)

        # Response is {'data': [{OrderedDict()}]}
        self.content = self.json['data'][0]

