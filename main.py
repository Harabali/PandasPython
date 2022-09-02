import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

#%%
print("Hello World!")
a = 151
#%%

# GET prices info
stock1 = yf.Ticker("NG=F")
stock2 = yf.Ticker("BZ=F")

#%%
prices_stock = stock1.history(period="max")
prices_ttf = stock2.history(period="max")
# prices_stock = prices_stock.drop(columns=['Dividends', 'Stock Splits'])
print(prices_stock.head())
print(prices_stock['Open'])
print(prices_stock['Open'][100])
ls = list(prices_stock['Open'])
print(ls)

prices_stock['Close'] = ls

#%%
plt.plot(prices_stock['Open'])
plt.show()

#%%
tmp = [y.year for y in prices_stock.index.tolist()]

#%%
prices_stock['Year'] = tmp

#%%
df_tmp = prices_stock[(prices_stock['Year']==2022) & (prices_stock['Year']==2022)]
# df_tmp = prices_stock.iloc[-30:]
# df_tmp = prices_stock.groupby(['Year']).mean()
plt.plot(df_tmp['Open'])
plt.show()

#%%
tmp = prices_stock.groupby(['Year']).max()
plt.bar(tmp.index.tolist(),tmp['Open'])
plt.show()


#%%
plt.plot(prices_stock['Open'],'b')
plt.plot(prices_ttf['Open'],'r')
plt.legend(['Natural Gas','Brent OIL'])
plt.show()

#%%
#USD-HUF
stock3 = yf.Ticker("USDHUF=X")
chgrate = stock3.history(period='max')
chgrate['Mean'] = (chgrate['High']+chgrate['Low'])/2
plt.plot(chgrate['Mean'])
plt.show()


#%%
# prices_ttf.index.get_value(prices_ttf,chgrate.index[1000])
prices_ttf.index.get_value(prices_ttf,prices_ttf.index[0])

tmp = {'Date':[], 'Open':[] , 'High':[],'Low':[], 'Close':[]}

for i in range(len(chgrate)):
    try:
        values = prices_stock.index.get_value(prices_stock,chgrate.index[i])
        tmp['Date'].append(chgrate.index[i])
        tmp['Open'].append(values[0]*chgrate['Mean'][i])
        tmp['High'].append(values[0] * chgrate['Mean'][i])
        tmp['Low'].append(values[0] * chgrate['Mean'][i])
        tmp['Close'].append(values[0] * chgrate['Mean'][i])
    except:
        continue

prices_stock_converted = pd.DataFrame(tmp).set_index('Date')

#%%
tmp = pd.merge(prices_ttf,chgrate, left_index=True,right_index=True)
tmp['Open_HUF'] = tmp.Open_x*tmp.Mean

plt.plot(prices_stock_converted['Open'],'b')
plt.plot(tmp['Open_HUF'],'r')
plt.legend(['Natural Gas','Brent OIL'])
plt.show()


#%%
tmp = chgrate.join(prices_ttf,rsuffix='_ttf')
tmp.fillna(-999,inplace=True)
tmp2 = tmp.dropna(axis=0,how='any')
tmp2.shape
