API Endpoints
=============

Real-Time API
---------------

This is the parent class for all queries to the Real Time API for OSRS. It is recommended to use one of the child classes documented below for standard usage.

For full documentation of the Real Time API routes and options, see the `Real-Time documentation <https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices>`_.

.. autoclass:: rswiki_wrapper.osrs.RealTimeQuery

Route: Latest
`````````````
.. autoclass:: rswiki_wrapper.osrs.Latest

Route: Mapping
``````````````
.. autoclass:: rswiki_wrapper.osrs.Mapping

Route: Avg Price
````````````````
.. autoclass:: rswiki_wrapper.osrs.AvgPrice

Route: Time-Series
``````````````````
.. autoclass:: rswiki_wrapper.osrs.TimeSeries

Weird Gloop API
---------------

This is the parent class for all queries to the Weird Gloop API for Exchange and Runescape information. It is recommended to use one of the child classes documented below for standard usage.

For full documentation of the Weird Gloop API routes and endpoints as well as query testing, see the `Weird Gloop documentation <https://api.weirdgloop.org/#/>`_.

.. autoclass:: rswiki_wrapper.wiki.WeirdGloop

Route: Exchange
```````````````
.. autoclass:: rswiki_wrapper.wiki.Exchange

Route: Runescape
````````````````
.. autoclass:: rswiki_wrapper.wiki.Runescape
   :private-members: _check_kwargs

Media Wiki API
---------------

This is the class for all queries to the Media Wiki API for all information in the RSWiki not covered by Real-Time and Weird Gloop APIs. There are a handful of helpful methods in this Class to assist with common queries.

For documentation of the Media Wiki API routes and endpoints, see the `Media Wiki documentation <https://runescape.wiki/api.php>`_.

.. autoclass:: rswiki_wrapper.wiki.MediaWiki
   :members:

WikiQuery
---------

This is the parent class for all queries to the various endpoints.

.. autoclass:: rswiki_wrapper.wiki.WikiQuery
   :members:
