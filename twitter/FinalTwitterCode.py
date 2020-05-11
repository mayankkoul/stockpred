#!/usr/bin/env python
# coding: utf-8

# In[22]:


from __future__ import print_function 
import GetOldTweets3 as got
import boto3
import json
import decimal
import time
import collections
from datetime import datetime
import datetime
import argparse

parser = argparse.ArgumentParser(description="This script is going to upload the tweets from twitter for the date you enter.")
parser.add_argument('-d','--date',type=str, metavar='',help="enter date as yyyy-mm-dd")
args = parser.parse_args()

def scrapetweet(fromdate,todate):
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://localhost:8000")
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
    tweets_uploaded=0
    for word in keyword_list:
        for state in states_list:
            print("Sending Request Again")
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(word)                                                       .setSince(fromdate)                                                       .setUntil(todate)                                                       .setNear(state + ", USA")                                                       .setMaxTweets(100)                                                       .setEmoji("unicode")
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
    d_list['tweeted_on']=[str(x.strftime('%Y-%M-%D')) for x in d_list['tweeted_on'] ]
    lot=list(zip(d_list['id_tweet'],d_list['tweeted_on'],d_list['tweeted_content']))
    for item in lot:
        id_tweet=item[0]
        tweet_datetime=item[1]
        tweet_content=item[2]
        table.put_item(Item={'id_tweet':id_tweet ,'tweet_datetime': tweet_datetime,'tweet_content': tweet_content,})
    tweets_uploaded=tweets_uploaded+len(tweet_list)
    print("Tweets Uploaded: {}".format(tweets_uploaded))
            
    text="uploaded"
    return text

def uploadbydate(date):
    fromdate=datetime.strptime(date,'%Y-%m-%d')
    fromdate= fromdate.strftime('%Y-%m-%d')
    todate=date+ datetime.timedelta(days=1)
    todate=todate.strftime('%Y-%m-%d')
    out=scrapetweet(fromdate,todate)
    if out== 'uploaded':
        text="Uploaded"
    else:
        text="Not Uploaded"
    return text

if __name__ == "__main__":
    output= uploadbydate(args.date)
    print(output)

