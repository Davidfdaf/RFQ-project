import pandas as pd
import numpy as np

def max_pnl_price(bonderror,trade,column1,column2,model1,model2,penalty):
    sample = pd.DataFrame()
    cut_off = trade['next_mid_price']/trade['MidPrice']
    if trade['Side']==1:
        sample['delta_from_mid'] = np.arange(min(0.1,cut_off-bonderror),max(0.1,cut_off-bonderror),0.01)
    if trade['Side']==-1:
        sample['delta_from_mid'] = np.arange(min(cut_off+bonderror,1.2),max(cut_off+bonderror,1.2),0.01)
    
    sample[column1] = trade[column1]

    sample['P_trade'],sample['P_pospnl']=model1.predict_proba(sample.drop(columns=['delta_from_mid']).values)[:, 1],model2.predict_proba(sample.drop(columns=['delta_from_mid']).values)[:, 1]

    # 0 for missing trade, 1 for trading and positive pnl, -1 for trading and negative pnl
    sample['Exp_PnL'] = (sample['P_trade']*sample['P_pospnl'])-penalty*(sample['P_trade']*(1-sample['P_pospnl']))
    pnl_argmax = np.argmax(sample['Exp_PnL'])
    return sample, sample.iloc[pnl_argmax]['delta_from_mid']
    
def pnl(quote,test):
    test_perf = pd.DataFrame()
    test_perf['My_Price']=quote
    test_perf[['Side','QuotedPrice','NextMidPrice']]=test[['Side','QuotedPrice','NextMidPrice']]
    
    pos_pnl = len(test_perf[(test_perf['Side'] == 'Bid')&(test_perf['NextMidPrice']>test_perf['My_Price'])]) + len(test_perf[(test_perf['Side'] == 'Offer')&(test_perf['NextMidPrice']<test_perf['My_Price'])])
    
    better_price = len(test_perf[(test_perf['Side'] == 'Bid')&(test_perf['QuotedPrice']<test_perf['My_Price'])]) + len(test_perf[(test_perf['Side'] == 'Offer')&(test_perf['QuotedPrice']>test_perf['My_Price'])])
    
    traded_pos_pnl = len(test_perf[(test_perf['Side'] == 'Bid')&(test_perf['NextMidPrice']>test_perf['My_Price'])&(test_perf['QuotedPrice']<test_perf['My_Price'])]) + len(test_perf[(test_perf['Side'] == 'Offer')&(test_perf['NextMidPrice']<test_perf['My_Price'])&(test_perf['QuotedPrice']>test_perf['My_Price'])])

    print("pos_pnl:%.0f"%(pos_pnl))
    print("better_price:%.0f"%(better_price))
    print("traded_pos_pnl:%.0f"%(traded_pos_pnl))