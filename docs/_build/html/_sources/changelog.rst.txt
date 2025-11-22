=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[1.0.0] - 2025-01-XX
--------------------

Initial release of **pyheaderparse**.

Added
~~~~~

**Core Features**

* ``HeaderParser`` class for parsing HTTP headers
* ``CookieParser`` class for parsing cookies
* ``HeaderValue`` dataclass for parameterized headers
* Full kwargs support for creating and modifying headers/cookies
* Automatic underscore-to-hyphen conversion in kwargs
* Method chaining support for fluent API
* Case-insensitive header access

**Header Parsing**

* Parse raw header strings and bytes
* Parse Content-Type with parameters
* Parse Accept headers with quality values
* Parse Accept-Language with quality values
* Parse Accept-Encoding as list
* Parse Cache-Control as dictionary
* Parse boolean headers (DNT, Sec-GPC)
* Parse Client Hints (Sec-CH-UA-*)
* Parse Sec-Fetch metadata headers
* Parse Priority header
* Automatic Content-Length to integer conversion

**Cookie Features**

* Parse multiple cookie lines
* Parse single-line semicolon-separated cookies
* ``to_cookie_header()`` - export as Cookie header string
* ``to_dict()`` - export as dictionary
* Full CRUD operations (set, get, remove, clear)

**Export Methods**

* ``to_dict()`` - export headers as dictionary
* ``to_dict(stringify=True)`` - export with string values
* ``to_raw()`` - export as raw header format
* ``to_requests_headers()`` - export for requests library

**Factory Methods**

* ``from_dict()`` - create from dictionary
* ``from_kwargs()`` - create from kwargs
* ``from_requests_response()`` - create from requests Response

**Utility Methods**

* ``is_cors()`` - check if CORS request
* ``is_ajax()`` - check if AJAX request
* ``get_client_hints()`` - get all Sec-CH-* headers
* ``get_sec_fetch_metadata()`` - get Sec-Fetch-* headers

**CLI**

* ``pyheaderparse parse`` - parse headers
* ``pyheaderparse cookies`` - parse cookies
* ``pyheaderparse info`` - show header metadata
* Multiple output formats (JSON, raw, repr)
* File and stdin input support

**Documentation**

* Comprehensive README
* Full Sphinx documentation
* API reference
* Usage guides
* CLI documentation

**Testing**

* Comprehensive test suite
* pytest integration
* Coverage reporting

[Unreleased]
------------

Planned
~~~~~~~

* Support for Set-Cookie parsing
* HTTP/2 pseudo-headers support
* Header validation
* Custom parser plugins
* Async support