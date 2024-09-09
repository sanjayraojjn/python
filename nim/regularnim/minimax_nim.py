import time
from functools import cache

@cache
def minimax(state, is_maximizing, last_counter_wins=False):
    if (score := evaluate(state, is_maximizing, last_counter_wins)) is not None:
        return score
    
    #print(f"state: {state}")
    return (max if is_maximizing else min) ( minimax(new_state, not is_maximizing, last_counter_wins) for new_state in possible_new_states(state) )
    
def best_move(state, last_counter_wins=False):
    return max( (minimax(new_state, False, last_counter_wins), new_state) 
               for  new_state in possible_new_states(state))

@cache
def possible_new_states(state):
    result = []
    for idx, pile in enumerate(state):
        if pile > 0:
            for num in range(pile):
                    result.append ( state[0: idx] + (num, ) + state[idx+1: ] )
    return result

def evaluate(state, is_maximizing, last_counter_wins=False):
    if last_counter_wins:
        non_zeros = [s for s in state if s>0]
        #print(f"non-zeros: {non_zeros}")
        if len(non_zeros) == 1 and non_zeros[0] < 4:
            return 1 if is_maximizing else -1
        #other player has already taken the last counter
        if not non_zeros:
            return -1 if is_maximizing else 1
    elif not any(state):
        return 1 if is_maximizing else -1
