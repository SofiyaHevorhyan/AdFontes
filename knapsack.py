def knapsack(items, weight):
    """
    :param items: the array of elements [(value, weight), (...)...]
    :param weight: max weight to be packed
    :return: total value of packed items, result items - list of indexes
    """
    n = len(items)
    two_row = [[0] * (weight + 1), []]

    # to make sure there will be no repetitions in keys
    two_dicts = [dict(), dict()]
    two_dicts[0][0] = []

    # the index of row and dict that we now work with
    index = 1

    for i in range(n):
        current_item = items[i]
        v, w, index_dict = current_item[0], current_item[1], current_item[2]

        work_row = two_row[index]
        prev_row = two_row[index - 1]
        work_dict = two_dicts[index]
        prev_dict = two_dicts[index - 1]

        for j in range(weight + 1):

            if j < w:

                value = prev_row[j]
                work_row.append(value)
                if value not in work_dict:
                    work_dict[value] = prev_dict[value]

            else:
                # lot's of values for optimization
                value1 = prev_row[j]
                value2 = prev_row[j-w]
                value3 = value2 + v

                if value1 > value3:
                    work_row.append(value1)

                    if value1 not in work_dict:
                        work_dict[value1] = prev_dict[value1]

                else:
                    work_row.append(value3)

                    if value3 not in work_dict:
                        work_dict[value3] = prev_dict[value2] + [index_dict]

        index = 0 if index else 1
        two_row[index] = []
        two_dicts[index] = dict()

    total = two_row[index - 1][-1]

    return total, two_dicts[index - 1][total]
