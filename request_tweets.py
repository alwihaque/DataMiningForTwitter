import tweepy
import os
import pandas
import csv

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAO42bAEAAAAAOVTkiHTGCVCY5WI557PXbwq7UQ8%3D9vZmiMI98s6tjBRDGWs7GqrEwloYXeC8gl8Id5kmb8U1rynI9e")

subdir = os.listdir('tweetid')
# print(files, len(files))
for dir in subdir:
    with open('tweets.csv', "w") as f:
        writer = csv.writer(f)

        header = ['TweetID', 'body', 'likes', 'retweets', "date", "time"]
        writer.writerow(header)
        # for file in files:
        #     #iterate over every tweet in file (can use pandas) and only include tweets in english
        #     pd = pandas.read_csv(file)
        #     data = pd.DataFrame(csv)
        #     tweets = data.loc[data['language'] == 'en']

            # look up tweet in tweets

            # write tweet id, contents, and likes and retweets
            # remove any commas from contents
            # writer.writerow(data)

            # tweet_data = client.get_tweets()
            # print(tweet_data.data[0])



