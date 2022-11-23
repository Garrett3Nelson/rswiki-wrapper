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

        # Valid endpoints are:
        # 'vos' - no kwargs
        # 'vos/history' - kwarg 'page=X' where X is a page number
        # 'social' - kwarg 'page=X' where X is a page number
        # 'social/last' - no kwargs
        # 'tms/current' - see below
        # 'tms/next' - see below
        # kwarg 'lang=X' where X is 'en', 'pt' (english, portuguese), 'id' (returns IDs only), 'full' (returns all)
        # 'tms/search' - see documentation for full kwarg formatting
        # kwargs lang=X (optional), start=X (dateString or today), end=X (dateString or today), id=X (item ID)
        # name=X (only name OR id can be used), number=X (number of total results, number OR end can be used)

        if endpoint == 'tms/search':
            if not self._check_kwargs(**kwargs):
                print('Keyword Arguments did not pass check, see documentation for allowable args')
                self.json = None
                self.content = None
                return

        super().__init__('runescape/', game="", endpoint=endpoint, **kwargs)

        self.json = self.response.json(object_pairs_hook=OrderedDict)

        # tms data can be a list or dict, depending on the kwargs used in lang
        if isinstance(self.json, list):
            self.content = self.json
        elif 'data' in self.json.keys():
            self.content = self.json['data']
        else:
            self.content = self.json

    def _check_kwargs(self, **kwargs):
        keys = kwargs.keys()

        # Any one of the below is required kwargs
        required_args = ['start', 'number', 'name', 'id']

        if not any(x in required_args for x in keys):
            print('No accepted mandatory keys were detected')
            return False

        conflicts = [['end', 'number'], ['end', 'id']]
        for conflict in conflicts:
            # This line counts how many of each conflicting pair are in the keys. If both are there, return False
            if len([i for i in conflict if i in keys]) == len(conflict):
                print('Both conflicting pairs were detected')
                return False

        return True


class MediaWiki(WikiQuery):
    def __init__(self, endpoint, **kwargs):
        # Used for the overall MediaWiki API for pulling information from the wiki
        pass
