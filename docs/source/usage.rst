Usage
===============

This section will teach you the API endpoints available in this wrapper and how to best use them in your own projects

Acceptable Use Policy
---------------------
To interface properly with the RuneScape Wiki API, first review their `acceptable use policy <https://runescape.wiki/w/Help:APIs#Acceptable_use_policy>`_.

To assist in the user setup, each child class accepts a ``user_agent`` parameter. Each user should identify a method of contact which will be submitted in each request header. This allows the RuneScape Wiki staff to contact you and correct any misbehaving queries. I recommend using the format ``user_agent='{Project Name} - {Contact}'``. The library contains a generic user agent which identifies you as using this wrapper and will warn you to use a custom user agent.

Basic Usage
-----------

The best practice for using this wrapper is to import the child Class for your use-case, for example to get the Real-Time OSRS Prices `/latest` data:

.. code-block:: python
   :linenos:

   from rswiki_wrapper import Latest
   latest_prices = Latest()


For a detailed description of the options with sample usage for each API Endpoint, see :doc:`endpoints`

