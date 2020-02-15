"""Server for production purposes."""

__author__ = "Ben Lafferty"
__version__ = "1.0"

from oracli_api import app
import os
import sys

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
