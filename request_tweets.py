import tweepy
import os
import pandas
import csv

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAO42bAEAAAAAOVTkiHTGCVCY5WI557PXbwq7UQ8%3D9vZmiMI98s6tjBRDGWs7GqrEwloYXeC8gl8Id5kmb8U1rynI9e")

files = os.listdir('tweetid')
print(files)

with open('tweets.csv', "w") as f:
    writer = csv.writer(f)
    header = ['TweetID', 'Body', 'Likes', 'Retweets']
    writer.writerow(header)
    for file in files:
        #iterate over every tweet in file (can use pandas) and only include tweets in english
        pd = pandas.read_csv(file)
        data = pd.DataFrame(csv)
        tweets = data.loc[data['language'] == 'en']

        # look up tweet in tweets
        for tweet in tweets:
            tweet_text = client.get_tweets(tweet.TweetID)
            tweet_likes = client.get_liking_users(tweet.TweetID, expansions=None, max_results=None, media_fields=None,
                                pagination_token=None, place_fields=None, poll_fields=None, tweet_fields=None,
                                user_fields=None, user_auth=False)
            tweet_retweets = client.get_retweeters(id, expansions=None, max_results=None, media_fields=None,
                            pagination_token=None, place_fields=None, poll_fields=None, tweet_fields=None,
                            user_fields=None, user_auth=False)



        # write tweet id, contents, and likes and retweets
        # remove any commas from contents
        writer.writerow(data)

        # tweet_data = client.get_tweets()
        # print(tweet_data.data[0])





rate: Union[int, str] = 1
auth = tweepy.OAuth1UserHandler(
    "Iiwmn8OaXO2SroZyhADCqQFCH", "j3e37pZ8GNpG94F3L4wL8LxiB5NYFjQcicyzAInlb6UHuYd6qQ"
)

client = tweepy.Client(
    "AAAAAAAAAAAAAAAAAAAAAO42bAEAAAAAOVTkiHTGCVCY5WI557PXbwq7UQ8%3D9vZmiMI98s6tjBRDGWs7GqrEwloYXeC8gl8Id5kmb8U1rynI9e")
id = '1507568189214920707'
tweets = client.get_tweets([id])

rts = client.get_retweeters()
likes = client.get_liking_users(id, expansions=None, max_results=None, media_fields=None,
                                pagination_token=None, place_fields=None, poll_fields=None, tweet_fields=None,
                                user_fields=None, user_auth=False)
print(tweets)
print(rts)
print(likes)
#
# api = tweepy.API(auth)
#
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

