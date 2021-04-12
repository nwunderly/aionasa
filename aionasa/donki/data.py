class CME:
    """A solar coronal mass ejection event.

    Attributes
    ----------
    activity_id
    start_time
    source_location
    active_region_num
    instruments
    cme_analyses
    linked_events
    note
    catalog
    """
    def __init__(self, data):
        self.data = data
        self.activity_id = data['activityID']
        self.start_time = data['startTime']
        self.source_location = data['sourceLocation']
        self.active_region_num = data['activeRegionNum']
        self.instruments = data['instruments']
        self.cme_analyses = data['cmeAnalyses']
        self.linked_events = data['linkedEvents']
        self.note = data['note']
        self.catalog = data['catalog']


class CMEAnalysis:
    """A coronal mass ejection analysis.

    Attributes
    ----------
    time21_5
    latitude
    longitude
    half_angle
    speed
    type
    is_most_accurate
    associated_cme_id
    note
    catalog
    """
    def __init__(self, data):
        self.data = data
        self.time21_5 = data['time21_5']
        self.latitude = data['latitude']
        self.longitude = data['longitude']
        self.half_angle = data['halfAngle']
        self.speed = data['speed']
        self.type = data['type']
        self.is_most_accurate = data['isMostAccurate']
        self.associated_cme_id = data['associatedCMEID']
        self.note = data['note']
        self.catalog = data['catalog']


class GMS:
    """A geomagnetic storm event.

    Attributes
    ----------
    gst_id
    start_time
    all_kp_index
    linked_events
    """
    def __init__(self, data):
        self.data = data
        self.gst_id = data['gstID']
        self.start_time = data['start_time']
        self.all_kp_index = data['allKpIndex']
        self.linked_events = data['linkedEvents']


class IPS:
    """An interplanetary shock event.

    Attributes
    ----------
    catalog
    activity_id
    location
    event_time
    instruments
    """
    def __init__(self, data):
        self.data = data
        self.catalog = data['catalog']
        self.activity_id = data['activityID']
        self.location = data['location']
        self.event_time = data['eventTime']
        self.instruments = data['instruments']


class FLR:
    """A solar flare event.

    Attributes
    ----------
    flr_id
    instrument
    begin_time
    peak_time
    end_time
    class_type
    source_location
    active_region_num
    linked_events
    """
    def __init__(self, data):
        self.data = data
        self.flr_id = data['flrID']
        self.instrument = data['instrument']
        self.begin_time = data['beginTime']
        self.peak_time = data['peakTime']
        self.end_time = data['endTime']
        self.class_type = data['classType']
        self.source_location = data['sourceLocation']
        self.active_region_num = data['activeRegionNum']
        self.linked_events = data['linkedEvents']


class SEP:
    """A solar energy particle event.

    Attributes
    ----------
    sep_id
    event_time
    instruments
    linked_events
    """
    def __init__(self, data):
        self.data = data
        self.sep_id = data['sepID']
        self.event_time = data['eventTime']
        self.instruments = data['instruments']
        self.linked_events = data['linkedEvents']


class MPC:
    """A magnetopause crossing event.

    Attributes
    ----------
    mpc_id
    event_time
    instruments
    linked_events
    """
    def __init__(self, data):
        self.data = data
        self.mpc_id = data['mpcID']
        self.event_time = data['eventTime']
        self.instruments = data['instruments']
        self.linked_events = data['linkedEvents']


class RBE:
    """A radiation belt enhancement event.

    Attributes
    ----------
    rbe_id
    event_time
    instruments
    linked_events
    """
    def __init__(self, data):
        self.data = data
        self.rbe_id = data['rbeID']
        self.event_time = data['eventTime']
        self.instruments = data['instruments']
        self.linked_events = data['linkedEvents']


class HSS:
    """A high speed stream event.

    Attributes
    ----------
    hss_id
    event_time
    instruments
    linked_events
    """
    def __init__(self, data):
        self.data = data
        self.hss_id = data['hssID']
        self.event_time = data['eventTime']
        self.instruments = data['instruments']
        self.linked_events = data['linkedEvents']


class WSAEnlilSim:
    """A WSA-Enlil simulation event.

    Attributes
    ----------
    simulation_id
    model_completion_time
    au
    cme_inputs
    estimated_shock_arrival_time
    estimated_duration
    rmin_re
    kp_18
    kp_90
    kp_135
    kp_180
    is_earth_gb
    impact_list
    """
    def __init__(self, data):
        self.data = data
        self.simulation_id = data['simulationID']
        self.model_completion_time = data['modelCompletionTime']
        self.au = data['au']
        self.cme_inputs = data['cmeInputs']
        self.estimated_shock_arrival_time = data['estimatedShockArrivalTime']
        self.estimated_duration = data['estimatedDuration']
        self.rmin_re = data['rmin_re']
        self.kp_18 = data['kp_18']
        self.kp_90 = data['kp_90']
        self.kp_135 = data['kp_135']
        self.kp_180 = data['kp_180']
        self.is_earth_gb = data['isEarthGB']
        self.impact_list = data['impactList']


class Notification:
    """A DONKI space weather notification.

    Attributes
    ----------
    message_type
    message_id
    message_url
    message_issue_time
    message_body
    """
    def __init__(self, data):
        self.data = data
        self.message_type = data['messageType']
        self.message_id = data['messageID']
        self.message_url = data['messageURL']
        self.message_issue_time = data['messageIssueTime']
        self.message_body = data['messageBody']
