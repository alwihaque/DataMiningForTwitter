import tweepy
import os
import pandas as pd
import csv

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAO42bAEAAAAAOVTkiHTGCVCY5WI557PXbwq7UQ8%3D9vZmiMI98s6tjBRDGWs7GqrEwloYXeC8gl8Id5kmb8U1rynI9e")

subdir = os.listdir('tweetid')
# print(files, len(files))
with open('tweets.csv', "w") as f:
    writer = csv.writer(f)
    header = ['TweetID', 'body', 'likes', 'retweets', "date", "time"]
    writer.writerow(header)
    for dir in subdir:
        files = os.listdir('tweetid/'+dir)
        for file in files:
            #iterate over every tweet in file (can use pandas) and only include tweets in english
            d = pd.read_csv('tweetid/'+dir+'/'+file, sep='\t')
            data = pd.DataFrame(d)
            tweets = data.loc[data['lang'] == 'en']

            for index, tweet in tweets.iterrows():
                # look up tweet in tweets
                tweet_data = client.get_tweets(tweet['tweet_id'])
                if tweet_data.data[0] is None:
                    continue
                text = tweet_data.data[0]
                text.replace(",", "")
                likes = 0
                retweets = 0

                # write tweet id, contents, and likes and retweets
                # remove any commas from contents
                row = [tweet['tweet_id'], text, likes, retweets, tweet['date'], tweet['time']]
                writer.writerow(row)

            # tweet_data = client.get_tweets()
            # print(tweet_data.data[0])

#parse strings to eliminate punctuation and emojis
def string_parse(st):
    return st
