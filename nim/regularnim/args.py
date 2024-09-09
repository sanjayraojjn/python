import argparse
from typing import NamedTuple


class Args(NamedTuple):
    last_counter_wins: bool
    starting_player: str

def parse_args() -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L",
        dest="last_counter_wins",
        default=False
    )
    parser.add_argument(
        "-S",
        dest="starting_player",
        choices=["computer", "human", "random"],
        default="random"
    )
    args = parser.parse_args()
    print(args)

    return Args(args.last_counter_wins, args.starting_player)
