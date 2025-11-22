============
Installation
============

Requirements
------------

* Python 3.8 or higher
* No external dependencies required

Install from PyPI
-----------------

The recommended way to install **pyheaderparse** is via pip:

.. code-block:: bash

   pip install pyheaderparse

Install with Development Dependencies
-------------------------------------

If you want to contribute or run tests:

.. code-block:: bash

   pip install pyheaderparse[dev]

This will install additional packages:

* ``pytest`` - Testing framework
* ``pytest-cov`` - Coverage reporting
* ``black`` - Code formatting
* ``mypy`` - Type checking
* ``ruff`` - Linting

Install from Source
-------------------

You can also install directly from the GitHub repository:

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/cumulus13/pyheaderparse.git
   cd pyheaderparse

   # Install in development mode
   pip install -e .

   # Or install with dev dependencies
   pip install -e ".[dev]"

Install Specific Version
------------------------

.. code-block:: bash

   # Install specific version
   pip install pyheaderparse==1.0.0

   # Install minimum version
   pip install "pyheaderparse>=1.0.0"

Verify Installation
-------------------

After installation, verify it works:

.. code-block:: python

   >>> from parser_header import HeaderParser, CookieParser
   >>> print(HeaderParser.__module__)
   parser_header.parser

Or via CLI:

.. code-block:: bash

   $ pyheaderparse --version
   pyheaderparse 1.0.0

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade pyheaderparse

Uninstalling
------------

To remove the package:

.. code-block:: bash

   pip uninstall pyheaderparse