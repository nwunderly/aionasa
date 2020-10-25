
import datetime

from ..errors import *


class EarthImage:
    """A NASA EPIC image asset.

    """
    def __init__(self, client, url):
        self.client = client
        self.url = url
