# rswiki_wrapper/wiki.py
# Contains generic functions for RS Wiki API calls

import requests
import json
from time import sleep


class WikiQuery(object):
    """
    A class for querying the RS Wiki API. If no URL is provided, the constructor returns a WikiQuery object with a
    None type ``response`` object. The ``response`` can then be created using ``MediaWiki.update()`` or
    specific Child-class methods.

    Args:
        url (str, optional): The URL of the API endpoint to query.
        user_agent (str, optional): The user agent string to use for the request. Default is
            ``'RS Wiki API Python Wrapper - Default'``.
        ``**kwargs``: Additional parameters to include in the query. See child classes for required kwargs.

    Attributes:
        headers (dict): The headers sent with the request object. Created from ``user_agent``
        response (:obj:`Response`): The response object provided by the ``requests`` library.
    """

    def __init__(self, url: str = None, user_agent: str = 'RS Wiki API Python Wrapper - Default', **kwargs):
        """
        Constructor method
        """
        super().__init__()

        if user_agent == 'RS Wiki API Python Wrapper - Default':
            print("WARNING: You are using the default user_agent. Please configure the query with the parameter "
                  "user_agent='{Project Name} - {Contact Information}'")

        self.headers = {
            'User-Agent': user_agent
        }

        if url is not None:
            self.response = requests.get(url, headers=self.headers, params=kwargs)

    def update(self, url, **kwargs):
        """
        Refresh the query with a new URL and additional parameters. Updates the ``self.response`` attribute.

        Args:
            url (str): The URL of the API endpoint to query.
            ``**kwargs``: Additional parameters to include in the query. See child classes for required kwargs.
        """
        self.response = requests.get(url, headers=self.headers, params=kwargs)


class WeirdGloop(WikiQuery):
    """
    This class extends the ``WikiQuery`` class to make queries to the Weird Gloop API.
    For general usage, it is recommended to use the specific Exchange or Runescape child classes.

    Args:
        route (str): The route of the Weird Gloop API to query.
        game (str): The game to query in the Weird Gloop API.
        endpoint (str): The endpoint of the Weird Gloop API to query.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.
        ``**kwargs``: Additional keyword arguments to pass, depending on the specific query

    Attributes:
        headers (dict): The headers sent with the request object. Created from ``user_agent``
        response (:obj:`Response`): The response object provided by the ``requests`` library.
    """

    def __init__(self, route: str, game:str, endpoint: str, user_agent: str, **kwargs):
        # https://api.weirdgloop.org/#/ for full documentation

        base_url = 'https://api.weirdgloop.org/' + route + game + '/' + endpoint

        super().__init__(base_url, user_agent, **kwargs)


