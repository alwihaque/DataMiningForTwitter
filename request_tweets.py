import tweepy
import os
import pandas as pd
import csv
import time


def main():
    kt = 0
    ah = 1
    client = tweepy.Client(
        "AAAAAAAAAAAAAAAAAAAAACQGbQEAAAAALeb1NcPRAhWqX7N2VbeFs0wq%2F34%3Dm9x3eYcJY8y79x8zNrWvI0pPSl4f4T4Hpt7CPz2HMaxsYoOdKQ",
    )

    subdir = os.listdir('tweetid')
    with open('tweets.csv', "w") as f:
        writer = csv.writer(f)
        header = ['TweetID', 'body', "date", "time"]
        writer.writerow(header)
        for directory in subdir:
            file_ctr = 0
            files = os.listdir('tweetid/' + directory)
            for file in files:
                file_ctr = file_ctr + 1
                print(file_ctr)
                print(file)
                d = pd.read_csv('tweetid/' + directory + '/' + file, sep='\t')
                data = pd.DataFrame(d)
                tweets = data.loc[data['lang'] == 'en']
                tweet_ids = []
                counter = 0
                for index, tweet in tweets.iterrows():
                    try:
                        if counter % 100 == 0:
                            if type(tweet_ids) is not int:
                                tweet_ids.append(tweet['tweet_id'])
                            if type(tweet_ids) is not int and len(tweet_ids) == 1:
                                tweet_ids = tweet_ids[0]
                            if type(tweet_ids) is not int and len(tweet_ids) == 101:
                                tweet_ids.pop(0)
                            tweet_data = client.get_tweets(tweet_ids)
                            for tweet_d in tweet_data.data:
                                if tweet_d is None:
                                    continue
                                if 'RT' in tweet_d['text']:
                                    continue
                                body = string_parse(str(tweet_d['text']))
                                id_d = tweet_d.id
                                record = tweets.loc[tweets['tweet_id'] == id_d]
                                date = record.date
                                time = record.time
                                writer.writerow([id_d, body, date.to_string(index=False), time.to_string(index=False)])
                            tweet_ids = []
                        else:
                            tweet_ids.append(tweet['tweet_id'])
                        counter = counter + 1
                    except tweepy.errors.TooManyRequests as e:
                        if kt == 1:
                            print(str(e) + "here")
                            kt = 0
                            ah = 1
                            client = tweepy.Client(
                                "AAAAAAAAAAAAAAAAAAAAACQGbQEAAAAALeb1NcPRAhWqX7N2VbeFs0wq%2F34%3Dm9x3eYcJY8y79x8zNrWvI0pPSl4f4T4Hpt7CPz2HMaxsYoOdKQ")
                            # if type(tweet_ids) is int:
                            #     tweet_ids = [tweet_ids]
                            # continue
                        elif ah == 1:
                            print(str(e))
                            kt = 1
                            ah = 0
                            client = tweepy.Client(
                                "AAAAAAAAAAAAAAAAAAAAAO42bAEAAAAAOVTkiHTGCVCY5WI557PXbwq7UQ8%3D9vZmiMI98s6tjBRDGWs7GqrEwloYXeC8gl8Id5kmb8U1rynI9e")
                            # if type(tweet_ids) is int:
                            #     tweet_ids = [tweet_ids]
                            # continue


def string_parse(st):
    replaced = str.replace(st, ',', '').replace('\n', ' ')
    return replaced


if __name__ == "__main__":
    main()
