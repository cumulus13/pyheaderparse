========================
HeaderParser API
========================

.. module:: parser_header.parser

   :synopsis: HTTP header parser classes

HeaderParser Class
------------------

.. class:: HeaderParser(data=None, **kwargs)

   Comprehensive HTTP header parser supporting all standard and custom headers.

   :param data: Raw header string or bytes to parse
   :type data: str | bytes | None
   :param kwargs: Header key-value pairs (underscores converted to hyphens)

   **Example:**

   .. code-block:: python

      # From raw data
      parser = HeaderParser("content-type: application/json")

      # From kwargs
      parser = HeaderParser(content_type='application/json', user_agent='MyApp')

      # Mixed
      parser = HeaderParser("accept: */*", content_type='json')

Constructor and Factory Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: HeaderParser.__init__(data=None, **kwargs)

   Initialize HeaderParser with optional data and/or kwargs.

.. classmethod:: HeaderParser.from_dict(headers)

   Create HeaderParser from a dictionary.

   :param headers: Dictionary of header name-value pairs
   :type headers: dict
   :returns: New HeaderParser instance
   :rtype: HeaderParser

   .. code-block:: python

      parser = HeaderParser.from_dict({
          'Content-Type': 'application/json',
          'Authorization': 'Bearer token'
      })

.. classmethod:: HeaderParser.from_kwargs(**kwargs)

   Create HeaderParser from keyword arguments.

   :param kwargs: Header key-value pairs
   :returns: New HeaderParser instance
   :rtype: HeaderParser

   .. code-block:: python

      parser = HeaderParser.from_kwargs(
          content_type='application/json',
          accept='*/*'
      )

.. classmethod:: HeaderParser.from_requests_response(response)

   Create HeaderParser from a requests Response object.

   :param response: requests Response object
   :returns: New HeaderParser instance
   :rtype: HeaderParser

   .. code-block:: python

      import requests
      response = requests.get('https://example.com')
      parser = HeaderParser.from_requests_response(response)

Parsing Methods
~~~~~~~~~~~~~~~

.. method:: HeaderParser.parse(data=None, **kwargs)

   Parse raw HTTP headers and/or kwargs.

   :param data: Raw header string/bytes
   :type data: str | bytes | None
   :param kwargs: Additional headers as key=value pairs
   :returns: Dictionary of parsed headers
   :rtype: dict

   .. code-block:: python

      parser = HeaderParser()
      parser.parse("content-type: text/html", accept='*/*')

Setting Methods
~~~~~~~~~~~~~~~

.. method:: HeaderParser.set(name=None, value=None, **kwargs)

   Set header(s) with parsing.

   :param name: Header name (optional if using kwargs)
   :type name: str | None
   :param value: Header value (required if name provided)
   :type value: Any | None
   :param kwargs: Header key=value pairs
   :returns: self for chaining
   :rtype: HeaderParser
   :raises ValueError: If name provided without value

   .. code-block:: python

      parser.set('Content-Type', 'application/json')
      parser.set(user_agent='Mozilla', accept='*/*')
      parser.set('Auth', 'Bearer x', x_request_id='123')

.. method:: HeaderParser.set_raw(name=None, value=None, **kwargs)

   Set header(s) without parsing the value.

   :param name: Header name
   :param value: Header value (stored as-is)
   :param kwargs: Header key=value pairs
   :returns: self for chaining
   :rtype: HeaderParser

   .. code-block:: python

      # Value stored as string, not parsed
      parser.set_raw('cache-control', 'max-age=3600')

.. method:: HeaderParser.update(data=None, **kwargs)

   Update headers from dict and/or kwargs.

   :param data: Dictionary of headers
   :type data: dict | None
   :param kwargs: Additional headers
   :returns: self for chaining
   :rtype: HeaderParser

   .. code-block:: python

      parser.update({'Accept': '*/*'}, user_agent='Test')

.. method:: HeaderParser.remove(*names)

   Remove headers by name.

   :param names: Header names to remove
   :returns: self for chaining
   :rtype: HeaderParser

   .. code-block:: python

      parser.remove('x-custom', 'accept')

.. method:: HeaderParser.clear()

   Clear all headers and cookies.

   :returns: self for chaining
   :rtype: HeaderParser

Accessing Methods
~~~~~~~~~~~~~~~~~

.. method:: HeaderParser.get(name, default=None)

   Get header value by name (case-insensitive).

   :param name: Header name
   :type name: str
   :param default: Default value if not found
   :returns: Header value or default

   .. code-block:: python

      parser.get('content-type')  # HeaderValue or string
      parser.get('missing', 'N/A')  # 'N/A'

.. method:: HeaderParser.__getitem__(name)

   Get header with bracket notation.

   :param name: Header name
   :raises KeyError: If header not found

   .. code-block:: python

      parser['content-type']

.. method:: HeaderParser.__setitem__(name, value)

   Set header with bracket notation.

   .. code-block:: python

      parser['Content-Type'] = 'application/json'

