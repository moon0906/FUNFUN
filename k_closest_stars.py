import functools
import math

from test_framework import generic_test
from test_framework.test_utils import enable_executor_hook
import heapq


class Star:
    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z

    @property
    def distance(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def __lt__(self, rhs):
        return self.distance < rhs.distance

    def __repr__(self):
        return str(self.distance)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, rhs):
        return math.isclose(self.distance, rhs.distance)


def find_closest_k_stars(stars, k):
    min_heap = []
    for i in range(k):
        star = next(stars)
        heapq.heappush(min_heap, (-star.distance, star))
    star = next(stars, None)
    while star is not None:
        heapq.heappush(min_heap, (-star.distance, star))
        heapq.heappop(min_heap)
        star = next(stars, None)
    return [s[1] for s in min_heap]


def comp(expected_output, output):
    if len(output) != len(expected_output):
        return False
    return all(
        math.isclose(s.distance, d)
        for s, d in zip(sorted(output), expected_output))


@enable_executor_hook
def find_closest_k_stars_wrapper(executor, stars, k):
    stars = [Star(*a) for a in stars]
    return executor.run(
        functools.partial(find_closest_k_stars, iter(stars), k))


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main("k_closest_stars.py",
                                       "k_closest_stars.tsv",
                                       find_closest_k_stars_wrapper, comp))