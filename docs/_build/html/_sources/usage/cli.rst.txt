======================
Command Line Interface
======================

**pyheaderparse** provides a command-line interface for quick header and cookie parsing.

Installation
------------

The CLI is automatically installed when you install the package:

.. code-block:: bash

   pip install pyheaderparse

Verify installation:

.. code-block:: bash

   $ pyheaderparse --version
   pyheaderparse 1.0.0

   $ pyheaderparse --help

General Usage
-------------

.. code-block:: text

   pyheaderparse <command> [options]

Available Commands
~~~~~~~~~~~~~~~~~~

* ``parse`` - Parse HTTP headers
* ``cookies`` - Parse cookies
* ``info`` - Show header metadata/info

Global Options
~~~~~~~~~~~~~~

* ``-v, --version`` - Show version
* ``-h, --help`` - Show help

Parse Command
-------------

Parse HTTP headers from a file or stdin.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Parse from file
   $ pyheaderparse parse -f headers.txt

   # Parse from stdin
   $ cat headers.txt | pyheaderparse parse --stdin

   # Parse inline data
   $ pyheaderparse parse "content-type: application/json"

Options
~~~~~~~

.. code-block:: text

   -f, --file FILE     Read headers from file
   --stdin             Read headers from stdin
   -H, --header NAME   Get specific header only
   -F, --format FORMAT Output format: json (default), raw, repr

Examples
~~~~~~~~

**Parse all headers (JSON output):**

.. code-block:: bash

   $ pyheaderparse parse -f headers.txt

.. code-block:: json

   {
     "content-type": {
       "value": "application/json",
       "params": {}
     },
     "content-length": 1024,
     "user-agent": "Mozilla/5.0",
     "accept": [
       {"type": "*/*", "q": 1.0}
     ],
     "dnt": true
   }

**Get specific header:**

.. code-block:: bash

   $ pyheaderparse parse -f headers.txt --header user-agent
   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0"

   $ pyheaderparse parse -f headers.txt --header content-length
   1024

   $ pyheaderparse parse -f headers.txt --header accept
   [{"type": "*/*", "q": 1.0}]

**Raw output format:**

.. code-block:: bash

   $ pyheaderparse parse -f headers.txt --format raw
   content-type: application/json
   content-length: 1024
   user-agent: Mozilla/5.0
   accept: [{'type': '*/*', 'q': 1.0}]
   dnt: True

**From stdin:**

.. code-block:: bash

   $ echo -e "content-type: text/html\naccept: */*" | pyheaderparse parse --stdin
   {
     "content-type": {
       "value": "text/html",
       "params": {}
     },
     "accept": [
       {"type": "*/*", "q": 1.0}
     ]
   }

**From clipboard (with xclip on Linux):**

.. code-block:: bash

   $ xclip -selection clipboard -o | pyheaderparse parse --stdin

Cookies Command
---------------

Parse cookies from header data or cookie files.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   # Parse from full headers file
   $ pyheaderparse cookies -f headers.txt --full-headers

   # Parse from cookie-only file
   $ pyheaderparse cookies -f cookies.txt

Options
~~~~~~~

.. code-block:: text

   -f, --file FILE     Read from file
   --stdin             Read from stdin
   --full-headers      Input is full headers (not just cookies)
   --as-header         Output as Cookie header format
   -c, --cookie NAME   Get specific cookie only
   -F, --format FORMAT Output format: json (default), raw, repr

Examples
~~~~~~~~

**Parse cookies from headers file:**

.. code-block:: bash

   $ pyheaderparse cookies -f headers.txt --full-headers

.. code-block:: json

   {
     "session": "abc123",
     "user": "john",
     "token": "xyz789",
     "csrf": "a9a6c92dc170"
   }

**Output as Cookie header format:**

.. code-block:: bash

   $ pyheaderparse cookies -f headers.txt --full-headers --as-header
   session=abc123; user=john; token=xyz789; csrf=a9a6c92dc170

