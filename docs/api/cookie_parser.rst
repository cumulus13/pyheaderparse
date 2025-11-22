========================
CookieParser API
========================

.. module:: parser_header.parser
   :synopsis: Cookie parser class

CookieParser Class
------------------

.. class:: CookieParser(data=None, **kwargs)

   Parser for HTTP cookies with multiple extraction methods.

   :param data: Raw cookie string or bytes to parse
   :type data: str | bytes | None
   :param kwargs: Cookie key-value pairs (underscores converted to hyphens)

   **Example:**

   .. code-block:: python

      # From raw data
      cookies = CookieParser("cookie: session=abc; user=john")

      # From kwargs
      cookies = CookieParser(session='abc', user='john')

      # Mixed
      cookies = CookieParser("cookie: a=1", b='2', c='3')

Constructor and Factory Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. method:: CookieParser.__init__(data=None, **kwargs)

   Initialize CookieParser with optional data and/or kwargs.

.. classmethod:: CookieParser.from_dict(cookies)

   Create CookieParser from a dictionary.

   :param cookies: Dictionary of cookie name-value pairs
   :type cookies: dict[str, str]
   :returns: New CookieParser instance
   :rtype: CookieParser

   .. code-block:: python

      cookies = CookieParser.from_dict({
          'session': 'abc123',
          'user': 'john'
      })

.. classmethod:: CookieParser.from_kwargs(**kwargs)

   Create CookieParser from keyword arguments.

   :param kwargs: Cookie key-value pairs
   :returns: New CookieParser instance
   :rtype: CookieParser

   .. code-block:: python

      cookies = CookieParser.from_kwargs(
          session='abc123',
          auth_token='xyz'
      )

Parsing Method
~~~~~~~~~~~~~~

.. method:: CookieParser.parse(data=None, **kwargs)

   Parse cookies from raw data and/or kwargs.

   :param data: Raw cookie string/bytes
   :type data: str | bytes | None
   :param kwargs: Additional cookies as key=value pairs
   :returns: Dictionary of cookies
   :rtype: dict[str, str]

   .. code-block:: python

      cookies = CookieParser()
      cookies.parse("cookie: a=1; b=2", c='3')
      # Result: {'a': '1', 'b': '2', 'c': '3'}

Setting Methods
~~~~~~~~~~~~~~~

.. method:: CookieParser.set(name=None, value=None, **kwargs)

   Set cookie(s).

   :param name: Cookie name (optional if using kwargs)
   :type name: str | None
   :param value: Cookie value (required if name provided)
   :type value: str | None
   :param kwargs: Cookie key=value pairs
   :returns: self for chaining
   :rtype: CookieParser
   :raises ValueError: If name provided without value

   .. code-block:: python

      cookies.set('session', 'abc123')
      cookies.set(user='john', token='xyz')
      cookies.set('a', '1', b='2', c='3')

.. method:: CookieParser.update(data=None, **kwargs)

   Update cookies from dict and/or kwargs.

   :param data: Dictionary of cookies
   :type data: dict[str, str] | None
   :param kwargs: Additional cookies
   :returns: self for chaining
   :rtype: CookieParser

   .. code-block:: python

      cookies.update({'a': '1', 'b': '2'}, c='3')

.. method:: CookieParser.remove(*names)

   Remove cookies by name.

   :param names: Cookie names to remove
   :returns: self for chaining
   :rtype: CookieParser

   .. code-block:: python

      cookies.remove('session', 'token')

.. method:: CookieParser.clear()

   Clear all cookies.

   :returns: self for chaining
   :rtype: CookieParser

Accessing Methods
~~~~~~~~~~~~~~~~~

.. method:: CookieParser.get(name, default=None)

   Get specific cookie value.

   :param name: Cookie name (underscores and hyphens interchangeable)
   :type name: str
   :param default: Default value if not found
   :returns: Cookie value or default
   :rtype: str | None

   .. code-block:: python

      cookies.get('session')           # 'abc123'
      cookies.get('user-id')           # Works
      cookies.get('user_id')           # Also works
      cookies.get('missing', 'N/A')    # 'N/A'

