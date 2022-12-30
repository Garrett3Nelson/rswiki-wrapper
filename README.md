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

For detailed documentation on the various API endpoints exposed and sample usage, see the [project documentation](https://rswiki-wrapper.readthedocs.io/)

### API Endpoints

For information on the various acceptable routes, queries, and optional arguments see the following documentation:
* [MediaWiki API](https://runescape.wiki/api.php) for all requests related to RuneScape wiki. This endpoint is valid for both OldSchool RuneScape and RuneScape.
* [Weird Gloop API](https://api.weirdgloop.org/#/) for requests to use the WeirdGloop API, which provides data for the RuneScape Grand Exchange and RuneScape Information. 
* [Real-Time API](https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices) for access to real-time Grand Exchange data. This endpoint is valid only for OldSchool RuneScape.

## Tests

Testing for this project is performed using PyTest. All tests are written in `/tests` and should confirm the `.content` is formatted correctly, confirm the response data matches the expected value (if possible) and confirm the response keys match the expected output format.

## Contributing

Pull requests are welcome. As a novice, I welcome all suggestions for improvements. For major changes, please open an issue to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
