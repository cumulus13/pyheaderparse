.. pyheaderparse documentation master file

=====================================
pyheaderparse Documentation
=====================================

.. image:: https://badge.fury.io/py/pyheaderparse.svg
   :target: https://badge.fury.io/py/pyheaderparse
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pyheaderparse.svg
   :target: https://pypi.org/project/pyheaderparse/
   :alt: Python versions

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: License: MIT

.. image:: https://readthedocs.org/projects/pyheaderparse/badge/?version=latest
   :target: https://pyheaderparse.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

**pyheaderparse** is a robust, production-ready HTTP header and cookie parser library for Python.

Features
--------

* **Complete Header Parsing** - Parse all standard HTTP headers including Content-Type, Accept, Cache-Control, and more
* **Cookie Support** - Full cookie parsing with multiple extraction methods
* **Kwargs Support** - Create and modify headers/cookies using keyword arguments
* **Client Hints** - Parse modern ``Sec-CH-UA-*`` headers
* **Type Safety** - Full type hints for IDE support
* **Zero Dependencies** - No external dependencies required
* **CLI Tool** - Command-line interface for quick parsing
* **Method Chaining** - Fluent API for easy manipulation

Quick Installation
------------------

.. code-block:: bash

   pip install pyheaderparse

Quick Example
-------------

.. code-block:: python

   from parser_header import HeaderParser, CookieParser

   # Parse raw headers
   raw = """content-type: application/json
   content-length: 1024
   cookie: session=abc123; user=john
   """
   parser = HeaderParser(raw)
   print(parser.content_type)  # 'application/json'
   print(parser.get_cookies_as_dict())  # {'session': 'abc123', 'user': 'john'}

   # Or create from kwargs
   parser = HeaderParser(content_type='application/json', user_agent='MyApp/1.0')

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation
   quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   usage/header_parser
   usage/cookie_parser
   usage/special_headers
   usage/cli

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/modules
   api/header_parser
   api/cookie_parser
   api/exceptions
   api/api_source

.. toctree::
   :maxdepth: 1
   :caption: Development

   contributing
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
