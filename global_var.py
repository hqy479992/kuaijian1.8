def _init():
    global _global_dict
    _global_dict = {}

def set_val(key, value):
    _global_dict[key] = value

def get_val(key):
    try:
        return  _global_dict[key]
    except KeyError:
        return None

_init()
set_val("processed_length", 0)
set_val("total_length", 1)