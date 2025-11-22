===========
Quick Start
===========

This guide will help you get started with **pyheaderparse** in just a few minutes.

Basic Usage
-----------

Parsing HTTP Headers
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser

   # Parse raw HTTP headers
   raw_headers = """content-type: application/json
   content-length: 1024
   user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0
   accept: */*
   cookie: session=abc123; user=john
   """

   parser = HeaderParser(raw_headers)

   # Access headers via properties
   print(parser.content_type)     # 'application/json'
   print(parser.content_length)   # 1024 (as int)
   print(parser.user_agent)       # 'Mozilla/5.0 ...'

   # Access any header
   print(parser.get('accept'))    # [{'type': '*/*', 'q': 1.0}]

**Output:**

.. code-block:: text

   application/json
   1024
   Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0
   [{'type': '*/*', 'q': 1.0}]

Creating Headers from Kwargs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser

   # Create headers using keyword arguments
   # Note: underscores are converted to hyphens automatically
   parser = HeaderParser(
       content_type='application/json',
       user_agent='MyApp/1.0',
       x_request_id='req-12345',
       authorization='Bearer token123'
   )

   print(parser.to_raw())

**Output:**

.. code-block:: text

   content-type: application/json
   user-agent: MyApp/1.0
   x-request-id: req-12345
   authorization: Bearer token123

Parsing Cookies
~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import CookieParser

   # Parse cookies from raw data
   raw_cookies = """cookie: session=abc123
   cookie: user=john
   cookie: token=xyz789
   """

   cookies = CookieParser(raw_cookies)

   # Get as Cookie header string
   print(cookies.to_cookie_header())

   # Get as dictionary
   print(cookies.to_dict())

   # Access individual cookie
   print(cookies.get('session'))

**Output:**

.. code-block:: text

   session=abc123; user=john; token=xyz789
   {'session': 'abc123', 'user': 'john', 'token': 'xyz789'}
   abc123

Creating Cookies from Kwargs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import CookieParser

   # Create cookies using kwargs
   cookies = CookieParser(
       session='abc123',
       user_id='12345',
       auth_token='xyz789'
   )

   print(cookies.to_cookie_header())
   print(cookies.to_dict())

**Output:**

.. code-block:: text

   session=abc123; user-id=12345; auth-token=xyz789
   {'session': 'abc123', 'user-id': '12345', 'auth-token': 'xyz789'}

Setting and Modifying Headers
-----------------------------

Using set() Method
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser

   parser = HeaderParser()

   # Positional arguments
   parser.set('Content-Type', 'application/json')

   # Kwargs only
   parser.set(user_agent='Mozilla/5.0', accept='*/*')

   # Mixed
   parser.set('Authorization', 'Bearer token', x_request_id='12345')

   print(parser.to_raw())

**Output:**

.. code-block:: text

   content-type: application/json
   user-agent: Mozilla/5.0
   accept: */*
   authorization: Bearer token
   x-request-id: 12345

Method Chaining
~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import HeaderParser

   parser = (
       HeaderParser()
       .set(content_type='application/json')
       .set(accept='*/*')
       .set(user_agent='MyApp/1.0')
       .set_cookie(session='abc123', user='john')
   )

   print(parser.to_raw())
   print(f"Cookies: {parser.get_cookies_as_header()}")

**Output:**

.. code-block:: text

   content-type: application/json
   accept: */*
   user-agent: MyApp/1.0
   Cookies: session=abc123; user=john

Accessing Cookies via HeaderParser
----------------------------------

.. code-block:: python

   from parser_header import HeaderParser

   raw = """content-type: application/json
   cookie: session=abc123
   cookie: user=john
   """

   parser = HeaderParser(raw)

   # Access cookies
   print(parser.get_cookie('session'))      # Individual cookie
   print(parser.get_cookies_as_header())    # As header string
   print(parser.get_cookies_as_dict())      # As dictionary

**Output:**

.. code-block:: text

   abc123
   session=abc123; user=john
   {'session': 'abc123', 'user': 'john'}

Integration with Requests Library
---------------------------------

.. code-block:: python

   from parser_header import HeaderParser
   import requests

   # Create headers
   parser = HeaderParser(
       content_type='application/json',
       authorization='Bearer my-token',
       user_agent='MyApp/1.0'
   )

   # Convert to requests-compatible format
   headers = parser.to_requests_headers()

   # Use with requests
   response = requests.get('https://httpbin.org/get', headers=headers)
   print(response.json())

   # Parse response headers
   response_parser = HeaderParser.from_requests_response(response)
   print(f"Response Content-Type: {response_parser.content_type}")

CLI Quick Start
---------------

Parse headers from a file:

.. code-block:: bash

   $ pyheaderparse parse -f headers.txt
   {
     "content-type": {"value": "application/json", "params": {}},
     "content-length": 1024,
     "user-agent": "Mozilla/5.0"
   }

Get specific header:

.. code-block:: bash

   $ pyheaderparse parse -f headers.txt --header user-agent
   "Mozilla/5.0"

Parse cookies:

.. code-block:: bash

   $ pyheaderparse cookies -f headers.txt --full-headers --as-header
   session=abc123; user=john; token=xyz789

What's Next?
------------

* :doc:`usage/header_parser` - Detailed HeaderParser guide
* :doc:`usage/cookie_parser` - Detailed CookieParser guide
* :doc:`usage/special_headers` - Parsing special headers (Client Hints, etc.)
* :doc:`api/modules` - Complete API reference