import boto3
import yfinance as yf
import pandas as pd

# boto3 is the AWS SDK library for Python.
# The "resources" interface allow for a higher-level abstraction than the low-level client interface.
# More details here: http://boto3.readthedocs.io/en/latest/guide/resources.html
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('djia')


# The BatchWriteItem API allows us to write multiple items to a table in one request.

djia = yf.Ticker("DJIA")

# get stock info


# get historical market data
hist = djia.history(start="2019-11-01", end="2020-05-01").reset_index().iloc[:,:5]
dates = pd.date_range(start="2019-11-01", end="2020-05-01", freq='D').to_frame(name="Date", index=False)
hist = hist.merge(dates,how='right', on="Date")
hist = hist.sort_values(by=['Date']).reset_index(drop=True)
hist = hist.interpolate(method='linear')
hist['Date'] = hist['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))


i=0
with table.batch_writer() as batch:
    while i<hist.shape[0]:
        batch.put_item(Item={"Date":hist.loc[i]['Date'],"Open":str(hist.loc[i]['Open']),"High":str(hist.loc[i]['High']),"Low":str(hist.loc[i]['Low']),"Close":str(hist.loc[i]['Close'])})
        i+=1