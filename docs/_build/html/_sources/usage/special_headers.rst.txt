===============
Special Headers
===============

**pyheaderparse** automatically parses certain headers into structured formats for easier access.

Content-Type with Parameters
----------------------------

Content-Type headers are parsed into ``HeaderValue`` objects with separate value and parameters:

.. code-block:: python

   from parser_header import HeaderParser

   parser = HeaderParser()
   parser.set('content-type', 'text/html; charset=utf-8; boundary=something')

   ct = parser.get('content-type')

   print(f"Type: {type(ct)}")
   # Output: Type: <class 'parser_header.parser.HeaderValue'>

   print(f"Value: {ct.value}")
   # Output: Value: text/html

   print(f"Params: {ct.params}")
   # Output: Params: {'charset': 'utf-8', 'boundary': 'something'}

   print(f"Charset: {ct.params.get('charset')}")
   # Output: Charset: utf-8

   # The content_type property returns just the value
   print(f"Property: {parser.content_type}")
   # Output: Property: text/html

   # String representation
   print(f"String: {str(ct)}")
   # Output: String: text/html; charset=utf-8; boundary=something

Content-Disposition
-------------------

Similar to Content-Type, parsed with parameters:

.. code-block:: python

   parser = HeaderParser()
   parser.set('content-disposition', 'attachment; filename="report.pdf"; size=1024')

   cd = parser.get('content-disposition')

   print(f"Value: {cd.value}")
   # Output: Value: attachment

   print(f"Filename: {cd.params.get('filename')}")
   # Output: Filename: report.pdf

   print(f"Size: {cd.params.get('size')}")
   # Output: Size: 1024

Accept Header
-------------

Accept headers are parsed into a list of media types with quality values, sorted by quality (descending):

.. code-block:: python

   parser = HeaderParser()
   parser.set('accept', 'text/html,application/json;q=0.9,*/*;q=0.8,text/plain;q=0.7')

   accept = parser.get('accept')

   print(accept)
   # Output (sorted by quality):
   # [
   #     {'type': 'text/html', 'q': 1.0},
   #     {'type': 'application/json', 'q': 0.9},
   #     {'type': '*/*', 'q': 0.8},
   #     {'type': 'text/plain', 'q': 0.7}
   # ]

   # Get preferred type
   print(f"Preferred: {accept[0]['type']}")
   # Output: Preferred: text/html

   # Check if JSON is accepted
   json_accepted = any(a['type'] == 'application/json' for a in accept)
   print(f"JSON accepted: {json_accepted}")
   # Output: JSON accepted: True

Special case - wildcard:

.. code-block:: python

   parser = HeaderParser()
   parser.set('accept', '*/*')

   print(parser.get('accept'))
   # Output: [{'type': '*/*', 'q': 1.0}]

Accept-Language
---------------

Accept-Language is parsed similarly with language codes and quality values:

.. code-block:: python

   parser = HeaderParser()
   parser.set('accept-language', 'en-US,en;q=0.9,es;q=0.8,fr;q=0.7,de;q=0.5')

   langs = parser.get('accept-language')

   print(langs)
   # Output (sorted by quality):
   # [
   #     {'lang': 'en-US', 'q': 1.0},
   #     {'lang': 'en', 'q': 0.9},
   #     {'lang': 'es', 'q': 0.8},
   #     {'lang': 'fr', 'q': 0.7},
   #     {'lang': 'de', 'q': 0.5}
   # ]

   # Get preferred language
   print(f"Preferred: {langs[0]['lang']}")
   # Output: Preferred: en-US

   # Get all accepted languages
   all_langs = [l['lang'] for l in langs]
   print(f"All: {all_langs}")
   # Output: All: ['en-US', 'en', 'es', 'fr', 'de']

Accept-Encoding
---------------

Accept-Encoding is parsed into a simple list:

.. code-block:: python

   parser = HeaderParser()
   parser.set('accept-encoding', 'gzip, deflate, br, zstd')

   encodings = parser.get('accept-encoding')

   print(encodings)
   # Output: ['gzip', 'deflate', 'br', 'zstd']

   # Check support
   print(f"Supports gzip: {'gzip' in encodings}")
   # Output: Supports gzip: True

   print(f"Supports brotli: {'br' in encodings}")
   # Output: Supports brotli: True

Cache-Control
-------------

