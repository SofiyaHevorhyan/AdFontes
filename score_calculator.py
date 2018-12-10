# File: score_calculator.py
# A simple program for calculating the score for streaming videos


def score_calculator(system, endpoints, cashes):

    score = 0

    for endpoint in endpoints:

        for req in endpoint.request:

            for cash in endpoint.cashes:
                real_cash = cashes[cash[0]]
                if req[0] in real_cash.save_video:
                    score += req[1]*(endpoint.dc_latency - cash[1])
                    break

    return score*1000/system.num_requests
