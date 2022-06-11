import tweepy
import config
# auth = tweepy.OAuth2BearerHandler(bearer_token)
# api = tweepy.API(auth)

auth = tweepy.OAuth2AppHandler(
    api_key, api_secret
)
api = tweepy.API(auth, wait_on_rate_limit = True)

'''
api.create_friendship('AanandaGiri')
api.create_friendship('huggingface')    # follow people
api.update_status("I am currently posting this status") # post
api.update_profile(description = '')    # to update description
# '''
user = api.get_user('neuralnine')
print(user.name)
print(user.description)

tweets_home = api.home_timeline = api.home_timeline(count=10)

# liking tweets
for tweet in tweets_home:
    if tweet.author.name.lower() != "neuralnine":
        if not tweet.favourited:
            # making sure we are not liking already liked
            print(f'Liking {tweet.author.name}')
            api.create_favourite(tweet.id)

# liking posts
user = api.get_user("lexfridman")
tweets_user = api.user_timeline(userid=user.id)
for tweet in tweets_user:
    if not tweet.favourited:
        api.create_favourite(tweet.id)

# prists follower names
for follower in user.followers():
    print(f'{follower.name} follows {user.name}')

#  search for stuff
tweets = tweepy.cursor(api.search, q="brains", lang="en").items(10)
print([tweet.text for tweet in tweets])

if __name__ == "main":
    twitter_thread=threading.Thread(target = start_twitter_bot, args=(config.,))