Cache-Control directives are parsed into a dictionary:

.. code-block:: python

   parser = HeaderParser()
   parser.set('cache-control', 'max-age=3600, public, no-transform, must-revalidate')

   cache = parser.get('cache-control')

   print(cache)
   # Output:
   # {
   #     'max-age': 3600,        # Numeric values parsed as int
   #     'public': True,         # Flags parsed as True
   #     'no-transform': True,
   #     'must-revalidate': True
   # }

   # Access directives
   print(f"Max age: {cache.get('max-age')} seconds")
   # Output: Max age: 3600 seconds

   print(f"Is public: {cache.get('public', False)}")
   # Output: Is public: True

   print(f"No cache: {cache.get('no-cache', False)}")
   # Output: No cache: False

Boolean Headers
---------------

Certain headers are automatically parsed as boolean values:

* ``DNT`` (Do Not Track)
* ``Sec-GPC`` (Global Privacy Control)
* ``Upgrade-Insecure-Requests``

.. code-block:: python

   parser = HeaderParser()
   parser.set('dnt', '1')
   parser.set('sec-gpc', '1')
   parser.set('upgrade-insecure-requests', '1')

   print(f"DNT: {parser.get('dnt')}")
   # Output: DNT: True

   print(f"Sec-GPC: {parser.get('sec-gpc')}")
   # Output: Sec-GPC: True

   print(f"UIR: {parser.get('upgrade-insecure-requests')}")
   # Output: UIR: True

   # Type check
   print(f"Type: {type(parser.get('dnt'))}")
   # Output: Type: <class 'bool'>

Recognized true values: ``1``, ``true``, ``yes``, ``?1``

Client Hints (Sec-CH-UA-*)
--------------------------

Modern browsers send Client Hints for feature detection. These are parsed specially:

Sec-CH-UA (User Agent Brands)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()
   parser.set('sec-ch-ua', '"Chrome";v="144", "Not A Brand";v="8", "Chromium";v="144"')

   ua = parser.get('sec-ch-ua')

   print(ua)
   # Output:
   # [
   #     {'brand': 'Chrome', 'version': '144'},
   #     {'brand': 'Not A Brand', 'version': '8'},
   #     {'brand': 'Chromium', 'version': '144'}
   # ]

   # Find Chrome version
   chrome = next((b for b in ua if b['brand'] == 'Chrome'), None)
   if chrome:
       print(f"Chrome version: {chrome['version']}")
   # Output: Chrome version: 144

Sec-CH-UA-Mobile
~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()

   # Mobile device
   parser.set('sec-ch-ua-mobile', '?1')
   print(f"Is mobile: {parser.get('sec-ch-ua-mobile')}")
   # Output: Is mobile: True

   # Desktop
   parser.set('sec-ch-ua-mobile', '?0')
   print(f"Is mobile: {parser.get('sec-ch-ua-mobile')}")
   # Output: Is mobile: False

Other Client Hints
~~~~~~~~~~~~~~~~~~

String values have quotes stripped automatically:

.. code-block:: python

   raw = '''sec-ch-ua-platform: "Windows"
   sec-ch-ua-arch: "x86"
   sec-ch-ua-bitness: "64"
   sec-ch-ua-model: ""
   sec-ch-ua-full-version: "144.0.7524.3"
   sec-ch-ua-platform-version: "15.0.0"
   '''

   parser = HeaderParser(raw)

   print(f"Platform: {parser.get('sec-ch-ua-platform')}")
   # Output: Platform: Windows (quotes stripped)

   print(f"Arch: {parser.get('sec-ch-ua-arch')}")
   # Output: Arch: x86

   print(f"Bitness: {parser.get('sec-ch-ua-bitness')}")
   # Output: Bitness: 64

   print(f"Model: {parser.get('sec-ch-ua-model')}")
   # Output: Model: (empty string)

   print(f"Full Version: {parser.get('sec-ch-ua-full-version')}")
   # Output: Full Version: 144.0.7524.3

Get All Client Hints
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw = '''sec-ch-ua: "Chrome";v="144"
   sec-ch-ua-mobile: ?0
   sec-ch-ua-platform: "Windows"
   sec-ch-ua-arch: "x86"
   '''

   parser = HeaderParser(raw)
   hints = parser.get_client_hints()

   print(hints)
   # Output:
   # {
   #     'sec-ch-ua': [{'brand': 'Chrome', 'version': '144'}],
   #     'sec-ch-ua-mobile': False,
   #     'sec-ch-ua-platform': 'Windows',
   #     'sec-ch-ua-arch': 'x86'
   # }

