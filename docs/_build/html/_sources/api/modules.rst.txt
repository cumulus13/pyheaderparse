=============
API Reference
=============

This section provides complete API documentation for all public classes and functions.

Module Overview
---------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Module
     - Description
   * - ``parser_header``
     - Main package with public exports
   * - ``parser_header.parser``
     - Core parser classes (HeaderParser, CookieParser, HeaderValue)
   * - ``parser_header.exceptions``
     - Custom exception classes
   * - ``parser_header.cli``
     - Command-line interface

Quick Import Reference
----------------------

.. code-block:: python

   # Main classes
   from parser_header import HeaderParser, CookieParser, HeaderValue

   # Exceptions
   from parser_header import ParserError, InvalidHeaderError, InvalidCookieError

   # Or import everything
   from parser_header import *

Class Summary
-------------

HeaderParser
~~~~~~~~~~~~

The main class for parsing and manipulating HTTP headers.

.. code-block:: python

   from parser_header import HeaderParser

   # Create
   parser = HeaderParser(raw_data)
   parser = HeaderParser(content_type='json', user_agent='MyApp')
   parser = HeaderParser.from_dict({'Content-Type': 'json'})
   parser = HeaderParser.from_kwargs(content_type='json')

   # Access
   parser.get('content-type')
   parser['content-type']
   parser.content_type

   # Modify
   parser.set('Header', 'value')
   parser.set(header='value')
   parser.remove('header')
   parser.clear()

   # Export
   parser.to_dict()
   parser.to_raw()
   parser.to_requests_headers()

See :doc:`header_parser` for complete API.

CookieParser
~~~~~~~~~~~~

Dedicated class for parsing and manipulating cookies.

.. code-block:: python

   from parser_header import CookieParser

   # Create
   cookies = CookieParser(raw_data)
   cookies = CookieParser(session='abc', user='john')
   cookies = CookieParser.from_dict({'session': 'abc'})

   # Access
   cookies.get('session')
   cookies['session']

   # Modify
   cookies.set('name', 'value')
   cookies.set(name='value')
   cookies.remove('name')
   cookies.clear()

   # Export
   cookies.to_cookie_header()  # "session=abc; user=john"
   cookies.to_dict()           # {'session': 'abc', 'user': 'john'}

See :doc:`cookie_parser` for complete API.

HeaderValue
~~~~~~~~~~~

Dataclass for headers with parameters (Content-Type, Content-Disposition).

.. code-block:: python

   from parser_header import HeaderValue

   # Usually created automatically when parsing
   parser = HeaderParser()
   parser.set('content-type', 'text/html; charset=utf-8')

   hv = parser.get('content-type')
   print(hv.value)   # 'text/html'
   print(hv.params)  # {'charset': 'utf-8'}

Exceptions
~~~~~~~~~~

.. code-block:: python

   from parser_header import ParserError, InvalidHeaderError, InvalidCookieError
   from parser_header.exceptions import EncodingError

   try:
       parser = HeaderParser(invalid_data)
   except ParserError as e:
       print(f"Parse error: {e}")

See :doc:`exceptions` for complete API.

Contents
--------

.. toctree::
   :maxdepth: 2

   header_parser
   cookie_parser
   exceptions