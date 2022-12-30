# rswiki_wrapper/wiki.py
# Contains generic functions for RS Wiki API calls

import requests
import requests.utils
from collections import OrderedDict
import json
from time import sleep


class WikiQuery(object):
    """
    A class for querying the RS Wiki API.

    :param url: The URL of the API endpoint to query.
    :param user_agent: (optional) The user agent string to use for the request. Default is 'RS Wiki API Python Wrapper - Default'.
    :param ``**kwargs``: (optional) Additional parameters to include in the query.
    """
    def __init__(self, url, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        super().__init__()

        if user_agent == 'RS Wiki API Python Wrapper - Default':
            print("WARNING: You are using the default user_agent. Please configure the query with the parameter user_agent='{Project Name} - {Contact Information}'")

        self.headers = {
            'User-Agent': user_agent
        }
        if url != '':
            self.response = requests.get(url, headers=self.headers, params=kwargs)

    def update(self, url, **kwargs):
        """
        Refresh the query with a new URL and additional parameters.

        :param url: The URL of the API endpoint to query.
        :param ``**kwargs``: (optional) Additional parameters to include in the query.
        """
        self.response = requests.get(url, headers=self.headers, params=kwargs)



class WeirdGloop(WikiQuery):
    """
    This class extends the `WikiQuery` class to make queries to the Weird Gloop API.
    For general usage, it is recommended to use the specific Exchange or Runescape child classes.

    :param route: The route of the Weird Gloop API to query.
    :param game: The game to query in the Weird Gloop API.
    :param endpoint: The endpoint of the Weird Gloop API to query.
    :param user_agent: The user agent string to use in the query.
    :param ``**kwargs``: Additional keyword arguments to pass.

    Example:
        query = WeirdGloop('exchange/history', 'osrs', 'latest', user_agent='My Project - me@example.com', id=2)
    """
    def __init__(self, route, game, endpoint, user_agent, **kwargs):
        # https://api.weirdgloop.org/#/ for full documentation

        base_url = 'https://api.weirdgloop.org/' + route + game + '/' + endpoint

        super().__init__(base_url, user_agent, **kwargs)



class Exchange(WeirdGloop):
    """
    This class extends the `WeirdGloop` class to make queries to the exchange history endpoint of the Weird Gloop API.

    :param game: The game to query in the Weird Gloop API. Valid options are 'rs', 'rs-fsw-2022', 'osrs', 'osrs-fsw-2022'.
    :param endpoint: The endpoint of the Weird Gloop API to query. Valid options are 'latest', 'all', 'last90d', and 'sample'.
    :param user_agent: The user agent string to use in the query. Default is 'RS Wiki API Python Wrapper - Default'.
    :param ``**kwargs``: Additional keyword arguments to pass to the `requests.get` function.
        - Required arguments are either 'id' or 'name', where 'id' is a single item ID or a trade index like 'GE Common Trade Index', and 'name' is the exact GE name of the item. Multiple 'id' or 'name' values can be provided as a pipe-separated string, e.g. "id='2|4'" or "name='Adamant arrow|Rune arrow'".
        - For the 'all', 'last90d', and 'sample' endpoints, multiple item ID or names cannot be provided.

    Example:
        query = Exchange('osrs', 'latest', user_agent='My Project - me@example.com', id='2|4')
        query = Exchange('osrs', 'all', user_agent='My Project - me@example.com', name='Coal')
    """
    def __init__(self, game, endpoint, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # https://api.weirdgloop.org/#/ for full documentation

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
    """
    This class extends the `WeirdGloop` class to make queries to the general endpoints of the Weird Gloop API for Runescape information.

    :param endpoint: The endpoint of the Weird Gloop API to query. Valid options are 'vos', 'vos/history', 'social', 'social/last', 'tms/current', 'tms/next', and 'tms/search'.
    :param user_agent: The user agent string to use in the query.
    :param ``**kwargs``: Additional keyword arguments to pass to the `requests.get` function.
        - For the 'vos/history' and 'social' endpoints, a 'page' keyword argument is required, with a page number as the value.
        - For the 'tms/current' and 'tms/next' endpoints a 'lang' keyword is required, valid values are 'en', 'pt', 'id' (item IDs only), and 'full' (all information)
        - For the 'tms/search' endpoint, the following keyword arguments are accepted: 'lang' (optional, default is 'en'), 'start' (date string or 'today'), 'end' (date string or 'today'), 'id' (item ID), 'name' (exact name of the item), and 'number' (number of results to return). Either 'id' or 'name' is required, and either 'end' or 'number' is required.

    Example:
        query = Runescape('tms/search', user_agent='My Project - me@example.com', lang='en', start='2022-01-01', end='2022-01-07', id='42274')
        query = Runescape('social', user_agent='My Project - me@example.com', page='2')
    """
    def __init__(self, endpoint, user_agent, **kwargs):
        # Used for the general endpoints for Runescape information

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
        """
        This method checks the keyword arguments passed to the `Runescape` class for the 'tms/search' endpoint to ensure that they are valid and do not conflict with each other.

        :param ``**kwargs``: The keyword arguments to check.
        :return: A boolean indicating whether the keyword arguments are valid and do not conflict.
        """
        required_args = ['start', 'number', 'name', 'id']
        conflicts = [['end', 'number'], ['name', 'id']]

        if not any(arg in kwargs for arg in required_args):
            return False

        for conflict in conflicts:
            if all(arg in kwargs for arg in conflict):
                return False

        return True


class MediaWiki(WikiQuery):
    """
    This class is used to access the MediaWiki API for pulling information from the Wiki. 
    
    :param game: A string indicating the game for which to pull information. Valid options are 'osrs' and 'rs3'.
    :type game: str, optional
    :param user_agent: A string indicating the user agent to use when making requests.
    :type user_agent: str, optional

    .. attribute:: json
       :type: dict
    
        The raw JSON response from the API.
    """
    def __init__(self, game, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
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
        """
        This method sends an ASK query to the MediaWiki API using the specified `conditions` and `printouts` parameters, and optional `offset` parameter. The `result_format` specifies the format in which the response is returned.
        
        :param result_format: The format in which the response is returned. Default is 'json'.
        :param conditions: A list of strings representing the conditions of the ASK query.
        :param printouts: A list of strings representing the printouts of the ASK query.
        :param offset: An optional integer representing the offset for the ASK query.
        :param ``**kwargs``: Additional keyword arguments to pass to the MediaWiki API.
        
        Example:
        query = MediaWiki('osrs')
        query.ask(conditions=['Mod:Ikov', 'Mod:Saloon bar'], printouts=['Mod:Ikov', 'Mod:Saloon bar'])
        query.json  # Returns the JSON response from the API
        """
        kwargs['action'] = 'ask'
        kwargs['format'] = result_format
        if isinstance(conditions, list):
            # Join the conditions with ']][[' and remove the brackets from each element
            query = '[[' + ']][['.join([x.replace('[', '').replace(']', '') for x in conditions]) + ']]'

            if isinstance(printouts, list):
                # Join the printouts with '|?' and remove the brackets and pipes from each element
                query += '|?' + '|?'.join([x.replace('?', '').replace('|', '') for x in printouts])

            # If the offset is not specified, set the query modification to an empty string
            if offset is None:
                query_mod = ''
            # Otherwise, set the query modification to the specified offset
            else:
                query_mod = f'|offset={offset}'
            kwargs['query'] = query + query_mod

        # Send the ASK query to the API and update the response
        self.update(self.base_url, **kwargs)
        self.json = self.response.json()

    def _get_ask_content(self, conditions: list, printouts: list, get_all: bool = False) -> None:
        """
        A helper function to retrieve content from an ASK query in the MediaWiki API.

        :param conditions: A list of conditions for the ASK query.
        :type conditions: list of str
        :param printouts: A list of printouts for the ASK query.
        :type printouts: list of str
        :param get_all: Whether to retrieve all results from the ASK query.
        :type get_all: bool
        """
        # Iterate over the results of the query
        for the_name, prods in self.json['query']['results'].items():
            # Initialize an empty list to store the printout values for this result
            self.content[the_name] = []
            # Iterate over the printouts for this result
            for printout in printouts:
                # Iterate over the values for this printout
                for prod in prods['printouts'][printout]:
                    # Append the parsed JSON value to the list
                    self.content[the_name].append(json.loads(prod))

        # If we want to retrieve all results and the query has more than the default limit of 50 results
        if get_all and self.json.get('query-continue-offset') is not None:
            # Sleep 1s to limit hits to API
            sleep(1)
            # Make another ASK query to retrieve the remaining results, using the provided offset
            self.ask(conditions=conditions, printouts=printouts, offset=self.json.get('query-continue-offset'))
            # Process the results of this additional query
            self._get_ask_content(conditions, printouts, get_all)

    # Helper function to format a production JSON query for a specific item or category
    # item can be 'Category:Items' or 'Cake' for example or None for all Production JSON
    # All is whether to get all items (aka continue past limit of 50 items per query)
    # Note: All=True may result in many queries
    def ask_production(self, item: str=None, get_all: bool=False):
        """
        Makes a query to the MediaWiki API to retrieve production data for a given item or category of items.
        
        :param item: The name of the item or category to retrieve production data for. If None, retrieves production data for all items.
        :param get_all: If True, retrieves production data for all items in the given category or all items if item is None. Otherwise, only retrieves production data for the first 50 items.
        :return: None
        """
        if item is None:
            conditions = ['Production JSON::+']
        else:
            conditions = [item, 'Production JSON::+']

        printouts = ['Production JSON']
        self.content = {}

        self.ask(conditions=conditions, printouts=printouts)
        self._get_ask_content(conditions, printouts, get_all)


    def ask_exchange(self, item: str=None, get_all: bool=False):
        """
        This method retrieves exchange data for the specified item or all items.
        The retrieved data is stored in the `self.content` attribute as a dictionary with the keys being the item name and the value being a list of dictionaries representing the exchange data for that item.
        The data can be further accessed by iterating over `self.content.items()` and accessing the data with `item[1]`.

        :param item: (optional) The name of the item to retrieve exchange data for.
        :type item: str
        :param get_all: (optional) A boolean indicating whether to retrieve data for all items (True) or just the first 50 items (False).
        :type get_all: bool
        :return: None
        """
        if item is None:
            conditions = ['Exchange JSON::+']
        else:
            conditions = ['Exchange:' + item, 'Exchange JSON::+']

        printouts = ['Exchange JSON']
        self.content = {}

        self.ask(conditions=conditions, printouts=printouts)
        self._get_ask_content(conditions, printouts, get_all)


    def browse(self, result_format: str = 'json', format_version: str = 'latest', **kwargs) -> None:
        """
        Use the SMWbrowse API endpoint to browse Semantic MediaWiki data.

        :param result_format: The format to return the result in. Defaults to 'json'.
        :param format_version: The version of the format to use. Defaults to 'latest'.
        :param ``**kwargs``: Additional keyword arguments to pass to the API endpoint.
        :return: None
        """
        # Add required kwargs for this endpoint
        kwargs['action'] = 'smwbrowse'
        kwargs['format'] = result_format
        kwargs['formatversion'] = format_version

        # Update the class and parse the json
        self.update(self.base_url, **kwargs)
        self.json = self.response.json()

    # Helper to sub out built-in property names to readable versions
    def _clean_properties(self):
        """
        Clean the property keys in the `content` attribute by renaming them to more human-readable names.
        """
        property_map = {
            "_INST": "Category",
            "_MDAT": "Modification Date",
            "_SKEY": "Name",
            "_SOBJ": "Subobject"
        }
        for old, new in property_map.items():
            if old in self.content:
                self.content[new] = self.content.pop(old)

    def _dirty_properties(self):
        """
        Revert the property keys in the `content` attribute to their original names.
        """
        property_map = {
            "Category": "_INST",
            "Modification Date": "_MDAT",
            "Name": "_SKEY",
            "Subobject": "_SOBJ"
        }
        for old, new in property_map.items():
            if old in self.content:
                self.content[new] = self.content.pop(old)

    def browse_properties(self, item: str):
        """
        Retrieve property values for a given subject.
        
        :param item: The subject to retrieve property values for.
        
        :return: None. Updates the `self.content` attribute with the retrieved properties.
        """
        # Format the subject for the API request
        browse_subject = '{"subject":"' + item.replace(" ", "_") + '","ns":0,"iw":"","subobject":"","options":{"dir":null,"lang":"en-gb","group":null,"printable":null,"offset":null,"including":false,"showInverse":false,"showAll":true,"showGroup":true,"showSort":false,"api":true,"valuelistlimit.out":"30","valuelistlimit.in":"20"}}'
        self.content = {}
        
        # Make the API request and update the `self.json` attribute
        self.browse(browse='subject', params=browse_subject)
        
        # Iterate through the retrieved data items and format them for the `self.content` attribute
        for prop in self.json['query']['data']:
            if len(prop['dataitem']) == 1:
                # If there is only one data item, store it in a single string
                temp_property = prop['dataitem'][0]['item'].replace("#6##", "").replace("#14##", "").replace("#0##", "")
                
                # If the string appears to be in JSON format, parse it to a dictionary
                if "{" in temp_property:
                    temp_property = eval(temp_property)
            else:
                # If there are multiple data items, store them in a list
                temp_property = []
                for item in prop['dataitem']:
                    temp_property.append(item['item'].replace("#6##", "").replace("#14##", "").replace("#0##", ""))
                    
                    # If the string appears to be in JSON format, parse it to a dictionary
                    if "{" in temp_property:
                        temp_property = eval(temp_property)
                        
            # Add the property and its value to the `self.content`
            self.content[prop['property']] = temp_property
