# File: video.py
# A simple realization of video


class Video:

    def __init__(self, idn, size):
        self.id = idn
        self.size = size

    def __str__(self):
        v = vars(self)
        line = ", ".join([key + " = " + str(v[key]) for key in v])
        return "{0}({1})".format(str(__class__.__name__), line)

    def __repr__(self):
        return str(self)