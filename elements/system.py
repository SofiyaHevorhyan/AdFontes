# File: system.py
# Altogether


class System:

    def __init__(self, data):
        self.num_videos = data[0]        # num of videos
        self.num_endpoints = data[1]     # num of endpoints
        self.num_requests = data[2]      # num of requests (total)
        self.num_cashes = data[3]        # num of cashes

    def __str__(self):
        v = vars(self)
        line = "\n ".join([key + " = " + str(v[key]) for key in v])
        return "{0}({1})".format(str(__class__.__name__), line)
