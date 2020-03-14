import tweepy
import logging
from config import create_api
import time

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
        tweet_phrase = ""
        if hasattr(tweet, "retweeted_status"):  # Check if Retweet
            try:
                if hasattr(tweet.retweeted_status, 'extended_tweet'):
                    tweet_phrase = tweet.retweeted_status.extended_tweet["full_text"]
                else:
                    tweet_phrase = tweet.retweeted_status.text
            except AttributeError:
                tweet_phrase = tweet.retweeted_status.text
                logger.info(
                    "Error on accessing extended_tweet part of retweeted_tweet: " + str(tweet.retweeted_status.text),
                    exc_info=True)
        else:
            try:
                if hasattr(tweet, "extended_tweet"):
                    tweet_phrase = tweet.extended_tweet["full_text"]
                else:
                    tweet_phrase = tweet.text
            except AttributeError:
                tweet_phrase = tweet.text
                logger.error("Error on accessing extended_tweet part of tweet: " + str(tweet.text), exc_info=True)

        tweet_phrase = tweet_phrase.lower()

        if contains_only_code_review_terms(tweet_phrase):
            try:
                logger.info(f"Tweet {tweet.id} retweeted ")
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweet", exc_info=False)

    def on_error(self, status):
        logger.error(status)
        # 420 is a time out. We must wait before connecting again to not get blocked.
        if status == 420:
            # returning False in on_error disconnects the stream
            return False


def contains_only_code_review_terms(tweet_text):
    if contains_ai_related_phrases(tweet_text) \
            or contains_gaming_related_phrases(tweet_text) \
            or contains_marketing_related_phrases(tweet_text):
        return False

    if contains_code_review_phrase(tweet_text):
        return True
    return False


def contains_gaming_related_phrases(tweet_text):
    if ("review code" in tweet_text and "game" in tweet_text) \
            or ("review code" in tweet_text and "nintendo" in tweet_text) \
            or ("review code" in tweet_text and "playstation" in tweet_text) \
            or ("review code" in tweet_text and "playing" in tweet_text) \
            or ("receiving a review code" in tweet_text) \
            or ("coupon" in tweet_text) \
            or "review the code of" in tweet_text \
            or "death stranding" in tweet_text \
            or "apply for review code" in tweet_text \
            or "need that review code" in tweet_text \
            or "need a review code" in tweet_text \
            or "request that review code" in tweet_text \
            or "request a review code" in tweet_text \
            or "the lost code review" in tweet_text \
            or "persona 5 royal" in tweet_text \
            or "doom eternal" in tweet_text \
            or "quantum manifestation code review" in tweet_text \
            or "deathstranding" in tweet_text:
        return True
    return False


def contains_marketing_related_phrases(tweet_text):
    if "product review" in tweet_text \
            or "discount" in tweet_text \
            or "referral code" in tweet_text \
            or "promo code" in tweet_text \
            or "Kibo Code Review" in tweet_text:
        return True
    return False


def contains_ai_related_phrases(tweet_text):
    if "DeepCode taps AI" in tweet_text:
        return True
    return False


def contains_code_review_phrase(tweet_text):
    # logger.info("Looking for exact match")
    if "code review" in tweet_text \
            or "reviewing code" in tweet_text \
            or "codereview" in tweet_text \
            or "review code" in tweet_text \
            or "review the code" in tweet_text \
            or "review your code" in tweet_text \
            or "review someone's code" in tweet_text \
            or " pr for review" in tweet_text \
            or (" pr review " in tweet_text) \
            or ("pull request" in tweet_text and "review" in tweet_text) \
            or ("merge request" in tweet_text and "review" in tweet_text):
        logger.info("Exact Match found in: " + tweet_text)
        return True
    return False


def main(keywords):
    api = create_api()
    tweets_listener = RetweetListener(api)
    start_stream(tweets_listener, keywords, api)


def start_stream(tweets_listener, keywords, api):
    while True:
        try:
            stream = tweepy.Stream(api.auth, tweets_listener)
            stream.filter(track=keywords, languages=["en"])
        except Exception as er:
            logger.error("Error in start_stream occurred " + er)
            time.sleep(5)
            continue


if __name__ == "__main__":
    # main(["python"])
    main(["code review,code reviews,#codereviews,codereviews,reviewing code,PR review,pull request,merge request"])
