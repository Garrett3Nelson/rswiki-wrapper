# wikiwrapper/wiki.py
# Contains generic functions for RS Wiki API calls

import requests
from config import USER_AGENT
from collections import OrderedDict


class WikiQuery(object):
    def __init__(self, url, **kwargs):
        super().__init__()

        headers = {
            'User-Agent': USER_AGENT
        }

        self.response = requests.get(url, headers=headers)


def create_url(base_url, **kwargs):
    # TODO: Validate kwargs against valid options

    if len(kwargs) == 0:
        return base_url

    # Use f-strings to format the kwargs properly
    return base_url + '?' + '&'.join(f'{k}={v}' for k, v in kwargs.items())


class WeirdGloop(WikiQuery):
    def __init__(self, route, game, endpoint, **kwargs):
        # https://api.weirdgloop.org/#/ for full documentation

        base_url = 'https://api.weirdgloop.org/' + route + game + '/' + endpoint
        url = create_url(base_url, **kwargs)

        super().__init__(url)


class Exchange(WeirdGloop):
    def __init__(self, game, endpoint, **kwargs):
        # Used for latest / historical prices. Use RealTimeQuery for real-time OSRS prices
        # Valid games are 'rs', 'rs-fsw-2022', 'osrs', 'osrs-fsw-2022'
        # Valid endpoints are 'latest', 'all', 'last90d', and 'sample'
        # https://api.weirdgloop.org/#/ for full documentation

        # Valid kwargs match API endpoint
        # For latest: required kwargs are EITHER by ID or Name.
        # For ID use "id=X" where X = itemID OR a trade index like 'GE Common Trade Index'
        # For Name use "name=X" where name is the exact GE name
        # For latest: multiple id or names can be used with "|" as the separator ie id='2|4'
        # This option is not available in any of the history (all, last90d, sample) modes

        super().__init__('exchange/history/', game, endpoint, **kwargs)
        self.json = self.response.json(object_pairs_hook=OrderedDict)

        # Exposing .content as the "user desired data" for consistency
        # For latest - there is only one entry per ID (an OrderedDict where the itemIDs are keys)
        # For history - there are many entries and one ID (a list of OrderedDict where each index is 1 day)
        # TODO unify the latest/history .context usage for consistency

        if endpoint != 'latest':
            # for all history items, the returned JSON is {id: [{OrderedDict()}]}
            self.content = list(self.json.items())[0][1]
        else:
            self.content = self.json


class Runescape(WeirdGloop):
    def __init__(self, endpoint, **kwargs):
        # Used for the general endpoints for Runescape information
        pass


class MediaWiki(WikiQuery):
    def __init__(self, endpoint, **kwargs):
        # Used for the overall MediaWiki API for pulling information from the wiki
        pass
