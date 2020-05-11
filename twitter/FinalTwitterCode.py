#!/usr/bin/env python
# coding: utf-8

# In[22]:


from __future__ import print_function 
import GetOldTweets3 as got
import pandas as pd
import boto3
import time
import collections
import datetime as dt1
from datetime import datetime as dt
# import argparse

# parser = argparse.ArgumentParser(description="This script is going to upload the tweets from twitter for the date you enter.")
# parser.add_argument('-d','--date',type=str, metavar='',help="enter date as yyyy-mm-dd")
# args = parser.parse_args()

def scrapetweet(fromdate,todate):
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    d_list=collections.defaultdict(list)
    table = dynamodb.Table('Tweet_Data')
    keyword_list=["I am","makes me","i'm","feel"]
    states_list=['Alabama','Alaska','Arizona','Arkansas','California','Colorado',
             'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho', 
             'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
             'Maine' 'Maryland','Massachusetts','Michigan','Minnesota',
             'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
             'New Hampshire','New Jersey','New Mexico','New York',
             'North Carolina','North Dakota','Ohio',    
             'Oklahoma','Oregon','Pennsylvania','Rhode Island',
             'South  Carolina','South Dakota','Tennessee','Texas','Utah',
             'Vermont','Virginia','Washington','West Virginia',
             'Wisconsin','Wyoming']
    for word in keyword_list:
        for state in states_list:
            print("for state:{} and word:{} on date:{}".format(state,word,fromdate))
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word).setSince(fromdate).setUntil(todate).setNear(state + ", USA").setMaxTweets(10).setEmoji("unicode")
            try:
                tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            except:
                print("Going to sleep for 15 mins")
                time.sleep(920)
                tweets = got.manager.TweetManager.getTweets(tweetCriteria)
            tweet_list=[tweet for tweet in tweets]
            for tweet in tweet_list:
                if tweet.id in d_list['id_tweet']:
                    pass
                else:
                    d_list['id_tweet'].append(tweet.id)
                    d_list['tweeted_on'].append(tweet.date)
                    d_list['tweeted_content'].append(tweet.text)
    d_list['tweeted_on']=[x.strftime('%Y-%m-%d') for x in d_list['tweeted_on']]
    tweets_uploaded_by_date=len(d_list['id_tweet'])
    print("Number of tweets uploaded on {} is : {}".format(fromdate,tweets_uploaded_by_date))
    lot=list(zip(d_list['id_tweet'],d_list['tweeted_on'],d_list['tweeted_content']))
    for item in lot:
        id_tweet=item[0]
        tweet_datetime=item[1]
        tweet_content=item[2]
        if(tweet_content==""):
            pass
        else:
            table.put_item(Item={'id_tweet':id_tweet ,'tweet_datetime': tweet_datetime,'tweet_content': tweet_content})
        
            
    text="uploaded"
    return text

def uploadbydate(date):
    fromdate=dt.strptime(date,'%Y-%m-%d')
    todate=fromdate + dt1.timedelta(days=1)
    fromdate= fromdate.strftime('%Y-%m-%d')
    todate=todate.strftime('%Y-%m-%d')
    out=scrapetweet(fromdate,todate)
    if out== 'uploaded':
        text="Uploaded"
    else:
        text="Not Uploaded"
    return text

if __name__ == "__main__":
    dates = pd.date_range(start="2019-11-01", end="2020-05-10", freq='D').to_frame(name="Date", index=False)
    length = dates.shape[0]
    dates["Date"]=dates["Date"].apply(lambda x: x.strftime('%Y-%m-%d'))
    i=0
    while i<length:
        out=uploadbydate(dates.iloc[i,:].item())
        print(out)
        i=i+1
        
    

