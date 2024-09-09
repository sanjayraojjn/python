import random

from minimax_simplenim import best_move

def game():
    state = random.randint(5, 20)

    computer = random.choice([0,1])

    while state>0:
        if computer:
            score, new_state = best_move(state)
            move = state - new_state
            computer = 0
            print(f"computer move {move}")
        else:
            while True:
                move = int(input(f"enter input(<{state})"))
                if move > state:
                    print("wrong input. Try again.")
                else:
                    break
            print(f"your move {move}")
            computer = True
        state = state - move
    
    if computer:
        print(f"Computer wins, you lose. \U0001F641")
    else:
        print(f"You win \N{party popper}")

if __name__ == "__main__":
    game()


