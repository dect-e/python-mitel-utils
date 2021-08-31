python-mitel-utils
==================

Some quick-and-dirty utility scripts that utilise the `python-mitel` API
wrapper.

These scripts have been written for very specific use cases and only cleaned up
rudimentarily. Inspect before use, use with caution, think thrice and hard
before using them on a production system. You have been warned.

Their purpose is usually summarised in commit messages and/or file headers,
their commandline options (if any) should be apparent from their use of
`argparse` or `sys.argv`.

Usage
-----

Make sure to set `PYTHONPATH=./python-mitel` if you're running these scripts
from the repository directory and haven't installed n-st's version of
python-mitel in your global/user Python path.

Everything is intended to be used with Python 3, usually somewhere around 3.7.
