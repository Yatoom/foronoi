from itertools import groupby
from pprint import pprint


class Tell:
    @staticmethod
    def print(verbose, *text, sep=' ', end='\n', file=None):
        if not verbose:
            return
        print(*text, sep=sep, end=end, file=file)

    @staticmethod
    def print_queue(event_queue, verbose):
        if not verbose:
            return
        print("Printing Queue, grouped by y (warning: expensive calculation!)")
        r = []
        while not event_queue.empty():
            r.append(event_queue.get())
        for i in r:
            event_queue.put(i)
        pprint([list(v) for l, v in groupby(r, lambda item: item.y)])
