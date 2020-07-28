import numpy as np

def initialize(context):
    schedule_function(check_pairs,date_rules.every_day(),time_rules.market_close(hours=1))
    
    context.aa = sid(45971)
    context.ual = sid(28051)
    
    context.long_on_spread = False
    context.shorting_spread = False
    
def check_pairs(context,data):
    
    aa = context.aa
    ual = context.ual
    
    prices = data.history([aa,ual],'price',30,'1d')

    short_prices = prices.iloc[-1:]
    mavg_1 = np.mean(short_prices[aa]-short_prices[ual])
    
    mavg_30 = np.mean(prices[aa]-prices[ual])
    std_30 = np.std(prices[aa]-prices[ual])
    
    if std_30 > 0:
        zscore = (mavg_1 - mavg_30) / std_30
        
        if zscore > 1.0 and not context.shorting_spread:
            order_target_percent(aa,-.5)
            order_target_percent(ual,.5)
            context.shorting_spread = True
            context.long_on_spread = False
        elif zscore < 1.0 and not context.long_on_spread:
            order_target_percent(aa,.5)
            order_target_percent(ual,-.5)
            context.shorting_spread = False
            context.long_on_spread = True
        elif abs(zscore) < 0.1:
            order_target_percent(aa,0)
            order_target_percent(ual,0)
            context.shorting_spread = False
            context.long_on_spread = False
        
        record(Z_score=zscore)
