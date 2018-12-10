# File: cash.py
# A simple realization of cash server


class Cash:

    def __init__(self, idn, capacity):
        self.id = idn
        self.capacity = capacity

        self.endpoints = []    # [ (endpoint, speed), (endpoint, speed)...]
        self.save_video = []

    def add_endpoint(self, endpoint, speed):
        self.endpoints.append((endpoint, speed))

    def put_video(self, id_video):
        self.save_video.append(id_video)

    def __str__(self):
        v = vars(self)
        line = ", ".join([key + " = " + str(v[key]) for key in v if key != "endpoints"])
        return "{0}({1})".format(str(__class__.__name__), line)

    def __repr__(self):
        return str(self)
