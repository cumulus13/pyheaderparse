============
HeaderParser
============

The ``HeaderParser`` class is the main class for parsing and manipulating HTTP headers.

Importing
---------

.. code-block:: python

   from parser_header import HeaderParser

Creating a HeaderParser
-----------------------

From Raw String/Bytes
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw_headers = """content-length: 1171
   content-type: application/json
   user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0
   accept: */*
   accept-language: en-US,en;q=0.9,es;q=0.8
   cache-control: max-age=3600, public
   dnt: 1
   origin: https://example.com
   cookie: session=abc123
   """

   parser = HeaderParser(raw_headers)

   print(f"Total headers: {len(parser)}")
   # Output: Total headers: 9

   # Also works with bytes
   parser = HeaderParser(raw_headers.encode('utf-8'))

From Keyword Arguments
~~~~~~~~~~~~~~~~~~~~~~

Underscores in key names are automatically converted to hyphens:

.. code-block:: python

   parser = HeaderParser(
       content_type='application/json',
       content_length='1024',
       user_agent='MyApp/1.0',
       x_request_id='req-12345',
       x_custom_header='custom-value'
   )

   print(parser.to_raw())

**Output:**

.. code-block:: text

   content-type: application/json
   content-length: 1024
   user-agent: MyApp/1.0
   x-request-id: req-12345
   x-custom-header: custom-value

Mixed: Raw Data + Kwargs
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw = "content-type: text/html\naccept: */*"

   parser = HeaderParser(raw, user_agent='Mozilla/5.0', x_token='abc123')

   print(parser.keys())
   # Output: ['content-type', 'accept', 'user-agent', 'x-token']

Factory Methods
~~~~~~~~~~~~~~~

.. code-block:: python

   # From dictionary
   parser = HeaderParser.from_dict({
       'Content-Type': 'application/json',
       'Authorization': 'Bearer token123'
   })

   # From kwargs
   parser = HeaderParser.from_kwargs(
       content_type='text/xml',
       cache_control='no-cache'
   )

   # From requests Response object
   import requests
   response = requests.get('https://httpbin.org/get')
   parser = HeaderParser.from_requests_response(response)

Setting Headers
---------------

Using set() Method
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()

   # Positional arguments
   parser.set('Content-Type', 'application/json')

   # Kwargs only
   parser.set(user_agent='Mozilla/5.0', accept='*/*')

   # Mixed positional + kwargs
   parser.set('Authorization', 'Bearer token', x_request_id='12345')

   print(parser.to_raw())

**Output:**

.. code-block:: text

   content-type: application/json
   user-agent: Mozilla/5.0
   accept: */*
   authorization: Bearer token
   x-request-id: 12345

Using set_raw() - No Value Parsing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()

   # set() parses the value
   parser.set('cache-control', 'max-age=3600, public')
   print(parser.get('cache-control'))
   # Output: {'max-age': 3600, 'public': True}

   # set_raw() keeps value as-is (no parsing)
   parser.set_raw('x-raw-header', 'max-age=3600, public')
   print(parser.get('x-raw-header'))
   # Output: 'max-age=3600, public'

Using Bracket Notation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()

   # Set
   parser['Content-Type'] = 'application/json'
   parser['X-Custom'] = 'value'

   # Get (case-insensitive)
   print(parser['content-type'])  # 'application/json'

   # Delete
   del parser['X-Custom']
   print('x-custom' in parser)  # False

Using update() Method
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser(content_type='text/html')

   # Update from dict
   parser.update({'Accept': '*/*', 'Accept-Language': 'en-US'})

   # Update from kwargs
   parser.update(user_agent='TestAgent', x_token='abc')

   # Mixed
   parser.update({'Cache-Control': 'no-cache'}, dnt='1')

Method Chaining
~~~~~~~~~~~~~~~

All mutating methods return ``self`` for chaining:

.. code-block:: python

   parser = (
       HeaderParser()
       .set(content_type='application/json')
       .set(accept='*/*')
       .set(user_agent='MyApp/1.0')
       .set_cookie(session='abc123')
       .remove('accept')
   )

   print(len(parser))  # 2 (content-type and user-agent)

Removing and Clearing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser(
       content_type='application/json',
       accept='*/*',
       user_agent='Test',
       x_custom='value'
   )

   # Remove specific headers
   parser.remove('x-custom', 'accept')
   print(parser.keys())
   # Output: ['content-type', 'user-agent']

   # Clear all headers
   parser.clear()
   print(len(parser))  # 0

Accessing Headers
-----------------

