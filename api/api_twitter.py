# Récupérer les données à partir de l'API TWITTER

import tweepy
from api.config.config_twitter import *

from datetime import datetime
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# cette fonction récupère toutes les données d'un compte Twitter à partir du nom d'utilisateur(username :'UNIQUE') comme:
#       - le nom d'utilisateur
#       - date de création du compte
#       - nombre des followers
#       - le compte privé ou non
#       - compte vérifier ou non
#       ....


def get_User(username):
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
        'compte_created_at': res.data.created_at.strftime('%Y-%m-%d'),
        'protected': int(res.data.protected==True),
        'verified': int(res.data.verified==True),
        'location': res.data.location,
        'followers_count': res.data.public_metrics["followers_count"]
    }
    return compte

# cette fonction récupère toutes les données d'un tweet à partir de l'Id de la publication comme:
#       - date création de la publication
#       - la publication
#       - nombre des likes
#       - nombre des commentaires
#       - nombre des retweets
#       - nombre des followers
#       ....
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
        'tweet_created_at': res.data.created_at.strftime('%Y-%m-%d'),
        'geo': res.data.geo,
        'retweet_count': res.data.public_metrics['retweet_count'],
        'reply_count': res.data.public_metrics['reply_count'],
        'like_count': res.data.public_metrics['like_count'],
        'quote_count': res.data.public_metrics['quote_count']
    }
    return tweet
