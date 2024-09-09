import time
from functools import cache

@cache
def minimax(state, is_maximizing):
    #print(f"state: {state}")
    if (score := evaluate(state, is_maximizing)) is not None:
        return score
    
    #print(f"state: {state}")
    return (max if is_maximizing else min) ( minimax(new_state, not is_maximizing) for new_state in possible_new_states(state) )
    
def best_move(state):
    return max( (minimax(new_state, False), new_state) 
               for  new_state in possible_new_states(state))

@cache
def possible_new_states(state):
    result = set([]) #new states are sorted set to avoid traversing duplicate subtrees
    for idx, pile in enumerate(state):
        if pile > 2:
            for num in range(1, int((pile)/2) + 1):
                    new_state = sorted ( state[0: idx] + (num, ) + (pile-num, ) + state[idx+1: ] )
                    result.add ( tuple(new_state) )
    return result

def evaluate(state, is_maximizing):
    splittable_piles = [pile for pile in state if pile > 2]
    if not splittable_piles:
        return 1 if is_maximizing else -1