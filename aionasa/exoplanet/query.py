"""
To anyone reading this:
    I'm sorry.
"""


class _QueryString:
    def __init__(self, string):
        self.str = string

    def __bool__(self):
        return True

    def __str__(self):
        return self.str

    def __repr__(self):
        return f"QueryString('{self}')"

    def __and__(self, other):
        return _QueryString(f"{self.str} and {other.str}")

    def __or__(self, other):
        return _QueryString(f"{self.str} or {other.str}")

    def __add__(self, other):
        return _QueryString(self.str + ',' + str(other))


class _Query:
    def __init__(self, name):
        self.name = name

    def __bool__(self):
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Query('{self}')"

    def __eq__(self, other):
        return _QueryString(f"{self.name}={other}")

    def __gt__(self, other):
        return _QueryString(f"{self.name}>{other}")

    def __lt__(self, other):
        return _QueryString(f"{self.name}<{other}")

    def __ge__(self, other):
        return _QueryString(f"{self.name}>={other}")

    def __le__(self, other):
        return _QueryString(f"{self.name}<={other}")

    def like(self, item):
        return _QueryString(f"{self.name} like {item}")

    def __contains__(self, item):
        return _QueryString(f"{self.name} like {item}")

    def __add__(self, other):
        return _QueryString(self.name + ',' + str(other))


"""
PUT QUERY OPTIONS HERE

ex:
    ra = _Query('ra')
    dec = _Query('dec')
    pl_discmethod = _Query('pl_discmethod')
"""

pl_hostname = _Query('pl_hostname')
ra = _Query("ra")
dec = _Query("dec")


# =====================================================================================================================================================

class _Format:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


csv = _Format('csv')
ipac = _Format('ipac')
bar = _Format('bar')
bar_delimited = _Format('bar_delimited')
pipe = _Format('pipe')
pipe_delimited = _Format('pipe_delimited')
xml = _Format('xml')
vo_table = _Format('vo_table')
json = _Format('json')


# =====================================================================================================================================================

class _Table:  # my god... this is going to be an ugly one.
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name



