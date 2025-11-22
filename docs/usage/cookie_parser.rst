============
CookieParser
============

The ``CookieParser`` class provides dedicated functionality for parsing and manipulating HTTP cookies.

Importing
---------

.. code-block:: python

   from parser_header import CookieParser

Creating a CookieParser
-----------------------

From Raw String (Multiple Lines)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw_cookies = """cookie: nonce=Ofymgy29
   cookie: sz=1490
   cookie: pr=1.25
   cookie: uid=2ca13899eb7a
   cookie: sid=1:KUo/b68Cp0mhPre4OYgcLF
   """

   cookies = CookieParser(raw_cookies)

   print(f"Total cookies: {len(cookies)}")
   # Output: Total cookies: 5

   print(cookies.to_dict())
   # Output:
   # {
   #     'nonce': 'Ofymgy29',
   #     'sz': '1490',
   #     'pr': '1.25',
   #     'uid': '2ca13899eb7a',
   #     'sid': '1:KUo/b68Cp0mhPre4OYgcLF'
   # }

From Single Line (Semicolon-Separated)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   single_line = "cookie: session=abc123; user=john; token=xyz789"

   cookies = CookieParser(single_line)

   print(cookies.to_dict())
   # Output: {'session': 'abc123', 'user': 'john', 'token': 'xyz789'}

From Keyword Arguments
~~~~~~~~~~~~~~~~~~~~~~

Underscores in key names are converted to hyphens:

.. code-block:: python

   cookies = CookieParser(
       session='abc123',
       user_id='12345',
       auth_token='xyz789',
       refresh_token='refresh123'
   )

   print(cookies.to_dict())
   # Output:
   # {
   #     'session': 'abc123',
   #     'user-id': '12345',
   #     'auth-token': 'xyz789',
   #     'refresh-token': 'refresh123'
   # }

   print(cookies.to_cookie_header())
   # Output: session=abc123; user-id=12345; auth-token=xyz789; refresh-token=refresh123

Mixed: Raw + Kwargs
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   raw = "cookie: existing=value"

   cookies = CookieParser(raw, new_cookie='new_value', another='test')

   print(cookies.to_dict())
   # Output:
   # {
   #     'existing': 'value',
   #     'new-cookie': 'new_value',
   #     'another': 'test'
   # }

Factory Methods
~~~~~~~~~~~~~~~

.. code-block:: python

   # From dictionary
   cookies = CookieParser.from_dict({
       'session': 'abc',
       'user': 'john',
       'token': 'xyz'
   })
   print(cookies.to_cookie_header())
   # Output: session=abc; user=john; token=xyz

   # From kwargs
   cookies = CookieParser.from_kwargs(
       session='test123',
       remember_me='true'
   )
   print(cookies.to_cookie_header())
   # Output: session=test123; remember-me=true

Setting Cookies
---------------

Using set() Method
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cookies = CookieParser()

   # Positional arguments
   cookies.set('session', 'abc123')

   # Kwargs only
   cookies.set(user='john', token='xyz')

   # Mixed
   cookies.set('admin', 'true', refresh_token='refresh123')

   print(cookies.to_dict())
   # Output:
   # {
   #     'session': 'abc123',
   #     'user': 'john',
   #     'token': 'xyz',
   #     'admin': 'true',
   #     'refresh-token': 'refresh123'
   # }

Using Bracket Notation
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cookies = CookieParser()

   # Set
   cookies['session'] = 'abc123'
   cookies['user'] = 'john'

   # Get
   print(cookies['session'])  # 'abc123'

   # Delete
   del cookies['user']
   print('user' in cookies)  # False

Using update() Method
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cookies = CookieParser(existing='value')

   # From dict
   cookies.update({'new1': 'val1', 'new2': 'val2'})

   # From kwargs
   cookies.update(new3='val3', new4='val4')

   # Mixed
   cookies.update({'from_dict': 'yes'}, from_kwargs='also_yes')

   print(cookies.keys())
   # Output: ['existing', 'new1', 'new2', 'new3', 'new4', 'from-dict', 'from-kwargs']

Method Chaining
~~~~~~~~~~~~~~~

All mutating methods return ``self`` for chaining:

.. code-block:: python

   cookies = (
       CookieParser()
       .set('session', 'abc')
       .set(user='john')
       .set(token='xyz', admin='false')
       .remove('admin')
   )

   print(cookies.to_cookie_header())
   # Output: session=abc; user=john; token=xyz

Removing and Clearing
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   cookies = CookieParser(a='1', b='2', c='3', d='4')

   # Remove specific cookies
   cookies.remove('a', 'b')
   print(cookies.keys())  # ['c', 'd']

   # Clear all
   cookies.clear()
   print(len(cookies))  # 0