.. method:: CookieParser.__getitem__(name)

   Get cookie with bracket notation.

   :param name: Cookie name
   :raises KeyError: If cookie not found

   .. code-block:: python

      cookies['session']  # 'abc123'

.. method:: CookieParser.__setitem__(name, value)

   Set cookie with bracket notation.

   .. code-block:: python

      cookies['session'] = 'new_value'

.. method:: CookieParser.__delitem__(name)

   Delete cookie with bracket notation.

   :raises KeyError: If cookie not found

   .. code-block:: python

      del cookies['session']

.. method:: CookieParser.__contains__(name)

   Check if cookie exists.

   :returns: True if cookie exists
   :rtype: bool

   .. code-block:: python

      'session' in cookies  # True/False

.. method:: CookieParser.__len__()

   Get number of cookies.

   :returns: Cookie count
   :rtype: int

.. method:: CookieParser.__iter__()

   Iterate over cookie names.

   .. code-block:: python

      for name in cookies:
          print(f"{name}={cookies[name]}")

.. method:: CookieParser.keys()

   Get list of cookie names.

   :returns: List of names
   :rtype: list[str]

.. method:: CookieParser.values()

   Get list of cookie values.

   :returns: List of values
   :rtype: list[str]

.. method:: CookieParser.items()

   Get list of (name, value) tuples.

   :returns: List of tuples
   :rtype: list[tuple[str, str]]

Output Methods
~~~~~~~~~~~~~~

.. method:: CookieParser.to_cookie_header(data=None, **kwargs)

   Convert cookies to Cookie header format.

   :param data: Optional new data to parse first
   :type data: str | bytes | None
   :param kwargs: Additional cookies to include
   :returns: Cookie header string (semicolon-separated)
   :rtype: str

   .. code-block:: python

      cookies = CookieParser(session='abc', user='john')

      cookies.to_cookie_header()
      # "session=abc; user=john"

      cookies.to_cookie_header(token='xyz')
      # "session=abc; user=john; token=xyz"

.. method:: CookieParser.to_dict(data=None, **kwargs)

   Get cookies as dictionary.

   :param data: Optional new data to parse first
   :type data: str | bytes | None
   :param kwargs: Additional cookies to include
   :returns: Dictionary of cookies
   :rtype: dict[str, str]

   .. code-block:: python

      cookies = CookieParser(session='abc')

      cookies.to_dict()
      # {'session': 'abc'}

      cookies.to_dict(extra='value')
      # {'session': 'abc', 'extra': 'value'}

Method Chaining
~~~~~~~~~~~~~~~

All mutating methods return ``self`` for chaining:

.. code-block:: python

   cookies = (
       CookieParser()
       .set('session', 'abc')
       .set(user='john', token='xyz')
       .remove('token')
       .update({'lang': 'en'})
   )

   print(cookies.to_cookie_header())
   # "session=abc; user=john; lang=en"

Complete Example
~~~~~~~~~~~~~~~~

.. code-block:: python

   from parser_header import CookieParser

   # Create and manipulate
   cookies = CookieParser(session='initial')
   cookies.set(user='john')
   cookies['token'] = 'xyz123'
   cookies.update({'lang': 'en'}, theme='dark')

   # Access
   print(cookies.get('session'))  # 'initial'
   print(cookies['user'])         # 'john'
   print(len(cookies))            # 5

   # Check existence
   print('token' in cookies)      # True
   print('missing' in cookies)    # False

   # Iterate
   for name, value in cookies.items():
       print(f"{name}={value}")

   # Output
   print(cookies.to_cookie_header())
   # "session=initial; user=john; token=xyz123; lang=en; theme=dark"

   print(cookies.to_dict())
   # {'session': 'initial', 'user': 'john', 'token': 'xyz123', 'lang': 'en', 'theme': 'dark'}

   # Remove and clear
   cookies.remove('theme', 'lang')
   print(len(cookies))  # 3

   cookies.clear()
   print(len(cookies))  # 0