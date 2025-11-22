============
Contributing
============

Thank you for your interest in contributing to **pyheaderparse**!

Getting Started
---------------

1. Fork the Repository
~~~~~~~~~~~~~~~~~~~~~~

Fork the repository on GitHub:
https://github.com/cumulus13/pyheaderparse

2. Clone Your Fork
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/YOUR_USERNAME/pyheaderparse.git
   cd pyheaderparse

3. Set Up Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install with dev dependencies
   pip install -e ".[dev]"

4. Create a Branch
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix

Development Workflow
--------------------

Running Tests
~~~~~~~~~~~~~

.. code-block:: bash

   # Run all tests
   pytest

   # Run with coverage
   pytest --cov=parser_header --cov-report=term-missing

   # Run specific test file
   pytest tests/test_parser.py

   # Run specific test
   pytest tests/test_parser.py::TestHeaderParser::test_parse_basic

   # Verbose output
   pytest -v

Code Formatting
~~~~~~~~~~~~~~~

We use ``black`` for code formatting:

.. code-block:: bash

   # Format all code
   black parser_header tests

   # Check formatting without changing
   black --check parser_header tests

Linting
~~~~~~~

We use ``ruff`` for linting:

.. code-block:: bash

   # Run linter
   ruff check parser_header tests

   # Auto-fix issues
   ruff check --fix parser_header tests

Type Checking
~~~~~~~~~~~~~

We use ``mypy`` for type checking:

.. code-block:: bash

   mypy parser_header

Pre-Commit Checklist
~~~~~~~~~~~~~~~~~~~~

Before committing, run:

.. code-block:: bash

   # Format
   black parser_header tests

   # Lint
   ruff check parser_header tests

   # Type check
   mypy parser_header

   # Test
   pytest

Code Style
----------

General Guidelines
~~~~~~~~~~~~~~~~~~

* Follow PEP 8
* Use meaningful variable and function names
* Add docstrings to all public functions and classes
* Keep functions focused and small
* Write tests for new features

Docstring Format
~~~~~~~~~~~~~~~~

We use Google-style docstrings:

.. code-block:: python

   def parse_header(name: str, value: str) -> dict:
       """Parse a single header into structured format.

       Args:
           name: The header name (case-insensitive)
           value: The header value string

       Returns:
           Parsed header value as appropriate type

       Raises:
           InvalidHeaderError: If header format is invalid

       Example:
           >>> parse_header('content-type', 'text/html; charset=utf-8')
           HeaderValue(value='text/html', params={'charset': 'utf-8'})
       """
       pass

Type Hints
~~~~~~~~~~

All public functions should have type hints:

.. code-block:: python

   from typing import Dict, List, Optional, Union, Any

   def get(self, name: str, default: Optional[str] = None) -> Optional[str]:
       ...

   def to_dict(self) -> Dict[str, Any]:
       ...

Testing Guidelines
------------------

Writing Tests
~~~~~~~~~~~~~

* Place tests in ``tests/`` directory
* Name test files ``test_*.py``
* Name test functions ``test_*``
* Use descriptive test names
* Test both success and failure cases

Test Structure
~~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from parser_header import HeaderParser, CookieParser

   class TestHeaderParser:
       """Tests for HeaderParser class."""

       def test_parse_basic(self):
           """Test basic header parsing."""
           parser = HeaderParser("content-type: application/json")
           assert parser.content_type == "application/json"

       def test_parse_empty(self):
           """Test parsing empty input."""
           parser = HeaderParser("")
           assert len(parser) == 0

       def test_set_with_kwargs(self):
           """Test setting headers via kwargs."""
           parser = HeaderParser()
           parser.set(content_type='json', accept='*/*')
           assert parser.content_type == 'json'

       def test_get_missing_with_default(self):
           """Test get() returns default for missing header."""
           parser = HeaderParser()
           assert parser.get('missing', 'default') == 'default'

       def test_bracket_access_raises_keyerror(self):
           """Test bracket access raises KeyError for missing header."""
           parser = HeaderParser()
           with pytest.raises(KeyError):
               _ = parser['nonexistent']

Fixtures
~~~~~~~~

Use pytest fixtures for common setup:

.. code-block:: python

   import pytest

   @pytest.fixture
   def sample_headers():
       return """content-type: application/json
   content-length: 1024
   user-agent: Mozilla/5.0
   cookie: session=abc123
   """

   @pytest.fixture
   def parser(sample_headers):
       return HeaderParser(sample_headers)

   def test_content_type(parser):
       assert parser.content_type == 'application/json'

Submitting Changes
------------------

1. Commit Your Changes
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git add .
   git commit -m "feat: add new feature description"

Use conventional commit messages:

* ``feat:`` New feature
* ``fix:`` Bug fix
* ``docs:`` Documentation changes
* ``test:`` Test changes
* ``refactor:`` Code refactoring
* ``style:`` Formatting changes
* ``chore:`` Maintenance tasks

2. Push to Your Fork
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git push origin feature/your-feature-name

3. Create Pull Request
~~~~~~~~~~~~~~~~~~~~~~

1. Go to GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill in the PR template
5. Submit

Pull Request Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

* Describe what changes you made and why
* Reference any related issues
* Ensure all tests pass
* Update documentation if needed
* Keep PRs focused on a single change

Reporting Issues
----------------

Bug Reports
~~~~~~~~~~~

Include:

* Python version
* pyheaderparse version
* Operating system
* Minimal code to reproduce
* Expected vs actual behavior
* Full error traceback

Feature Requests
~~~~~~~~~~~~~~~~

Include:

* Use case description
* Proposed API/behavior
* Example code showing desired usage

Questions
---------

For questions, please:

1. Check existing documentation
2. Search existing issues
3. Open a new issue with the "question" label

License
-------

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank You!
----------

Your contributions help make pyheaderparse better for everyone. We appreciate your time and effort!