Output Methods
--------------

to_cookie_header()
~~~~~~~~~~~~~~~~~~

Returns cookies formatted as a Cookie header string (semicolon-separated):

.. code-block:: python

   cookies = CookieParser(session='abc', user='john', token='xyz')

   # Basic usage
   header = cookies.to_cookie_header()
   print(header)
   # Output: session=abc; user=john; token=xyz

   # With additional cookies via kwargs
   header = cookies.to_cookie_header(extra='value', another='test')
   print(header)
   # Output: session=abc; user=john; token=xyz; extra=value; another=test

**Use Case: HTTP Request**

.. code-block:: python

   import urllib.request

   cookies = CookieParser(session='abc123', csrf='token456')

   req = urllib.request.Request('https://example.com/api')
   req.add_header('Cookie', cookies.to_cookie_header())

   # Header will be: Cookie: session=abc123; csrf=token456

to_dict()
~~~~~~~~~

Returns cookies as a dictionary:

.. code-block:: python

   cookies = CookieParser(session='abc', user='john')

   # Basic usage
   d = cookies.to_dict()
   print(d)
   # Output: {'session': 'abc', 'user': 'john'}

   # With additional cookies
   d = cookies.to_dict(extra='value')
   print(d)
   # Output: {'session': 'abc', 'user': 'john', 'extra': 'value'}

**Use Case: Requests Library**

.. code-block:: python

   import requests

   cookies = CookieParser(session='abc123', user='john')

   response = requests.get(
       'https://httpbin.org/cookies',
       cookies=cookies.to_dict()
   )
   print(response.json())

Accessing Cookies
-----------------

Individual Access
~~~~~~~~~~~~~~~~~

.. code-block:: python

   cookies = CookieParser(session='abc', user_id='123', auth_token='xyz')

   # get() with default
   print(cookies.get('session'))           # 'abc'
   print(cookies.get('missing', 'N/A'))    # 'N/A'

   # Underscore/hyphen interchangeable
   print(cookies.get('user-id'))     # '123'
   print(cookies.get('user_id'))     # '123' (also works)
   print(cookies.get('auth-token'))  # 'xyz'
   print(cookies.get('auth_token'))  # 'xyz' (also works)

   # Bracket notation
   print(cookies['session'])  # 'abc'

Iteration
~~~~~~~~~

.. code-block:: python

   cookies = CookieParser(session='abc', user='john', token='xyz')

   # Iterate
   for name in cookies:
       print(f"{name}={cookies[name]}")
   # Output:
   # session=abc
   # user=john
   # token=xyz

   # Keys, values, items
   print(cookies.keys())    # ['session', 'user', 'token']
   print(cookies.values())  # ['abc', 'john', 'xyz']
   print(cookies.items())   # [('session', 'abc'), ('user', 'john'), ('token', 'xyz')]

Check Existence
~~~~~~~~~~~~~~~

.. code-block:: python

   cookies = CookieParser(session='abc')

   print('session' in cookies)  # True
   print('missing' in cookies)  # False
   print(len(cookies))          # 1

Parse Method
------------

The ``parse()`` method can be called to parse additional data:

.. code-block:: python

   cookies = CookieParser()

   # Parse raw data
   cookies.parse("cookie: a=1; b=2")
   print(cookies.to_dict())  # {'a': '1', 'b': '2'}

   # Parse with additional kwargs
   cookies.parse("cookie: c=3", d='4', e='5')
   print(cookies.to_dict())  # {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5'}

   # Parse only kwargs (None for data)
   cookies.parse(None, f='6')
   print(cookies.to_dict())  # {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6'}

Complete Example
----------------

.. code-block:: python

   from parser_header import CookieParser

   # Create with initial cookies
   cookies = CookieParser(
       session='initial_session',
       user='john'
   )

   # Add more cookies
   cookies.set(token='xyz123')
   cookies.set(remember_me='true', theme='dark')

   # Update from dict
   cookies.update({'lang': 'en', 'timezone': 'UTC'})

   # Remove unwanted
   cookies.remove('theme')

   # Get results
   print("As Header:")
   print(cookies.to_cookie_header())
   # Output: session=initial_session; user=john; token=xyz123; remember-me=true; lang=en; timezone=UTC

   print("\nAs Dict:")
   print(cookies.to_dict())
   # Output:
   # {
   #     'session': 'initial_session',
   #     'user': 'john',
   #     'token': 'xyz123',
   #     'remember-me': 'true',
   #     'lang': 'en',
   #     'timezone': 'UTC'
   # }

   print(f"\nTotal: {len(cookies)} cookies")
   # Output: Total: 6 cookies