Basic Access
~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser("""content-type: application/json; charset=utf-8
   content-length: 1024
   user-agent: Mozilla/5.0
   """)

   # get() method - case-insensitive, with default
   print(parser.get('Content-Type'))
   # Output: HeaderValue(value='application/json', params={'charset': 'utf-8'})

   print(parser.get('X-Missing', 'N/A'))
   # Output: 'N/A'

   # Bracket notation
   print(parser['user-agent'])
   # Output: 'Mozilla/5.0'

   # Check existence
   print('content-type' in parser)  # True
   print('x-missing' in parser)     # False

Property Shortcuts
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser("""content-type: application/json
   content-length: 1024
   user-agent: Mozilla/5.0
   origin: https://example.com
   referer: https://example.com/page
   """)

   print(parser.content_type)    # 'application/json'
   print(parser.content_length)  # 1024 (as int)
   print(parser.user_agent)      # 'Mozilla/5.0'
   print(parser.origin)          # 'https://example.com'
   print(parser.referer)         # 'https://example.com/page'

Iteration
~~~~~~~~~

.. code-block:: python

   parser = HeaderParser(content_type='application/json', accept='*/*', dnt='1')

   # Iterate keys
   for name in parser:
       print(f"{name}: {parser[name]}")

   # Output:
   # content-type: application/json
   # accept: [{'type': '*/*', 'q': 1.0}]
   # dnt: True

   # Get all keys, values, items
   print(parser.keys())    # ['content-type', 'accept', 'dnt']
   print(parser.values())  # [HeaderValue(...), [...], True]
   print(parser.items())   # [('content-type', ...), ...]

Export/Conversion
-----------------

to_dict()
~~~~~~~~~

.. code-block:: python

   parser = HeaderParser(content_type='application/json', dnt='1')

   # Normal dict (with parsed values)
   print(parser.to_dict())
   # Output: {'content-type': HeaderValue(...), 'dnt': True}

   # Stringified values
   print(parser.to_dict(stringify=True))
   # Output: {'content-type': 'application/json', 'dnt': 'True'}

to_raw()
~~~~~~~~

.. code-block:: python

   parser = HeaderParser(content_type='application/json', accept='*/*')

   print(parser.to_raw())
   # Output:
   # content-type: application/json
   # accept: [{'type': '*/*', 'q': 1.0}]

to_requests_headers()
~~~~~~~~~~~~~~~~~~~~~

Convert to format suitable for ``requests`` library:

.. code-block:: python

   parser = HeaderParser(
       content_type='application/json',
       authorization='Bearer token'
   )

   headers = parser.to_requests_headers()
   print(headers)
   # Output: {'content-type': 'application/json', 'authorization': 'Bearer token'}

   # Use with requests
   import requests
   response = requests.get('https://httpbin.org/get', headers=headers)

Working with Cookies
--------------------

Accessing Cookies
~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw = """content-type: application/json
   cookie: session=abc123
   cookie: user=john
   """

   parser = HeaderParser(raw)

   # Access CookieParser instance
   print(parser.cookies.to_dict())
   # Output: {'session': 'abc123', 'user': 'john'}

   # Shortcut methods
   print(parser.get_cookie('session'))       # 'abc123'
   print(parser.get_cookies_as_header())     # 'session=abc123; user=john'
   print(parser.get_cookies_as_dict())       # {'session': 'abc123', 'user': 'john'}

Setting Cookies
~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()

   # Set cookies using set_cookie()
   parser.set_cookie('session', 'abc123')
   parser.set_cookie(user='john', token='xyz')

   print(parser.get_cookies_as_header())
   # Output: session=abc123; user=john; token=xyz

Utility Methods
---------------

CORS and AJAX Detection
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser(
       origin='https://example.com',
       x_requested_with='XMLHttpRequest'
   )

   print(parser.is_cors())  # True
   print(parser.is_ajax())  # True

   parser2 = HeaderParser(user_agent='Mozilla/5.0')
   print(parser2.is_cors())  # False
   print(parser2.is_ajax())  # False

Get Client Hints
~~~~~~~~~~~~~~~~

.. code-block:: python

   raw = """sec-ch-ua: "Chrome";v="144"
   sec-ch-ua-mobile: ?0
   sec-ch-ua-platform: "Windows"
   """

   parser = HeaderParser(raw)
   hints = parser.get_client_hints()
   print(hints)
   # Output:
   # {
   #     'sec-ch-ua': [{'brand': 'Chrome', 'version': '144'}],
   #     'sec-ch-ua-mobile': False,
   #     'sec-ch-ua-platform': 'Windows'
   # }

Get Sec-Fetch Metadata
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw = """sec-fetch-site: same-origin
   sec-fetch-mode: cors
   sec-fetch-dest: empty
   """

   parser = HeaderParser(raw)
   metadata = parser.get_sec_fetch_metadata()
   print(metadata)
   # Output:
   # {
   #     'site': 'same-origin',
   #     'mode': 'cors',
   #     'dest': 'empty',
   #     'user': ''
   # }