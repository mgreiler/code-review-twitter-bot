import tweepy
import logging
import os

logger = logging.getLogger()


def create_api():
    consumer_key = os.environ.get('TWITTER_CONS_KEY')
    consumer_secret = os.environ.get('TWITTER_CONS_SECRET')
    access_token = os.environ.get('TWITTER_TOKEN')
    access_token_secret = os.environ.get('TWITTER_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True, timeout=5)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
