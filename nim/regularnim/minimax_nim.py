import time

gPossibleStates = {}

def minimax(state, is_maximizing, last_counter_wins=False):
    if (score := evaluate(state, is_maximizing, last_counter_wins)) is not None:
        return score
    
    #print(f"state: {state}")
    return (max if is_maximizing else min) ( minimax(new_state, not is_maximizing, last_counter_wins) for new_state in possible_new_states(state) )
    
def best_move(state, last_counter_wins=False):
    return max( (minimax(new_state, False, last_counter_wins), new_state) 
               for  new_state in possible_new_states(state))

def possible_new_states(state):
    if state in gPossibleStates:
        return gPossibleStates[state]
    
    result = []
    for idx, pile in enumerate(state):
        if pile > 0:
            for num in range(pile):
                    #print(state[0: idx] + [num, ] + state[idx+1: ])
                    #time.sleep(5)
                    result.append ( state[0: idx] + (num, ) + state[idx+1: ] )
    gPossibleStates[state] = result
    return result
    #return [for pile in piles]
    #return [state - take for take in (1,2,3) if state >= take]

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
