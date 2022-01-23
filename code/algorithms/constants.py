def get_constants(scale):
    """ 
    Determine constants based on the scale
    """ 
    if scale == 'Holland':
        MAX_TIME = 120
        MAX_ROUTES = 7
    elif scale == 'Nationaal': 
        MAX_TIME = 180
        MAX_ROUTES = 20
    
    return MAX_TIME, MAX_ROUTES