import time

gPossibleStates = {}

def minimax(state, is_maximizing):
    if (score := evaluate(state, is_maximizing)) is not None:
        return score
    
    return (max if is_maximizing else min) ( minimax(new_state, not is_maximizing) for new_state in possible_new_states(state) )
    
def best_move(state):
    return max( (minimax(new_state, False), new_state) 
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

def evaluate(state, is_maximizing):
    if not any(state):
        return 1 if is_maximizing else -1
