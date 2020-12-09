from datetime import datetime, date, timedelta


def date_strptime(day):
    keywords = {
        'today': date.today(),
        'yesterday': date.today() - timedelta(days=1)
    }
    if day in keywords.keys():
        return keywords[day]

    return datetime.strptime(day, f'%Y-%m-%d').date()