.. method:: HeaderParser.__delitem__(name)

   Delete header with bracket notation.

   :raises KeyError: If header not found

   .. code-block:: python

      del parser['x-custom']

.. method:: HeaderParser.__contains__(name)

   Check if header exists.

   :returns: True if header exists
   :rtype: bool

   .. code-block:: python

      'content-type' in parser  # True/False

.. method:: HeaderParser.__len__()

   Get number of headers.

   :returns: Header count
   :rtype: int

.. method:: HeaderParser.__iter__()

   Iterate over header names.

   .. code-block:: python

      for name in parser:
          print(name)

.. method:: HeaderParser.keys()

   Get list of header names.

   :returns: List of names
   :rtype: list[str]

.. method:: HeaderParser.values()

   Get list of header values.

   :returns: List of values
   :rtype: list

.. method:: HeaderParser.items()

   Get list of (name, value) tuples.

   :returns: List of tuples
   :rtype: list[tuple]

Export Methods
~~~~~~~~~~~~~~

.. method:: HeaderParser.to_dict(stringify=False)

   Export headers as dictionary.

   :param stringify: If True, convert all values to strings
   :type stringify: bool
   :returns: Dictionary of headers
   :rtype: dict

   .. code-block:: python

      parser.to_dict()  # With parsed values
      parser.to_dict(stringify=True)  # All strings

.. method:: HeaderParser.to_raw()

   Convert headers to raw format string.

   :returns: Raw headers string
   :rtype: str

   .. code-block:: python

      print(parser.to_raw())
      # content-type: application/json
      # accept: */*

.. method:: HeaderParser.to_requests_headers()

   Convert to format suitable for requests library.

   :returns: Dictionary with string values
   :rtype: dict[str, str]

   .. code-block:: python

      import requests
      headers = parser.to_requests_headers()
      requests.get(url, headers=headers)

Cookie Methods
~~~~~~~~~~~~~~

.. attribute:: HeaderParser.cookies

   Access the CookieParser instance.

   :type: CookieParser

.. method:: HeaderParser.get_cookie(name, default=None)

   Get specific cookie value.

   :param name: Cookie name
   :param default: Default if not found
   :returns: Cookie value or default

.. method:: HeaderParser.set_cookie(name=None, value=None, **kwargs)

   Set cookie(s).

   :param name: Cookie name
   :param value: Cookie value
   :param kwargs: Cookie key=value pairs
   :returns: self for chaining
   :rtype: HeaderParser

   .. code-block:: python

      parser.set_cookie('session', 'abc')
      parser.set_cookie(user='john', token='xyz')

.. method:: HeaderParser.get_cookies_as_header()

   Get cookies as Cookie header string.

   :returns: Cookie header string
   :rtype: str

   .. code-block:: python

      parser.get_cookies_as_header()
      # "session=abc; user=john"

.. method:: HeaderParser.get_cookies_as_dict()

   Get cookies as dictionary.

   :returns: Dictionary of cookies
   :rtype: dict[str, str]

Properties
~~~~~~~~~~

.. attribute:: HeaderParser.content_type

   Get Content-Type value (without parameters).

   :type: str | None

.. attribute:: HeaderParser.content_length

   Get Content-Length as integer.

   :type: int | None

.. attribute:: HeaderParser.user_agent

   Get User-Agent value.

   :type: str | None

.. attribute:: HeaderParser.origin

   Get Origin value.

   :type: str | None

.. attribute:: HeaderParser.referer

   Get Referer value.

   :type: str | None

Utility Methods
~~~~~~~~~~~~~~~

.. method:: HeaderParser.is_cors()

   Check if request is CORS (has Origin header).

   :returns: True if CORS request
   :rtype: bool

.. method:: HeaderParser.is_ajax()

   Check if request is AJAX (X-Requested-With: XMLHttpRequest).

   :returns: True if AJAX request
   :rtype: bool

.. method:: HeaderParser.get_client_hints()

   Get all Client Hints (`Sec-CH-*`) headers.

   :returns: Dictionary of client hints
   :rtype: dict

.. method:: HeaderParser.get_sec_fetch_metadata()

   Get Sec-Fetch-* headers.

   :returns: Dictionary with site, mode, dest, user keys
   :rtype: dict

HeaderValue Class
-----------------

.. class:: HeaderValue

   Dataclass representing a header value with parameters.

   .. attribute:: value

      Main header value.

      :type: str

   .. attribute:: params

      Parameter dictionary.

      :type: dict[str, str]

   **Example:**

   .. code-block:: python

      # Created automatically when parsing Content-Type, etc.
      parser.set('content-type', 'text/html; charset=utf-8')
      hv = parser.get('content-type')

      print(hv.value)   # 'text/html'
      print(hv.params)  # {'charset': 'utf-8'}
      print(str(hv))    # 'text/html; charset=utf-8'
