from time import perf_counter

RANDOM_SEED = 675675

def timer(fn):
    def inner(*args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(*args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        print('\x1B[31m {0} took {1:.8f}s \x1B[0m to execute'.format(fn.__name__, execution_time))
        return to_execute
    
    return inner
