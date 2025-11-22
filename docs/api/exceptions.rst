==========
Exceptions
==========

.. module:: parser_header.exceptions
   :synopsis: Custom exception classes

Exception Hierarchy
-------------------

.. code-block:: text

   Exception
   └── ParserError
       ├── InvalidHeaderError
       ├── InvalidCookieError
       └── EncodingError

All custom exceptions inherit from ``ParserError``, which inherits from Python's built-in ``Exception``.

Importing Exceptions
--------------------

.. code-block:: python

   # From main package
   from parser_header import ParserError, InvalidHeaderError, InvalidCookieError

   # From exceptions module (includes EncodingError)
   from parser_header.exceptions import (
       ParserError,
       InvalidHeaderError,
       InvalidCookieError,
       EncodingError
   )

Exception Classes
-----------------

ParserError
~~~~~~~~~~~

.. exception:: ParserError

   Base exception for all parser errors.

   This is the parent class for all custom exceptions in pyheaderparse.
   You can catch this to handle any parser-related error.

   **Example:**

   .. code-block:: python

      from parser_header import HeaderParser, ParserError

      try:
          parser = HeaderParser(some_data)
          result = parser.get('header')
      except ParserError as e:
          print(f"Parser error: {e}")

InvalidHeaderError
~~~~~~~~~~~~~~~~~~

.. exception:: InvalidHeaderError

   Raised when header format is invalid.

   This exception is raised when the parser encounters malformed header data
   that cannot be parsed.

   **Example:**

   .. code-block:: python

      from parser_header import HeaderParser, InvalidHeaderError

      try:
          parser = HeaderParser(malformed_data)
      except InvalidHeaderError as e:
          print(f"Invalid header: {e}")

InvalidCookieError
~~~~~~~~~~~~~~~~~~

.. exception:: InvalidCookieError

   Raised when cookie format is invalid.

   This exception is raised when the parser encounters malformed cookie data.

   **Example:**

   .. code-block:: python

      from parser_header import CookieParser, InvalidCookieError

      try:
          cookies = CookieParser(malformed_cookies)
      except InvalidCookieError as e:
          print(f"Invalid cookie: {e}")

EncodingError
~~~~~~~~~~~~~

.. exception:: EncodingError

   Raised when encoding/decoding fails.

   This exception is raised when bytes input cannot be decoded to string
   using UTF-8 or Latin-1 encodings.

   **Example:**

   .. code-block:: python

      from parser_header import HeaderParser
      from parser_header.exceptions import EncodingError

      try:
          # Invalid bytes that can't be decoded
          parser = HeaderParser(b'\xff\xfe\x00\x01invalid')
      except EncodingError as e:
          print(f"Encoding error: {e}")

Common Error Scenarios
----------------------

Missing Value Error
~~~~~~~~~~~~~~~~~~~

When using ``set()`` with a name but no value:

.. code-block:: python

   from parser_header import HeaderParser

   parser = HeaderParser()

   try:
       parser.set('Content-Type')  # Missing value!
   except ValueError as e:
       print(f"Error: {e}")
       # Output: Error: value is required when name is provided

Key Not Found Error
~~~~~~~~~~~~~~~~~~~

When accessing a non-existent header/cookie with bracket notation:

.. code-block:: python

   from parser_header import HeaderParser, CookieParser

   parser = HeaderParser()

   try:
       value = parser['nonexistent']
   except KeyError as e:
       print(f"Error: {e}")
       # Output: Error: "Header 'nonexistent' not found"

   cookies = CookieParser()

   try:
       value = cookies['missing']
   except KeyError as e:
       print(f"Error: {e}")
       # Output: Error: "Cookie 'missing' not found"

Delete Non-Existent Key
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser

   parser = HeaderParser(content_type='json')

   try:
       del parser['nonexistent']
   except KeyError as e:
       print(f"Error: {e}")
       # Output: Error: "Header 'nonexistent' not found"

Best Practices
--------------

Catch Specific Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser, ParserError, InvalidHeaderError
   from parser_header.exceptions import EncodingError

   def parse_headers(data):
       try:
           parser = HeaderParser(data)
           return parser.to_dict()
       except EncodingError:
           print("Could not decode input data")
           return None
       except InvalidHeaderError:
           print("Invalid header format")
           return None
       except ParserError:
           print("Unknown parser error")
           return None

Use get() with Default
~~~~~~~~~~~~~~~~~~~~~~

To avoid KeyError, use ``get()`` with a default value:

.. code-block:: python

   from parser_header import HeaderParser

   parser = HeaderParser(content_type='json')

   # Safe access - returns default if not found
   value = parser.get('nonexistent', 'default')
   print(value)  # 'default'

   # Check existence first
   if 'content-type' in parser:
       value = parser['content-type']

Validate Before Processing
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser

   def process_request(raw_headers):
       parser = HeaderParser(raw_headers)

       # Validate required headers
       required = ['content-type', 'authorization']
       missing = [h for h in required if h not in parser]

       if missing:
           raise ValueError(f"Missing required headers: {missing}")

       # Safe to proceed
       return parser.to_dict()