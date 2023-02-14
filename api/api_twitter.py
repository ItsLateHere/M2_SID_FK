import tweepy
from api.config.config_twitter import *

from datetime import datetime

client = tweepy.Client(bearer_token=BEARER_TOKEN)


def get_User(username):
    print(username)
    res = client.get_user(
        username=username,
        user_fields=[
            "created_at", "description", 'protected',
            'verified', 'location', 'public_metrics'
        ]
    )
    compte = {
        'id_Compte': res.data.id,
        'name': res.data.name,
        'username': res.data.username,
        'compte_created_at': res.data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'protected': res.data.protected,
        'verified': res.data.verified,
        'location': res.data.location,
        'followers_count': res.data.public_metrics["followers_count"]
    }
    return compte


def get_Tweet(idTweet):
    res = client.get_tweet(
        id=idTweet,
        tweet_fields=[
            'edit_history_tweet_ids',
            "public_metrics",
            'geo',
            'created_at'
        ]
    )

    tweet = {
        'id_Tweet': res.data.id,
        'text': res.data.text,
        'tweet_created_at': res.data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'geo': res.data.geo,
        'retweet_count': res.data.public_metrics['retweet_count'],
        'reply_count': res.data.public_metrics['reply_count'],
        'like_count': res.data.public_metrics['like_count'],
        'quote_count': res.data.public_metrics['quote_count']
    }
    return tweet
