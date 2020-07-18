
import datetime


class AstronomyPicture:
    """
    A class representing a single daily APOD picture.
    """
    def __init__(self, date: datetime.date, **kwargs):
        self.date = date
        self.copyright = kwargs.get('copyright')
        self.title = kwargs.get('title')
        self.explanation = kwargs.get('explanation')
        self.url = kwargs.get('url')
        self.hdurl = kwargs.get('hdurl')
        self.media_type = kwargs.get('media_type')
        self.service_version = kwargs.get('service_version')




