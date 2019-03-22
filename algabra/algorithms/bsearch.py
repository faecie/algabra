import math
import typing


def binary_search(items: typing.Sequence, value: int) -> typing.Optional[int]:
    """
    Classic implementation of Binary Search

    Get a middle point of a list and if the value is greater than searching -
    do the same with a left part or with right part if the value is less

    :param items: MUST be already sorted sequence of integers
    :param value: Is the integer value that we want to find
    :return: The key of the value in the sequence or None if its not in it
    """
    first, last = 0, len(items) - 1
    while last >= first:
        if first == last:
            return first if items[first] == value else None

        middle = last - math.floor((last - first) / 2)

        if items[middle] == value:
            return middle

        if items[middle] < value:
            first = middle
        else:
            last = middle - 1

    return None


def minimum_passes(m, w, p, n):
    steps = 0
    candies = 0
    while candies < n:
        steps_to_increase = math.ceil((p - candies) / (m * w))

        steps_to_reach = math.ceil((n - candies) / (m * w))
        if abs(steps_to_reach - steps_to_increase) <= 1:
            return steps + steps_to_reach
        else:
            steps += steps_to_increase
            candies += m * w * steps_to_increase
            new_units = math.floor(candies / p)
            candies -= p * new_units
            fulfilm = min(w - m, new_units) if m < w else 0
            fulfilw = min(m - w, new_units) if w < m else 0
            new_units -= (fulfilm + fulfilw)
            m += fulfilm + math.floor(new_units / 2)
            w += fulfilw + math.ceil(new_units / 2)

    return steps


# Complete the abbreviation function below.
def abbreviation(a, b):
    pref = [[False] * (len(a) + 1) for _ in range(len(b) + 1)]
    for i in range(len(a) + 1):
        pref[0][i] = True if (i == 0 or a[i - 1].islower()) else False

    for i in range(1, len(pref)):
        for j in range(1, len(pref[i])):
            lettera, letterb = a[j - 1], b[i - 1]
            if lettera.isupper():
                pref[i][j] = pref[i - 1][j - 1] if lettera == letterb else False
            elif letterb == lettera.upper():
                pref[i][j] = pref[i - 1][j - 1] or pref[i][j - 1]
            else:
                pref[i][j] = pref[i][j - 1]

    return 'YES' if pref[i][j] else 'NO'


MIN_CANDIES = 1


# Complete the candies function below.
def candies(rates):
    amounts = [MIN_CANDIES]
    for ix in range(1, len(rates)):
        prev = amounts[ix - 1]
        amounts.append(prev + 1 if rates[ix - 1] < rates[ix] else MIN_CANDIES)
    result = amounts[len(amounts) - 1]
    for ix in range(len(rates) - 2, -1, -1):
        prev = amounts[ix + 1]
        is_higher = rates[ix] > rates[ix + 1]
        amounts[ix] = max(amounts[ix], prev + 1) if is_higher else amounts[ix]
        result += amounts[ix]

    return result
