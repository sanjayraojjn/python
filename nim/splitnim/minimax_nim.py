import time

gPossibleStates = {}

def minimax(state, is_maximizing):
    #print(f"state: {state}")
    if (score := evaluate(state, is_maximizing)) is not None:
        return score
    
    #print(f"state: {state}")
    return (max if is_maximizing else min) ( minimax(new_state, not is_maximizing) for new_state in possible_new_states(state) )
    
def best_move(state):
    return max( (minimax(new_state, False), new_state) 
               for  new_state in possible_new_states(state))

def possible_new_states(state):    
    result = []
    for idx, pile in enumerate(state):
        if pile > 2:
            for num in range(1, int((pile+1)/2)):
                    #print(state[0: idx] + [num, ] + state[idx+1: ])
                    #time.sleep(5)
                    result.append ( state[0: idx] + (num, ) + (pile-num, ) + state[idx+1: ] )
    gPossibleStates[state] = result
    return result
    #return [for pile in piles]
    #return [state - take for take in (1,2,3) if state >= take]

def evaluate(state, is_maximizing):
    splittable_piles = [pile for pile in state if pile > 2]
    if not splittable_piles:
        return 1 if is_maximizing else -1
