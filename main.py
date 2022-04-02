import tweepy

auth = tweepy.OAuth1UserHandler(
   "Iiwmn8OaXO2SroZyhADCqQFCH", "j3e37pZ8GNpG94F3L4wL8LxiB5NYFjQcicyzAInlb6UHuYd6qQ"
)

client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAO42bAEAAAAAOVTkiHTGCVCY5WI557PXbwq7UQ8%3D9vZmiMI98s6tjBRDGWs7GqrEwloYXeC8gl8Id5kmb8U1rynI9e")

tweets = client.get_tweets(['1333156800926015488'])
print(tweets.data[0])

#
# api = tweepy.API(auth)
#
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

