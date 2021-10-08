import tweepy
import logging

import matching_rules

from urllib3.exceptions import ReadTimeoutError
from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class RetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or it's the author so, it should be ignored
            return

        # let's check for exact matching of our track phrase
        if hasattr(tweet, "retweeted_status"):  # Check if Retweet
            try:
                if hasattr(tweet.retweeted_status, 'extended_tweet'):
                    tweet_phrase = tweet.retweeted_status.extended_tweet["full_text"]
                else:
                    tweet_phrase = tweet.retweeted_status.text
            except AttributeError:
                tweet_phrase = tweet.retweeted_status.text
                logger.info(
                    "Error on accessing extended_tweet part of retweeted_tweet: " +
                    str(tweet.retweeted_status.text),
                    exc_info=True)
        else:
            try:
                if hasattr(tweet, "extended_tweet"):
                    tweet_phrase = tweet.extended_tweet["full_text"]
                else:
                    tweet_phrase = tweet.text
            except AttributeError:
                tweet_phrase = tweet.text
                logger.error(
                    "Error on accessing extended_tweet part of tweet: " + str(tweet.text), exc_info=True)

        tweet_phrase = tweet_phrase.lower()

        if contains_only_code_review_terms(tweet_phrase):
            try:
                logger.info(f"Tweet {tweet.id} retweeted ")
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweet" + str(e), exc_info=False)

    def on_error(self, status):
        logger.error(status)
        # 420 is a time out. We must wait before connecting again to not get blocked.
        if status == 420:
            # returning False in on_error disconnects the stream
            return False


def contains_only_code_review_terms(tweet_text):
    if matching_rules.contains_ai_related_phrases(tweet_text) \
            or matching_rules.contains_gaming_related_phrases(tweet_text) \
            or matching_rules.contains_inappropriate_phrases(tweet_text) \
            or matching_rules.contains_marketing_related_phrases(tweet_text) \
            or matching_rules.contains_unrelated_phrases(tweet_text) \
            or matching_rules.contains_conspiracy_phrases(tweet_text):
        return False

    if matching_rules.contains_code_review_phrase(tweet_text):
        return True
    return False


def main(keywords):
    api = create_api()
    tweets_listener = RetweetListener(api)
    start_stream(tweets_listener, keywords, api)


def start_stream(tweets_listener, keywords, api):
    try:
        stream = tweepy.Stream(api.auth, tweets_listener)
        stream.filter(track=keywords, languages=["en"])
    except ReadTimeoutError:
        stream.disconnect()
        logger.exception("ReadTimeoutError exception")
        logger.exception("Restart the stream")
        start_stream(tweets_listener, keywords, api)
    except Exception:
        stream.disconnect()
        logger.exception("Fatal exception. Consult logs.")
        start_stream(tweets_listener, keywords, api)


if __name__ == "__main__":
    # main(["python"])
    main(["code review,code reviews,#codereviews,codereviews,reviewing code,PR review,pull request,merge request"])
