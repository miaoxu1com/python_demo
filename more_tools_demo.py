from more_itertools import chunked
from more_itertools import flatten

iterable = [(0, 1), (2, 3)]
print(list(flatten(iterable)))
iterable = [0, 1, 2, 3, 4, 5, 6, 7, 8]
print(list(chunked(iterable, 3)))
