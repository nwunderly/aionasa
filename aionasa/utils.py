from datetime import datetime, date, timedelta


def date_strptime(date_string):
    """Converts a YYYY-MM-DD string into a datetime.date object.

    Equivalent to strptime with format string "%Y-%m-%d".
    Also accepts 'today' and 'yesterday' as shortcuts.

    Parameters
    ----------
    date_string: String to format.

    Returns
    -------
    datetime.date: The converted date.
    """
    keywords = {
        'today': date.today(),
        'yesterday': date.today() - timedelta(days=1)
    }
    if date_string in keywords.keys():
        return keywords[date_string]

    return datetime.strptime(date_string, f'%Y-%m-%d').date()
