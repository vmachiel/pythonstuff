import tweepy
from datetime import datetime, timedelta

"""
The function layout is not necessary, this is done to make it portable.
"""


def login_twitter():
    # fill in, get them at twitter website.
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_secret = ""

    oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    oauth.set_access_token(access_token, access_secret)
    return tweepy.API(oauth)


def tweet_deleter(api, oldest_tweet_day):

    print("Getting tweets, please wait")
    tweets = tweepy.Cursor(api.user_timeline).items()

    deleted = 0
    ignored = 0

    for tweet in tweets:
        if tweet.created_at < oldest_tweet_day:
            print("Removing {}: [{}] {}".format(tweet.id, tweet.created_at,
                                                tweet.text))
            api.destroy_status(tweet.id)
            deleted += 1
        else:
            ignored += 1
    print("Removed {} tweets, left {} up.".format(deleted, ignored))


def favs_deleter(api, oldest_fav_day):

    print("Getting favorites, please wait")
    favs = tweepy.Cursor(api.favorites).items()

    unfavorited = 0
    ignored = 0

    for tweet in favs:
        if tweet.created_at < oldest_fav_day:
            print("Unfaving {}: [{}] {}".format(tweet.id, tweet.created_at,
                                                tweet.text))
            api.destroy_favorite(tweet.id)
            unfavorited += 1
        else:
            ignored += 1
    print("Removed {} favs, left {} intact".format(unfavorited, ignored))


def main():
    # set the days parameters to how many days of tweets/favs you wanted saved
    oldest_tweet_day = datetime.utcnow() - timedelta(days=730)
    oldest_fav_day = datetime.utcnow() - timedelta(days=900)

    api = login_twitter()

    tweet_deleter(api, oldest_tweet_day)
    favs_deleter(api, oldest_fav_day)


if __name__ == "__main__":
    main()
