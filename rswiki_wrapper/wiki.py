# rswiki_wrapper/wiki.py
# Contains generic functions for RS Wiki API calls

import requests
import requests.utils
from collections import OrderedDict
import json
from time import sleep


class WikiQuery(object):
    def __init__(self, url, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        super().__init__()

        if user_agent == 'RS Wiki API Python Wrapper - Default':
            print("WARNING: You are using the default user_agent. Please configure the query with the parameter user_agent='{Project Name} - {Contact Information}'")

        self.headers = {
            'User-Agent': user_agent
        }
        if url != '':
            self.response = requests.get(url, headers=self.headers, params=kwargs)

    # For on-demand refreshing of a query
    def update(self, url, **kwargs):
        self.response = requests.get(url, headers=self.headers, params=kwargs)


class WeirdGloop(WikiQuery):
    def __init__(self, route, game, endpoint, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # https://api.weirdgloop.org/#/ for full documentation

        base_url = 'https://api.weirdgloop.org/' + route + game + '/' + endpoint

        super().__init__(base_url, user_agent, **kwargs)


class Exchange(WeirdGloop):
    def __init__(self, game, endpoint, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
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

        super().__init__('exchange/history/', game, endpoint, user_agent, **kwargs)
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
    def __init__(self, endpoint, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
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

        super().__init__('runescape/', game="", endpoint=endpoint, user_agent=user_agent, **kwargs)

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
    def __init__(self, game, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # Used for the overall MediaWiki API for pulling information from the wiki

        if game not in ['osrs', 'rs3']:
            print('Invalid game; choose osrs or rs3')

        if game == 'osrs':
            self.base_url = 'https://oldschool.runescape.wiki/api.php'
        else:
            self.base_url = 'https://runescape.wiki/api.php'

        self.user_agent = user_agent

        if kwargs:
            super().__init__(self.base_url, user_agent, **kwargs)
        else:
            super().__init__('', user_agent=user_agent)

        if kwargs:
            self.json = self.response.json(object_pairs_hook=OrderedDict)
            self.content = self.json
            pass
        else:
            # Create an empty object - for using built-in methods after
            self.json = None
            self.content = None

    # Use the ASK route
    def ask(self, result_format: str = 'json', conditions=None, printouts=None, offset=None, **kwargs):
        kwargs['action'] = 'ask'
        kwargs['format'] = result_format
        if isinstance(conditions, list):
            query = '[[' + ']][['.join([x.replace('[', '').replace(']', '') for x in conditions]) + ']]'

            if isinstance(printouts, list):
                query += '|?' + '|?'.join([x.replace('?', '').replace('|', '') for x in printouts])

            if offset is None:
                query_mod = ''
            else:
                query_mod = f'|offset={offset}'
            kwargs['query'] = query + query_mod

        self.update(self.base_url, self.user_agent, **kwargs)
        self.json = self.response.json()

    #
    def _get_ask_content(self, conditions: list, printouts: list, get_all=False):
        for the_name, prods in self.json['query']['results'].items():
            self.content[the_name] = []
            for printout in printouts:
                for prod in prods['printouts'][printout]:
                    #print(f'{the_name} : {prod}')
                    self.content[the_name].append(json.loads(prod))

        if get_all and self.json.get('query-continue-offset') is not None:
            # Sleep 1s to limit hits to API
            sleep(1)
            self.ask(conditions=conditions, printouts=printouts, offset=self.json.get('query-continue-offset'))

            self._get_ask_content(conditions, printouts, get_all)

    # Helper function to format a production JSON query for a specific item or category
    # item can be 'Category:Items' or 'Cake' for example or None for all Production JSON
    # All is whether to get all items (aka continue past limit of 50 items per query)
    # Note: All=True may result in many queries
    def ask_production(self, item=None, get_all: bool = False):
        if item is None:
            conditions = ['Production JSON::+']
        else:
            conditions = [item, 'Production JSON::+']

        printouts = ['Production JSON']
        self.content = {}

        self.ask(conditions=conditions, printouts=printouts)
        self._get_ask_content(conditions, printouts, get_all)

    def ask_exchange(self, item=None, get_all: bool = False):
        if item is None:
            conditions = ['Exchange JSON::+']
        else:
            conditions = ['Exchange:' + item, 'Exchange JSON::+']

        printouts = ['Exchange JSON']
        self.content = {}

        self.ask(conditions=conditions, printouts=printouts)

        if len(self.json['query']['results']) > 0:
            self._get_ask_content(conditions, printouts, get_all)

    def browse(self, result_format='json', format_version='latest', **kwargs):
        # Add required kwargs for this endpoint
        kwargs['action'] = 'smwbrowse'
        kwargs['format'] = result_format
        kwargs['formatversion'] = format_version

        # Update the class and parse the json
        self.update(self.base_url, self.user_agent, **kwargs)
        self.json = self.response.json()

    # Helper to sub out built-in property names to readable versions
    def _clean_properties(self):
        keys = self.content.keys()
        if "_INST" in keys:
            self.content['Category'] = self.content.pop('_INST')

        if "_MDAT" in keys:
            self.content['Modification Date'] = self.content.pop('_MDAT')

        if "_SKEY" in keys:
            self.content['Name'] = self.content.pop('_SKEY')

        if "_SOBJ" in keys:
            self.content['Subobject'] = self.content.pop('_SOBJ')

    # Change back to original properties
    def _dirty_properties(self):
        keys = self.content.keys()
        if "Category" in keys:
            self.content['_INST'] = self.content.pop('Category')

        if "Modification Date" in keys:
            self.content['_MDAT'] = self.content.pop('Modification Date')

        if "Name" in keys:
            self.content['_SKEY'] = self.content.pop('Name')

        if "Subobject" in keys:
            self.content['_SOBJ'] = self.content.pop('Subobject')

    def browse_properties(self, item: str):
        browse_subject = '{"subject":"' + item.replace(" ", "_") + '","ns":0,"iw":"","subobject":"","options":{"dir":null,"lang":"en-gb","group":null,"printable":null,"offset":null,"including":false,"showInverse":false,"showAll":true,"showGroup":true,"showSort":false,"api":true,"valuelistlimit.out":"30","valuelistlimit.in":"20"}}'
        self.content = {}

        self.browse(browse='subject', params=browse_subject)

        for prop in self.json['query']['data']:
            if len(prop['dataitem']) == 1:
                temp_property = prop['dataitem'][0]['item'].replace("#6##", "").replace("#14##", "").replace("#0##", "")

                # If a JSON format is detected, parse str to dict
                if "{" in temp_property:
                    temp_property = eval(temp_property)
            else:
                temp_property = []
                for item in prop['dataitem']:
                    temp_property.append(item['item'].replace("#6##", "").replace("#14##", "").replace("#0##", ""))

                    # If a JSON format is detected, parse str to dict
                    if "{" in temp_property:
                        temp_property = eval(temp_property)

            self.content[prop['property']] = temp_property