class Exchange(WeirdGloop):
    """
    This class extends the ``WeirdGloop`` class to make queries to the exchange history endpoint of the Weird Gloop API.

    Args:
        game (str): The game to query in the Weird Gloop API. Valid options are ``'rs'``, ``'rs-fsw-2022'``,
            ``'osrs'``, ``'osrs-fsw-2022'``.
        endpoint (str): The endpoint of the Weird Gloop API to query. Valid options are ``'latest'``, ``'all'``,
            ``'last90d'``, and ``'sample'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Keyword Args:
        id (str): The itemID or a trade index like *GE Common Trade Index*
        name (str): The exact Grand Exchange item name.

    Note:
        * Only ``id`` or ``name`` can be provided as kwargs, not both.

        * If using the ``latest`` endpoint, multiple items can be specified using pipes "|" like ``id='2|6'``

        * If using ``all``, ``last90d``, and ``sample`` endpoints, multiple item ID or names cannot be provided.

    Attributes:
        headers (dict): The headers sent with the request object. Created from ``user_agent``
        response (:obj:`Response`): The response object provided by the ``requests`` library.
        json (dict): The raw JSON formatted response from the API
        content (dict): The parsed content of the request. Formatted as follows. ``item`` is either the item name or
            item ID that you provided to the request.
            Sample content format::

                {
                item (str):
                    [
                        {
                            'id' : item_id (str),
                            'timestamp': timestamp (str),
                            'price': price (int),
                            'volume': volume (int),
                        },
                        # A new dict for each timestamp
                    ]
                }


    Examples:
        Example usage of ``latest`` endpoint::

            >>> query = Exchange('osrs', 'latest', user_agent='My Project - me@example.com', id='2|6')
            >>> query.content['2'][0]['id']
            '2'

        Example usage of ``all`` endpoint::

            >>> query = Exchange('osrs', 'all', user_agent='My Project - me@example.com', name='Coal')
            >>> query.content['Coal'][0]['id']
            '453'
    """
    def __init__(self, game, endpoint, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # https://api.weirdgloop.org/#/ for full documentation

        super().__init__('exchange/history/', game, endpoint, user_agent, **kwargs)
        self.json = self.response.json()

        self.content = self.json
        if endpoint == 'latest':
            # To standardize the format of content
            self.content = {key: [value] for key, value in self.content.items()}


class Runescape(WeirdGloop):
    """
    This class extends the ``WeirdGloop`` class to make queries to the general endpoints of the Weird Gloop API for
    Runescape information.

    Args:
        endpoint (str): The endpoint of the Weird Gloop API to query. Valid options are ``"vos"``, ``'vos/history'``,
            ``'social'``, ``'social/last'``, ``'tms/current'``, ``'tms/next'``, and ``'tms/search'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Keyword Args:
        lang (str): Required for ``'tms/current'`` and ``'tms/next'`` endpoints. Optional for ``'tms/search'``. Valid
            values are ``'en'``, ``'pt'``, ``'id'`` (item IDs only), and ``'full'`` (all information).
        page (str): Required for ``'vos/history'`` and ``'social'`` endpoints. The page number is formatted as a string.
        start (str): Required for ``'tms/search'``. Date string or ``'today'``.
        id (str): Optional for ``'tms/search'``. The item ID to search for.
        name (str): Optional for ``'tms/search'``. The item name to search for.
        number (str): Optional for ``'tms/search'``. The number of results to return
        end (str): Optional for ``'tms/search'``. Date string or ``'today'``.

    Note:
        For ``'tms/search'`` endpoint, either ``'id'`` or ``'name'`` is required (but not both) and either ``'end'``
        or ``'number'`` is required (but not both).

    Attributes:
        headers (dict): The headers sent with the request object. Created from ``user_agent``
        response (:obj:`Response`): The response object provided by the ``requests`` library.
        json (dict): The raw JSON formatted response from the API
        content: The parsed content of the request. Generally either a list of multiple results or a single
            result in ``dict`` format, depending on the endpoint used.

    Examples:
        Example usage of ``tms/search`` endpoint to search for instances where item ID 42274 was active::

            >>> query = Runescape('tms/search', user_agent='My Project - me@example.com', lang='full', start='2022-01-01', end='2022-01-07', id='42274')
            >>> query.content[0]['items'][0]
            {'id': '42274', 'en': 'Uncharted island map (Deep Sea Fishing)', 'pt': 'Mapa da ilha inexplorada (Pesca em Alto Mar)'}

        Example usage of ``social`` endpoint::

            >>> query = Runescape('social', user_agent='My Project - me@example.com', page='1')
            >>> query.content[0].keys()
            dict_keys(['id', 'url', 'title', 'excerpt', 'author', 'curator', 'source', 'image', 'icon', 'expiryDate', 'datePublished', 'dateAdded'])
    """

    def __init__(self, endpoint, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        # Used for the general endpoints for Runescape information

        if endpoint == 'tms/search':
            if not self._check_kwargs(**kwargs):
                print('Keyword Arguments did not pass check, see documentation for allowable args')
                self.json = None
                self.content = None
                return

        super().__init__('runescape/', game="", endpoint=endpoint, user_agent=user_agent, **kwargs)

        self.json = self.response.json()

        # tms data can be a list or dict, depending on the kwargs used in lang
        if isinstance(self.json, list):
            self.content = self.json
        elif 'data' in self.json.keys():
            self.content = self.json['data']
        else:
            self.content = self.json

    @staticmethod
    def _check_kwargs(**kwargs):
        """
        This method checks the keyword arguments passed to the ``Runescape`` class for the ``'tms/search'`` endpoint to
        ensure that they are valid and do not conflict with each other.

        Args:
            ``**kwargs``: The keyword arguments to check.

        Returns:
            bool: Whether the keyword arguments are valid and do not conflict.
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
    This class is used to access the MediaWiki API for pulling information from the Wiki. An empty instance can be
    created for using the various helper methods built into this class, or the query can be made directly from
    this interface using the appropriate kwargs.

    Args:
        game (str, optional): The game RSWiki should refer to. Valid options are ``'osrs'`` or ``'rs3'``.
        user_agent (str): The user agent string to use in the query. Default is
            ``'RS Wiki API Python Wrapper - Default'``.

    Attributes:
        headers (dict): The headers sent with the request object. Created from ``user_agent``
        response (:obj:`Response`): The response object provided by the ``requests`` library.
        json (dict): The raw JSON formatted response from the API
        content: The parsed content of the request. If created via the constructor method, it will be identical
            to the json content. If created via the built-in methods, it will be formatted to contain the requested
            data with minimal data wrangling required.
    """
    def __init__(self, game, user_agent='RS Wiki API Python Wrapper - Default', **kwargs):
        assert game in ['osrs', 'rs3'], 'Invalid game; choose osrs or rs3'

        if game == 'osrs':
            self.base_url = 'https://oldschool.runescape.wiki/api.php'
        else:
            self.base_url = 'https://runescape.wiki/api.php'

        if kwargs:
            super().__init__(self.base_url, user_agent=user_agent, **kwargs)
            self.json = self.response.json()
            self.content = self.json
        else:
            super().__init__(user_agent=user_agent)
            self.json = None
            self.content = None

    # Use the ASK route
    def ask(self, result_format: str = 'json', conditions: list[str] = None, printouts: list[str] = None,
            offset: str = None, **kwargs):
        """
        This method sends an ASK query to the MediaWiki API using the specified ``conditions`` and ``printouts``
        parameters, and optional ``offset`` parameter. The ``result_format`` specifies the format in which the
        response is returned.

        Args:
            result_format (str, optional): The format in which the response is returned. Default is ``'json'``.
            conditions (list[str]): The conditions to match in the ASK query.
            printouts (list[str]): The printouts (results) to provide from the ASK query.
            offset (str, optional): The offset in results. Typical ASK queries provide 50 results, so ``offset='50'``
                will provide results 51-100 (or lower if there are less than 100 results).

        Note:
            This route only updates the ``.json`` attribute due to the variety of possible printouts. To get the
            ``.content``, first try the ``.get_ask_content()`` method which parses the conditions and printouts.

        Examples:
            Example usage of the ASK query to find production JSON data for all items::

                >>> query = MediaWiki('osrs', user_agent='My Project - me@example.com')
                >>> query.ask(conditions=['Category:Items', 'Production JSON::+'], printouts=['Production JSON'])
                >>> query.json['query']['results']['Abyssal bludgeon']['printouts']['Production JSON'][0]
                '{"ticks":"","materials":[{"name":"Bludgeon axon","quantity":"1"},{"name":"Bludgeon claw","quantity":"1"},
                {"name":"Bludgeon spine","quantity":"1"}],"facilities":"The Overseer","skills":[],"members":"Yes","output":
                {"cost":11131623,"quantity":"1","name":"Abyssal bludgeon","image":
                "[[File:Abyssal bludgeon.png|link=Abyssal bludgeon]]"}}'

        Hint:
            If trying to access the Production JSON or Exchange JSON information, use the included ``ask_production``
            and ``ask_exchange`` methods below, which make the result navigation much simpler.
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

    def get_ask_content(self, conditions: list[str], printouts: list[str], get_all: bool = False) -> None:
        """
        A helper function to retrieve content from an ASK query in the MediaWiki API.

        Args:
            conditions (list[str]): The conditions to match in the ASK query.
            printouts (list[str]): The printouts (results) to provide from the ASK query.
            get_all (bool, optional): Whether to retrieve all results from the ASK query recursively.

        Warning:
            Using get_all will recursively retrieve all results of the query. For some queries such as getting all
            production JSON information for all items, this results in a long wait to retrieve the results. This is
            because the wrapper has a limit of 1 query/second when recursively following the results to reduce load
            on the API.
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
            self.get_ask_content(conditions, printouts, get_all)

    # Helper function to format a production JSON query for a specific item or category
    # item can be 'Category:Items' or 'Cake' for example or None for all Production JSON
    # All is whether to get all items (aka continue past limit of 50 items per query)
    # Note: All=True may result in many queries
    def ask_production(self, item: str = None, get_all: bool = False):
        """
        Makes a query to the MediaWiki API to retrieve production data for a given item or category of items.

        Args:
            item (str, optional): The item name to search Production Information. Can also be a Category
                ``'Category:X'``. If no name is provided, all items with a valid Production JSON will be returned.
            get_all (bool, optional): To recursively search for all matching items, or only provide the first page of
                results, which by RSWiki convention is 50 results.

        Returns:
            None. Updates the ``.content`` attribute as follows. ``item`` is the name of the item provided in args or
            all items matching the category selected.
            Resulting content format::

                {
                    item (str):
                        [
                            {
                                'ticks' : ticks (str),
                                'materials': [
                                    {
                                        'name': material_name (str),
                                        'quantity': material_quantity (str)
                                    }
                                    # New dict for each material
                                ],
                                'facilities': facilities (str),
                                'skills': [
                                    {
                                        'experience': experience_per (str),
                                        'level': level_required (str),
                                        'name': level_name (str),
                                        'boostable': yes_no (str)
                                    }
                                    # New dict for each material
                                ],
                                'members': yes_no (str),
                                'output': {
                                    'cost': cost (int)
                                    'quantity': quantity (str),
                                    'name': name (str),
                                    'image': img_link (str)
                                }
                            },
                            # A new dict for each production method
                        ]
                    # A new key for each item name
                }

        Example:
            Example of getting Production JSON information for Cake::

                >>> query = MediaWiki('osrs', user_agent='My Project - me@example.com')
                >>> query.ask_production('Cake')
                >>> query.content['Cake'][0]['skills']
                [{'experience': '180', 'level': '40', 'name': 'Cooking', 'boostable': 'Yes'}]

        Warning:
            Using get_all will recursively retrieve all results of the query. For some queries such as getting all
            production JSON information for all items, this results in a long wait to retrieve the results. This is
            because the wrapper has a limit of 1 query/second when recursively following the results to reduce load
            on the API.
        """
        if item is None:
            conditions = ['Production JSON::+']
        else:
            conditions = [item, 'Production JSON::+']

        printouts = ['Production JSON']
        self.content = {}

        self.ask(conditions=conditions, printouts=printouts)
        self.get_ask_content(conditions, printouts, get_all)

    def ask_exchange(self, item: str = None, get_all: bool = False):
        """
        This method retrieves exchange data for the specified item or all items.

        Args:
            item (str, optional): The item name to search Exchange Information. If no name is provided,
                all items with a valid Exchange JSON will be returned.
            get_all (bool, optional): To recursively search for all matching items, or only provide the first page of
                results, which by RSWiki convention is 50 results.

        Warning:
            Unlike the ask_production method, a category can not be specified. This is because the Exchange JSON is
            actually formatted as ``[Exchange:Item]]``, and ``[[Exchange:Category:X]]`` is not a valid condition.

        Returns:
            None. Updates the ``.content`` attribute as follows. ``item`` is the name of the item provided in args.
            Resulting content format::

                {
                    'Exchange:Item' (str):
                        [
                            {
                                'historical' : historical_info (bool),
                                'id': ge_item_id (int),
                                'lowalch': low_alch (int),
                                'limit': ge_limit (int),
                                'isalchable': alchable (bool),
                                'value' : ge_value (int),
                                'info': module_page (str),
                                'name': item_name (str),
                                'highalch': high_alch (int),
                            },
                            # A new dict for any other exchange pages with this name
                        ]
                    # A new key for each item name
                }

        Example:
            Example of getting Exchange JSON information for Cake::

                >>> query = MediaWiki('osrs', user_agent='My Project - me@example.com')
                >>> query.ask_exchange('Cake')
                >>> query.content['Exchange:Cake'][0]['info']
                'Module:Exchange/Cake'

        Warning:
            Using get_all will recursively retrieve all results of the query. Retrieving all Exchange pages recursively
            will result in a long wait to retrieve the results. This is because the wrapper has a limit of
            1 query/second when recursively following the results to reduce load on the API.
        """
        if item is None:
            conditions = ['Exchange JSON::+']
        else:
            conditions = ['Exchange:' + item, 'Exchange JSON::+']

        printouts = ['Exchange JSON']
        self.content = {}

        self.ask(conditions=conditions, printouts=printouts)
        self.get_ask_content(conditions, printouts, get_all)

    def browse(self, result_format: str = 'json', format_version: str = 'latest', **kwargs) -> None:
        """
        Use the SMWbrowse API endpoint to browse Semantic MediaWiki data. This helper assists with the ``smwbrowse``
        action.

        Args:
            result_format (str, optional): The format in which the response is returned. Default is ```json'``.
            format_version (str, optional): The version of the chosen format to use. Default is ``'latest'``
            ``**kwargs``: Additional keyword arguments to pass as params to the query.

        Note:
            This route only updates the ``.json`` attribute due to the variety of possible printouts. To get the
            ``.content``, custom parsing is required.

        Hint:
            If trying to browse for properties of pages ``(Special:Browse)`` the ``browse_properties()`` method will
            simplify the parsing of json content.
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

        Args:
            item (str): The page name to search properties for.

        Returns:
            None. Creates the ``.content`` attribute as a dict with ``keys`` of each property and ``values`` of the
            value of each property.

        Example:
            Example of getting all property information for Cake::

                >>> query = MediaWiki('osrs', user_agent='My Project - me@example.com')
                >>> query.browse_properties('Cake')
                >>> query.content.keys()
                dict_keys(['All_Image', 'All_Is_members_only', 'All_Item_ID', 'All_Weight', 'Cooking_experience',
                'Cooking_level', 'Default_version', 'Is_boostable', 'Is_members_only', 'Production_JSON', 'Store_price_delta',
                'Uses_facility', 'Uses_material', 'Uses_skill', 'Version_count', '_INST', '_MDAT', '_SKEY', '_SOBJ'])

                # Cleaning the `_X` properties to human-readable values.
                >>> query._clean_properties()
                dict_keys(['All_Image', 'All_Is_members_only', 'All_Item_ID', 'All_Weight', 'Cooking_experience',
                'Cooking_level', 'Default_version', 'Is_boostable', 'Is_members_only', 'Production_JSON', 'Store_price_delta',
                'Uses_facility', 'Uses_material', 'Uses_skill', 'Version_count', 'Category', 'Modification Date', 'Name', 'Subobject'])
        """
        # Format the subject for the API request
        browse_subject = '{"subject":"' + item.replace(" ", "_") + '","ns":0,"iw":"","subobject":"","options":{' \
                                                                   '"dir":null,"lang":"en-gb","group":null,' \
                                                                   '"printable":null,"offset":null,"including":false,' \
                                                                   '"showInverse":false,"showAll":true,' \
                                                                   '"showGroup":true,"showSort":false,"api":true,' \
                                                                   '"valuelistlimit.out":"30",' \
                                                                   '"valuelistlimit.in":"20"}} '
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