Sec-CH-UA-Full-Version-List
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   parser = HeaderParser()
   parser.set(
       'sec-ch-ua-full-version-list',
       '"Not(A:Brand";v="8.0.0.0", "Chromium";v="144.0.7524.3", "Google Chrome";v="144.0.7524.3"'
   )

   versions = parser.get('sec-ch-ua-full-version-list')

   print(versions)
   # Output:
   # [
   #     {'brand': 'Not(A:Brand', 'version': '8.0.0.0'},
   #     {'brand': 'Chromium', 'version': '144.0.7524.3'},
   #     {'brand': 'Google Chrome', 'version': '144.0.7524.3'}
   # ]

Fetch Metadata (Sec-Fetch-*)
----------------------------

Sec-Fetch headers provide context about how a request was initiated:

.. code-block:: python

   raw = '''sec-fetch-site: same-origin
   sec-fetch-mode: cors
   sec-fetch-dest: empty
   sec-fetch-user: ?1
   '''

   parser = HeaderParser(raw)

   # Individual access
   print(f"Site: {parser.get('sec-fetch-site')}")
   # Output: Site: same-origin

   print(f"Mode: {parser.get('sec-fetch-mode')}")
   # Output: Mode: cors

   print(f"Dest: {parser.get('sec-fetch-dest')}")
   # Output: Dest: empty

   # Get all at once
   metadata = parser.get_sec_fetch_metadata()
   print(metadata)
   # Output:
   # {
   #     'site': 'same-origin',
   #     'mode': 'cors',
   #     'dest': 'empty',
   #     'user': '?1'
   # }

**Common Values:**

* ``sec-fetch-site``: ``same-origin``, ``same-site``, ``cross-site``, ``none``
* ``sec-fetch-mode``: ``navigate``, ``cors``, ``no-cors``, ``same-origin``, ``websocket``
* ``sec-fetch-dest``: ``document``, ``script``, ``style``, ``image``, ``font``, ``empty``, etc.

Priority Header
---------------

The Priority header (HTTP/2 and HTTP/3) is parsed into a dictionary:

.. code-block:: python

   parser = HeaderParser()
   parser.set('priority', 'u=1, i')

   priority = parser.get('priority')

   print(priority)
   # Output: {'u': '1', 'i': True}

   # u = urgency (0-7, lower is more urgent)
   # i = incremental (boolean flag)

   print(f"Urgency: {priority.get('u')}")
   # Output: Urgency: 1

   print(f"Incremental: {priority.get('i')}")
   # Output: Incremental: True

Content-Length
--------------

Content-Length is automatically parsed as an integer:

.. code-block:: python

   parser = HeaderParser()
   parser.set('content-length', '1024')

   length = parser.get('content-length')

   print(f"Value: {length}")
   # Output: Value: 1024

   print(f"Type: {type(length)}")
   # Output: Type: <class 'int'>

   # Also via property
   print(f"Property: {parser.content_length}")
   # Output: Property: 1024

Custom/Unknown Headers
----------------------

Headers that don't have special parsing are stored as plain strings:

.. code-block:: python

   parser = HeaderParser()
   parser.set('x-custom-header', 'some value here')
   parser.set('x-request-id', 'req-12345-abcde')
   parser.set('authorization', 'Bearer eyJhbGciOiJIUzI1NiIs...')

   print(parser.get('x-custom-header'))
   # Output: some value here

   print(parser.get('x-request-id'))
   # Output: req-12345-abcde

   print(parser.get('authorization'))
   # Output: Bearer eyJhbGciOiJIUzI1NiIs...

Using set_raw() to Skip Parsing
-------------------------------

If you want to store a value without any parsing:

.. code-block:: python

   parser = HeaderParser()

   # With set() - value is parsed
   parser.set('cache-control', 'max-age=3600')
   print(parser.get('cache-control'))
   # Output: {'max-age': 3600}

   # With set_raw() - value stored as-is
   parser.set_raw('cache-control', 'max-age=3600')
   print(parser.get('cache-control'))
   # Output: max-age=3600 (string)