from datetime import datetime, date, timedelta


def date_strptime(date_string):
    """Converts a ``YYYY-MM-DD`` string into a datetime.date object.

    Equivalent to strptime with format string ``'%Y-%m-%d'``.
    Also accepts ``'today'`` and ``'yesterday'`` as shortcuts.

    Parameters
    ----------
    date_string: String to format.

    Returns
    -------
    :class:`datetime.date`
        The converted date.
    """
    keywords = {
        'today': date.today(),
        'yesterday': date.today() - timedelta(days=1)
    }
    if date_string in keywords.keys():
        return keywords[date_string]

    return datetime.strptime(date_string, f'%Y-%m-%d').date()


def datetime_strptime(date_string, seconds=False):
    """Converts a ``YYYY-MM-DD HH:MM`` string into a datetime.datetime object.

    Equivalent to strptime with format string ``'%Y-%m-%d %H:%M'``.

    Parameters
    ----------
    date_string: :class:`str`
        String to format.
    seconds: :class:`bool`
        Uses format string ``'%Y-%m-%d %H:%M:%S'`` instead.

    Returns
    -------
    :class:`datetime.datetime`
        The converted datetime.
    """
    if seconds:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.strptime(date_string, '%Y-%m-%d %H:%M')