**Get specific cookie:**

.. code-block:: bash

   $ pyheaderparse cookies -f headers.txt --full-headers -c session
   abc123

   $ pyheaderparse cookies -f headers.txt --full-headers -c user
   john

**Parse cookie-only file:**

If your file contains only cookie lines:

.. code-block:: text

   # cookies.txt
   cookie: session=abc123
   cookie: user=john

.. code-block:: bash

   $ pyheaderparse cookies -f cookies.txt
   {
     "session": "abc123",
     "user": "john"
   }

**Parse single-line cookies:**

.. code-block:: bash

   $ echo "cookie: a=1; b=2; c=3" | pyheaderparse cookies --stdin
   {
     "a": "1",
     "b": "2",
     "c": "3"
   }

Info Command
------------

Display metadata and information about headers.

Basic Usage
~~~~~~~~~~~

.. code-block:: bash

   $ pyheaderparse info -f headers.txt

Options
~~~~~~~

.. code-block:: text

   -f, --file FILE     Read from file
   --stdin             Read from stdin
   -F, --format FORMAT Output format: json (default), raw, repr

Example Output
~~~~~~~~~~~~~~

.. code-block:: bash

   $ pyheaderparse info -f headers.txt

.. code-block:: json

   {
     "total_headers": 15,
     "total_cookies": 4,
     "content_type": "application/json",
     "content_length": 1171,
     "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0",
     "origin": "https://medium.com",
     "is_cors": true,
     "sec_fetch": {
       "site": "same-origin",
       "mode": "cors",
       "dest": "empty",
       "user": ""
     },
     "client_hints": {
       "sec-ch-ua": [
         {"brand": "Chrome", "version": "144"},
         {"brand": "Not A Brand", "version": "8"}
       ],
       "sec-ch-ua-mobile": false,
       "sec-ch-ua-platform": "Windows",
       "sec-ch-ua-arch": "x86",
       "sec-ch-ua-bitness": "64"
     }
   }

Sample Headers File
-------------------

Create a sample ``headers.txt`` file for testing:

.. code-block:: text

   content-length: 1171
   content-type: application/json
   user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/144.0.0.0
   accept: */*
   accept-language: en-US,en;q=0.9
   accept-encoding: gzip, deflate, br
   cache-control: max-age=3600, public
   dnt: 1
   sec-ch-ua: "Chrome";v="144", "Not A Brand";v="8"
   sec-ch-ua-mobile: ?0
   sec-ch-ua-platform: "Windows"
   sec-fetch-site: same-origin
   sec-fetch-mode: cors
   sec-fetch-dest: empty
   origin: https://example.com
   referer: https://example.com/page
   cookie: session=abc123
   cookie: user=john
   cookie: token=xyz789

Piping and Scripting
--------------------

The CLI works well in shell pipelines:

**Extract specific values:**

.. code-block:: bash

   # Get just the user-agent string
   $ pyheaderparse parse -f headers.txt -H user-agent -F raw

   # Count cookies
   $ pyheaderparse cookies -f headers.txt --full-headers | jq 'keys | length'

**Use with curl:**

.. code-block:: bash

   # Save response headers
   $ curl -sI https://example.com > response_headers.txt

   # Parse them
   $ pyheaderparse parse -f response_headers.txt

**Use with httpie:**

.. code-block:: bash

   # Get headers from httpie
   $ http --print=h GET https://httpbin.org/get > headers.txt
   $ pyheaderparse info -f headers.txt

**Process multiple files:**

.. code-block:: bash

   # Parse multiple header files
   $ for f in *.headers; do
       echo "=== $f ==="
       pyheaderparse parse -f "$f" -H content-type
   done

Exit Codes
----------

* ``0`` - Success
* ``1`` - Error (file not found, invalid input, etc.)

.. code-block:: bash

   $ pyheaderparse parse -f nonexistent.txt
   Error: File 'nonexistent.txt' not found

   $ echo $?
   1