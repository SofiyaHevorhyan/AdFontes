# File: endpoint.py
# A simple realization of endpoint


class Endpoint:

    def __init__(self, idn, data):
        self.id = idn
        self.dc_latency = data[0]
        self.num_cashes = data[1]

        self.cashes = []
        self.request = dict()

    def add_cash(self, cash_id, speed):
        self.cashes.append((cash_id, speed))

    def add_request(self, video, num_requests):
        self.request[video] = num_requests
        # self.request.append((video, num_requests))

    def time_to_dc(self):
        time = []
        n_videos = len(self.request)
        for i in range(n_videos):
            time.append((self.dc_latency*self.request[i][1],
                         self.request[i][0], self.id))

        return time

    def __str__(self):
        v = vars(self)
        line = ", ".join([key + " = " + str(v[key]) for key in v])
        return "{0}({1})".format(str(__class__.__name__), line)

    def __repr__(self):
        return str(self)
