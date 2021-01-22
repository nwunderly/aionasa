from ..utils import date_strptime
from ..asset import Asset


class RoverManifest:
    """A mars rover mission manifest.

    Attributes
    ----------
    name: :class:`str`
        Name of the rover.
    landing_date: :class:`datetime.date`
        The Earth date that the rover landed on Mars.
    launch_date: :class:`datetime.date`
        The Earth date that the rover was launched.
    status: :class:`str`
        The rover's status.
    max_sol: :class:`int`
        The last Martian sol with available photos.
    max_date: :class:`datetime.date`
        The last Earth date with available photos.
    total_photos: :class:`int`

    """
    def __init__(self, data):
        data = data['photo_manifest']
        self.name = data['name']
        self.landing_date = date_strptime(data['landing_date'])
        self.launch_date = date_strptime(data['launch_date'])
        self.status = data['status']
        self.max_sol = data['max_sol']
        self.max_date = date_strptime(data['max_date'])
        self.total_photos = data['total_photos']
        self.photos = MarsPhotoDate._from_list(data['photos'])


class MarsPhotoDate:
    """A date from a rover's mission manifest.

    Attributes
    ----------
    sol: :class:`int`
        The Martial sol corresponding to this date.
    earth_date: :class:`datetime.date`
        The Earth date corresponding to this date.
    total_photos: :class:`int`
        The total number of photos available from this date.
    cameras: :class:`List[str]`
        List of cameras with available images from this date.
    """
    def __init__(self, data):
        self.sol = data['sol']
        self.earth_date = date_strptime(data['earth_date'])
        self.total_photos = data['total_photos']
        self.cameras = data['cameras']

    @classmethod
    def _from_list(cls, data):
        return [cls(d) for d in data]


class MarsPhoto(Asset):
    """A Mars rover photo.

    Attributes
    ----------
    id: :class:`int`
        The photo id.
    sol: :class:`int`
        The Martian sol that the photo was taken.
    earth_date: :class:`datetime.date`
        The Earth date that the photo was taken.
    camera: :class:`RoverCamera`
        The camera that took the photo.
    img_src: :class:`str`
        URL where the photo can be found.
    rover: :class:`Rover`
        The rover that took this photo.
    """
    def __init__(self, client, data):
        self.id = data['id']
        self.sol = data['sol']
        self.earth_date = date_strptime(data['earth_date'])
        self.camera = RoverCamera(data['camera'])
        self.img_src = data['img_src']
        self.rover = Rover(data['rover'])

        super().__init__(client, self.img_src, self.img_src.split('/')[-1])

    async def read(self):
        """Downloads the image associated with this MarsPhoto.

        Returns
        -------
        :class:`bytes`
            The image, downloaded from the URL provided by the API.
        """
        return await super().read(self.img_src)

    async def save(self, path=None):
        """Downloads the file associated with this MarsPhoto and saves to the requested path.

        Parameters
        ----------
        path:
            The file path at which to save the file.
            If ``None``, saves the image to the working directory using the filename from the asset url.

        Returns
        -------
        :class:`int`
            The number of bytes written.
        """
        return await super().save(path, self.img_src)


class RoverCamera:
    """A Mars rover camera.

    Attributes
    ----------
    id: :class:`int`
        The camera id.
    name: :class:`str`
        The camera's name, i.e. "MAST"
    rover_id: :class:`int`
        The rover id.
    full_name: :class:`str`
        The camera's full name, i.e. "Mast Camera"
    """
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.rover_id = data['rover_id']
        self.full_name = data['full_name']


class Rover:
    """A Mars rover.

    Attributes
    ----------
    id: :class:`int`
        The rover id.
    name: :class:`str`
        Name of the rover.
    landing_date: :class:`datetime.date`
        The Earth date that the rover landed on Mars.
    launch_date: :class:`datetime.date`
        The Earth date that the rover was launched.
    status: :class:`str`
        The rover's status.
    """
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.landing_date = date_strptime(data['landing_date'])
        self.launch_date = date_strptime(data['launch_date'])
        self.status = data['status']
