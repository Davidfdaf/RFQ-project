import pandas as pd
import numpy as np

def max_pnl_price(next_mid_price,bonderror,trade,cols,model1,model2,penalty):
    sample = pd.DataFrame()
    cut_off = next_mid_price/trade['MidPrice']
    if trade['Side']=='Bid':
        sample['delta_from_mid'] = np.arange(0.8,cut_off-bonderror,0.01)
    if trade['Side']=='Offer':
        sample['delta_from_mid'] = np.arange(cut_off+bonderror,1.2,0.01)
    cols = cols.drop('delta_from_mid')
    sample[cols] = trade.drop('delta_from_mid')

    sample['P_trade'],sample['P_pospnl']=model1.predict_proba(sample.drop(columns=['Traded','PnL']).values)[:, 1],model2.predict_proba(sample.drop(columns=['Traded','PnL']).values)[:, 1]

    # 0 for missing trade, 1 for trading and positive pnl, -1 for trading and negative pnl
    sample['Exp_PnL'] = (sample['P_trade']*sample['P_pospnl'])-penalty*(sample['P_trade']*(1-sample['P_pospnl']))
    pnl_argmax = np.argmax(sample['Exp_PnL'])
    return sample, sample.iloc[pnl_argmax]['delta_from_mid']
    
def pnl(quote,test):
    test_perf = pd.DataFrame()
    test_perf['My_Price']=quote
    test_perf[['Side','QuotedPrice','NextMidPrice']]=test[['Side','QuotedPrice','NextMidPrice']]
    
    pos_pnl = len(test_perf[(test_perf['Side'] == 1)&(test_perf['NextMidPrice']>test_perf['My_Price'])]) + len(test_perf[(test_perf['Side'] == -1)&(test_perf['NextMidPrice']<test_perf['My_Price'])])
    
    better_price = len(test_perf[(test_perf['Side'] == 1)&(test_perf['QuotedPrice']<test_perf['My_Price'])]) + len(test_perf[(test_perf['Side'] == -1)&(test_perf['QuotedPrice']>test_perf['My_Price'])])
    
    traded_pos_pnl = len(test_perf[(test_perf['Side'] == 1)&(test_perf['NextMidPrice']>test_perf['My_Price'])&(test_perf['QuotedPrice']<test_perf['My_Price'])]) + len(test_perf[(test_perf['Side'] == -1)&(test_perf['NextMidPrice']<test_perf['My_Price'])&(test_perf['QuotedPrice']>test_perf['My_Price'])])
    
    print("pos_pnl:%.0f"%(pos_pnl))
    print("better_price:%.0f"%(better_price))
    print("traded_pos_pnl:%.0f"%(traded_pos_pnl))