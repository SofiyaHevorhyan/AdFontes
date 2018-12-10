# File: process_file.py
#

from elements.cash import Cash
from elements.endpoint import Endpoint
from elements.system import System
from elements.videos import Video


def read_line(file):
    data = file.readline().split()
    return [int(el) for el in data]


def process(name):

    with open(name, "r") as f:
        elem_info = read_line(f)
        videos_info = read_line(f)

        system = System(elem_info)

        cash_capacity = elem_info[4]
        cashes = [Cash(i, cash_capacity) for i in range(system.num_cashes)]
        videos = [Video(i, videos_info[i]) for i in range(system.num_videos)]

        endpoints = []
        for i in range(system.num_endpoints):
            data = read_line(f)

            endpoint = Endpoint(i, data)
            endpoints.append(endpoint)

            for j in range(endpoint.num_cashes):
                data = read_line(f)  # (cash, speed)
                id_cash, speed = data[0], data[1]

                cashes[id_cash].add_endpoint(endpoint, speed)
                endpoint.add_cash(cashes[id_cash].id, speed)

            endpoint.cashes.sort(key=lambda x: x[1])

        for i in range(system.num_requests):
            data = read_line(f)
            endpoints[data[1]].add_request(videos[data[0]].id, data[2])

        for end in endpoints:
            end.request = list(end.request.items())
            end.request.sort(key=lambda x: x[1], reverse=True)

    return system, endpoints, cashes, videos
