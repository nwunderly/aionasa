
import datetime

from ..errors import *


class EarthImage:
    """A NASA EPIC image asset.

    """
    def __init__(self, client, url, **kwargs):
        self.client = client
        self.url = url

        for key, value in kwargs.items():
            setattr(self, key, value)
            #hello



