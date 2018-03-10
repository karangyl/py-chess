import collections


def flatten(l):
    if isinstance(l, collections.Iterable):
        return [item for sublist in l for item in flatten(sublist)]
    else:
        return l


def check_within_board(tup):
    return check_dim_valid(tup[0]) and check_dim_valid(tup[1])


def check_dim_valid(dim):
    return 0 <= dim <= 8


def filter_within_board_moves(l):
    return filter(check_within_board, l)