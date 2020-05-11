import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Tweet_Data')

resp = table.scan()

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier

def clean_tweet(self, tweet): 
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



analysis = TextBlob(self.clean_tweet(tweet)) 