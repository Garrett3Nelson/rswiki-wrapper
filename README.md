# RSWiki-Wrapper

RSWiki-Wrapper is an open-source Python library wrapping functionality of the RuneScape Wiki API. Its goal is to support all RuneScape Wiki API endpoints for both OldSchool RuneScape and RuneScape (aka RS3).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

To begin developing and testing this wrapper, set up a python environment with the prerequisites noted in Requirements.txt. No other environment setup is currently required.

### Configuration

To interface properly with the RuneScape Wiki API, first review their [acceptable use policy](https://runescape.wiki/w/Help:APIs#Acceptable_use_policy). To assist, I have created a configuration file.

Each user should identify a method of contact which is submitted in the USER_AGENT. This allows the RuneScape Wiki staff to contact you and correct any misbehaving queries. If using for a full-scale project, renaming the PROJECT_NAME variable will identify your use-case to the staff.

Update the following sections in `config.py`

```python
# Insert a method for wiki staff to identify you ('Discord: @Username#1234' for example)
CONTACT_NAME = ''

# Identify your project name
PROJECT_NAME = 'RS Wiki API Python Wrapper'
```

## Usage

The project is written such that it exposes the full API responses for user interaction under `WikiQuery.response`. Users can review all aspects of the request response under this property. Each class also exposes two helpful properties:
* `WikiQuery.json` is a python dictionary format of the API response
* `WikiQuery.content` is the "useful" data returned by the query, typically formatted as a python dictionary or list of dictionaries, where applicable.

### API Endpoints

For information on the various acceptable routes, queries, and optional arguments see the following documentation:
* [MediaWiki API](https://runescape.wiki/api.php) for all requests related to RuneScape wiki. This endpoint is valid for both OldSchool RuneScape and RuneScape.
* [WeirdGloop API](https://api.weirdgloop.org/#/) for requests to use the WeirdGloop API, which provides data for the RuneScape Grand Exchange and RuneScape Information. RuneScape Grand Exchange data is valid for both OldSchool RuneScape and RuneScape. RuneScape information is valid only for RuneScape (RS3).
* [Real-Time API](https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices) for access to real-time Grand Exchange data. This endpoint is valid only for OldSchool RuneScape.

### Sample Usage

All requests are initiated using a sub-class dedicated to the specific route. For example, using the Exchange sub-class to obtain the day's Grand Exchange information from  WeirdGloop:

The URL for WeirdGloop requests follows the format `https://api.weirdgloop.org/exchange/history/{game}/{filter}?{args}`

Setting up an Exchange class follows the same format, using `endpoint` instead of the existing python `filter` as an argument `Exchange(game, endpoint, **kwargs)`:

```python
from wikiwrapper import Exchange

exchange = Exchange('osrs', 'latest', id="2|6")
```

Can be used as follows:

```python
>>> exchange.content
OrderedDict([('2', OrderedDict([('id', '2'), ('timestamp', '2022-11-18T06:13:09.000Z'), ('price', 162), ('volume', 51173617)])), ('6', OrderedDict([('id', '6'), ('timestamp', '2022-11-18T06:13:09.000Z'), ('price', 185765), ('volume', 417)]))])
>>> exchange.content['2']['price']
162
```

For a sample script using the Real-Time API, see `sample.py`

## Tests

Testing for this project is performed using PyTest. All tests are written in `/tests` and should confirm the `.content` is formatted correctly, confirm the response data matches the expected value (if possible) and confirm the response keys match the expected output format.

Tests should be written with the following template in mind:
```python
@fixture
def exchange_keys():
    # Keys that are returned by a successful query
    return ['id', 'timestamp', 'price', 'volume']


def test_exchange_latest(exchange_keys):
    """Tests an API call to get the latest Grand Exchange price information"""

    query_instance = Exchange('rs', 'latest', id='2|6')
    response = query_instance.content

    assert isinstance(response, OrderedDict)
    assert list(response.keys())[0] == '2', "The ID should be in the response"
    assert set(exchange_keys).issubset(response['2'].keys()), "All keys should be in the response"
```

## Roadmap

The goal of this project is to extend functionality to all distinct APIs and all available routes. There are still many TODO items throughout the source code which are a reminder of verifications for edge cases that I have identified but have not yet resolved.

### Routes Under Development
* All MediaWiki API routes. The placeholder class is `MediaWiki` 
* The highest priority MediaWiki route is `ask` which has important `query` arguments which provide detailed game information

### Working Routes
* All Real-Time API routes
* WeirdGloop Exchange information
* WeirdGloop Runescape information except Traveling Merchant Search

## Contributing

Pull requests are welcome. As a novice to open source projects, I welcome all suggestions for improvements. For major changes, please open an issue to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
