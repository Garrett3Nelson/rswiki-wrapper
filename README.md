# RSWiki-Wrapper

RSWiki-Wrapper is an open-source Python library wrapping functionality of the RuneScape Wiki API. Its goal is to support all RuneScape Wiki API endpoints for both OldSchool RuneScape and RuneScape (aka RS3).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

To begin using the wrapper, you can install with pip 

`pip install rswiki-wrapper`

The package is imported with `import rswiki_wrapper` or `from rswiki_wrapper import Exchange`.

To begin developing and testing this wrapper, set up a python environment with the prerequisites noted in [requirements.txt](requirements.txt).

### Acceptable Use Policy

To interface properly with the RuneScape Wiki API, first review their [acceptable use policy](https://runescape.wiki/w/Help:APIs#Acceptable_use_policy).

To assist in the user setup, each child class accepts a `user_agent` parameter. Each user should identify a method of contact which will be submitted in each request header. This allows the RuneScape Wiki staff to contact you and correct any misbehaving queries. I recommend using the format `user_agent='{Project Name} - {Contact}'`. The library contains a generic user agent which identifies you as using this wrapper and will warn you to use a custom user agent.

## Usage

The project is written such that it exposes the full API responses for user interaction under `WikiQuery.response`. Users can review all aspects of the request response under this property. Each class also exposes two helpful properties:
* `WikiQuery.json` is a python dictionary format of the API response
* `WikiQuery.content` is the "useful" data returned by the query, typically formatted as a python dictionary or list of dictionaries, where applicable.

### API Endpoints

For information on the various acceptable routes, queries, and optional arguments see the following documentation:
* [MediaWiki API](https://runescape.wiki/api.php) for all requests related to RuneScape wiki. This endpoint is valid for both OldSchool RuneScape and RuneScape.
* [Weird Gloop API](https://api.weirdgloop.org/#/) for requests to use the WeirdGloop API, which provides data for the RuneScape Grand Exchange and RuneScape Information. 
* [Real-Time API](https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices) for access to real-time Grand Exchange data. This endpoint is valid only for OldSchool RuneScape.

### MediaWiki Usage

The MediaWiki API provides access to all information hosted on the RS Wiki. There is a long list of `actions` in the API documentation above.

All MediaWiki requests take four inputs:
* Mandatory Parameter`game` which is 'osrs' or 'rs3' 
* Optional Parameter `user_agent` per the acceptable use policy
* kwarg `action` per the list from API Documentation
* Any kwargs which go with your `action`

You can test queries in the [API Sandbox](https://runescape.wiki/w/Special:ApiSandbox) to determine the output and assist in parsing the JSON returned. `.json` and `.content` are identical for MediaWiki requests although both are exposed to allow future expansion of known common queries.

#### Media Wiki Helper Functions
There are several helper functions built into the wrapper, with more to come. If using the helper functions, initialize a blank MediaWiki instance with `query = MediaWiki({game})` and then call the helper function with `query.function()`.

* `ask()` is a shortcut to the Semantic MediaWiki Ask API. The `query` must still be entered as a kwarg (`query='x'`)
* `ask_production()` is a shortcut to query Production JSON information for any item(s) or category.
  * Input `item={item}` where the format matches the Ask API `[[{Item}]][[Production JSON::+]]|?Production JSON`
  * Output `.content` outputs a dictionary where item names are the keys and production information is the values. As always, the `.response` and `.json` attributes can provide full details of the query.

### Weird Gloop Usage

Weird Gloop provides two main routes: `exchange` for Grand Exchange daily information and `runescape` for Runescape (RS3) information. The classes to access these routes are `Exchange` and `Runescape`.

The URL for Weird Gloop requests follows the format `https://api.weirdgloop.org/exchange/history/{game}/{filter}?{args}`

Setting up an Exchange class follows the same format, using `endpoint` instead of `filter` as an argument `Exchange(game, endpoint, user_agent, **kwargs)`:

```python
from rswiki_wrapper import Exchange

exchange = Exchange('osrs', 'latest', user_agent='Price Scraper - Garrett3Nelson', id="2|6")

# Usage of this information:
>>> exchange.content
OrderedDict([('2', OrderedDict([('id', '2'), ('timestamp', '2022-11-18T06:13:09.000Z'), ('price', 162), ('volume', 51173617)])), ('6', OrderedDict([('id', '6'), ('timestamp', '2022-11-18T06:13:09.000Z'), ('price', 185765), ('volume', 417)]))])
>>> exchange.content['2']['price']
162
```

### Real-Time Usage

The Real-Time API uses Runelite information to provide real time pricing and volume for OSRS Grand Exchange items. For a sample script using the Real-Time API, see `sample.py`

The child class routes available for Real-Time are:
* `Latest` to access the latest information for all items (or specify an ID)
* `Mapping` for a list of all items and relevant information
* `AvgPrice` to access either the `5m` or `1hr` routes
* `TimeSeries` for (up to) 365 points showing the price and volume for a specific itemID and timestep

## Tests

Testing for this project is performed using PyTest. All tests are written in `/tests` and should confirm the `.content` is formatted correctly, confirm the response data matches the expected value (if possible) and confirm the response keys match the expected output format.

## Roadmap

The goal of this project is to extend functionality to all distinct APIs and all available routes. All routes are currently working. There are still many TODO items throughout the source code which are a reminder of verifications for edge cases that I have identified but have not yet resolved.

### Under Development
* Implement specific common queries in MediaWiki API

## Contributing

Pull requests are welcome. As a novice, I welcome all suggestions for improvements. For major changes, please open an issue to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
