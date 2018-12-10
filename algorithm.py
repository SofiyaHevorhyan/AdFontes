import copy
import time

from elements.process_file import process
from knapsack import knapsack
from score_calculator import score_calculator


def choose_next_priority(dc_time):

    max_second = 0
    priority = []
    for end in dc_time:
        max_elem = end[0]
        if max_elem[0] > max_second:
            priority.append(max_elem)  # time, id of video, endpoint
            end.pop(0)

        if end and end[0][0] > max_second:
            max_second = end[0][0]

    return priority


def request_to_cash(system, priority, endpoints, cashes, videos):

    to_cash = {el: [] for el in range(system.num_cashes)}
    possible_ways = {el: [] for el in priority}
    num = len(priority)

    for i in range(num):
        end_video = priority[i]
        endpoint = endpoints[end_video[2]]
        video = videos[end_video[1]]

        indicator = False
        for j in range(endpoint.num_cashes):
            cash_id = endpoint.cashes[j][0]

            if cashes[cash_id].capacity >= video.size:
                possible_ways[end_video].append(cash_id)
                if not indicator:
                    to_cash[cash_id].append(end_video)  # each video from end to its best cash
                    indicator = True

    ways2 = copy.deepcopy(possible_ways)
    for el in ways2:
        if not ways2[el]:
            del possible_ways[el]

    return to_cash, possible_ways


def resolve_collisions(to_cash, ways, cashes, videos):

    for key in to_cash:
        cash = cashes[key]
        if len(to_cash[key]) == 1:
            if cash.capacity >= videos[to_cash[key][0][1]].size:
                video = videos[to_cash[key][0][1]]
                cash.capacity -= video.size
                cash.put_video(video.id)
                if to_cash[key][0] in ways:
                    del ways[to_cash[key][0]]
            else:
                to_cash[key] = []
                update_to_cash(to_cash, ways)
        elif len(to_cash[key]) > 1:

            video_put = to_cash[key]
            num_videos = len(videos)

            data = {i: [0, videos[i].size, i] for i in range(num_videos)}
            for i in range(num_videos):
                data[i][0] += sum([el[0] for el in video_put if el[1] == i])

            values = list(data.values())
            values = [el for el in values if el[0]]
            total_value, result_items = knapsack(values,
                                                 cash.capacity)
            sizes = [videos[el].size for el in result_items]
            for el, size in zip(result_items, sizes):
                cash.capacity -= size
                cash.put_video(el)

            new_video_put = []
            for el in video_put:
                if el[1] not in result_items:
                    new_video_put.append(el)
            to_cash[key] = new_video_put

            if not result_items:
                ways = {}

            ways2 = copy.deepcopy(ways)
            for el in ways2:
                if el[1] in result_items or len(ways[el]) == 1:
                    del ways[el]
                else:
                    ways[el].pop(0)
    return to_cash, ways


def update_to_cash(to_cash, ways):
    for el in ways:
        to_cash[ways[el][0]].append(el)

    return to_cash


def main(name):

    system, endpoints, cashes, videos = process(name)

    dc_time = []  # time to dc for all requests for all videos from diff end-s
    for i in range(system.num_endpoints):
        if endpoints[i].num_cashes > 0:
            dc_time.append(endpoints[i].time_to_dc())

    while dc_time:
        priority = choose_next_priority(dc_time)
        dc_time = [el for el in dc_time if el]

        to_cash, ways = request_to_cash(system, priority, endpoints, cashes, videos)
        while ways:
            to_cash, ways = resolve_collisions(to_cash, ways, cashes, videos)

    score = score_calculator(system, endpoints, cashes)
    print(score)
    return score


if __name__ == "__main__":
    files = [r"datasets\example.in", r"datasets\me_at_the_zoo.in",
             r"datasets\videos_worth_spreading.in", r"datasets\kittens.in",
             r"datasets\trending_today.in"]
    score = 0
    for el in files:
        start = time.time()
        score += main(el)
        end = time.time() - start
        print("time", end)

    print(score)
