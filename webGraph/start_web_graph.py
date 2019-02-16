import trio
import sys

from ._set_up_workers import set_up_workers
from .utils._data_structures import Url


def parse_args(args):
    parsed_args = []
    parsed_args.append(args[0])
    parsed_args.append(int(args[1]))
    parsed_args.append(int(args[2]))
    parsed_args.append(int(args[3]))
    return parsed_args


if __name__ == "__main__":
    if len(sys.argv) != 6:
        raise Exception("Invalid number of arguments")

    args = parse_args(sys.argv[1:])
    url = Url(args[0])
    trio.run(set_up_workers, url, args)






