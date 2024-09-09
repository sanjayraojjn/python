import random
import re

from minimax_nim import best_move

def game():
    #num_piles = 2
    #state = (5,2)
    num_piles = random.randint(1,3)
    state = tuple([random.randint(2, 7) for pile in range(num_piles)] )
    
    reg = re.compile("^\d+\s\d+$")

    computer = random.choice([0,1])

    while any(state):
        print(f"Current State: {state}")
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

                if pile > num_piles:
                    print(f"wrong input, #pile cannot be more than {num_piles}")
                    continue
                if not state[pile-1]:
                    print(f"no counter left in pile#{pile}")
                    continue
                if counter > state[pile-1]:
                    print(f"wrong input, #counter cannot be more than {state[pile-1]}")
                    continue
                break
            print(f"your move {pile} {counter}")
            computer = True
            state = state[0:pile-1] + (state[pile-1] - counter, ) + state[pile:]
            #state[pile-1] = state[pile-1] - counter
    
    if computer:
        print(f"Computer wins, you lose. \U0001F641")
    else:
        print(f"You win \N{party popper}")

if __name__ == "__main__":
    game()


