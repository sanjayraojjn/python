import random
import re

from minimax_nim import best_move
from args import parse_args

def game(starting_player):
    state = (random.randint(3, 50), )
    state = (10, )
    
    reg = re.compile("^\d+\s\d+$")

    if starting_player == "random":
        computer = random.choice([False, True])
    elif starting_player == "computer":
        computer = True
    else:
        computer = False

    while any([pile > 2 for pile in state]):
        print(f"Current State: ", end='')
        for i, p in enumerate(state):
            print(f"[{i+1}]{p}", end=", ")
        print()
        if computer:
            score, new_state = best_move(state)
            #move = state - new_state
            computer = 0
            print(f"Computer played. {state} -> {new_state}")
            state = new_state
        else:
            while True:
                ##### TODO input two int and verify first
                move = input(f"your call (pile counter)")
                if not reg.match(move):
                    print("wrong input, enter in #pile #count form")
                    continue
                matches = move.strip().split()
                pile, counter = int(matches[0]), int(matches[1])

                num_piles = len(state)
                if pile > len(state):
                    print(f"wrong input, #pile cannot be more than {num_piles}")
                    continue
                if state[pile-1] < 3:
                    print(f"pile#{pile} cannot be splitted")
                    continue
                if counter >= state[pile-1] - 1:
                    print(f"wrong input, cannot split {counter} counters from pile#{pile}(length={state[pile-1]}).")
                    continue
                break
            print(f"your move {pile} {counter}")
            computer = True
            state = state[0:pile-1] + (counter, ) + (state[pile-1] - counter, ) + state[pile:]
    
    if computer:
        print(f"You win. Computer cannot split anymore. \N{party popper}")
    else:
        print(f"Computer wins, you lose. \U0001F641")
        

if __name__ == "__main__":
    args = parse_args()
    game(args.starting_player)



