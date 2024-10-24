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

class EventContextManager:

    def __init__(self, _event):
        self._event = _event
    
    def __enter__(self):
        self._event.wait()
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._event.clear()
