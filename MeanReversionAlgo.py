import numpy as np

def initialize(context):
    
    context.jj = sid(4151)
    schedule_function(check_band,date_rules.every_day())
    
    
def check_band(context,data):
    
    jj = context.jj
    
    prices = data.history(jj,'price',20,'1d')
    mavg_20 = np.mean(prices)
    std_20 = np.std(prices)
    
    if data.current(jj,'price') >= (mavg_20 + 2 * std_20):
        order_target_percent(jj,-1)
        print('Shorting')
    elif data.current(jj,'price') <= (mavg_20 - 2 * std_20):
        order_target_percent(jj,1)
        print('Buying')
    else:
        pass
    
    record(upper=(mavg_20 + 2 * std_20),lower=(mavg_20 - 2 * std_20),average=mavg_20,
           price=data.current(jj,'price'))
