import logging
from urllib3.exceptions import ReadTimeoutError
import tweepy
import matching_rules
from time import sleep

from config import create_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_tweet_fulltexr(tweet):
    # Get the full text of the tweet, handling possible extended tweets
    if hasattr(tweet, "retweeted_status"):  # Check if Retweet
        try:
            if hasattr(tweet.retweeted_status, 'extended_tweet'):
                tweet_phrase = tweet.retweeted_status.extended_tweet["full_text"]
            else:
                tweet_phrase = tweet.retweeted_status.text
        except AttributeError:
            tweet_phrase = tweet.retweeted_status.text
            print("Error accessing extended_tweet of retweet")
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
            print("Error accessing extended_tweet of tweet")
            logger.error(
                "Error on accessing extended_tweet part of tweet: " + str(tweet.text), exc_info=True)

    return tweet_phrase


class RetweetListener(tweepy.StreamListener):

    def __init__(self, api):
        self.api = api
        self.me = api.me()
        self.timeline = set([tweet.id for tweet in api.user_timeline()])

    def on_status(self, tweet):

        if tweet.id in self.timeline:
            # check if we already retweeted or tweeted this tweet. If let's skip it.
            print("Tweet already on timeline")
            logger.info(f"Tweet ALREADY on Timeline")
            return

        # Check if this tweet is a reply or it's the author so, it should be ignored
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            print("Skipping reply or self-tweet")
            return

        self.timeline.add(tweet.id)

        tweet_text = get_tweet_fulltexr(tweet)

        if matching_rules.contains_only_allowed_code_review_phrases(tweet_text):
            try:
                logger.info(f"Tweet {tweet.id} retweeted ")
                print(f"Tweet {tweet.id} retweeted ")
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweet" + str(e), exc_info=False)

    def on_error(self, status):
        logger.error(status)
        # 420 is a time out. We must wait before connecting again to not get blocked.
        if status == 420:
            # returning False in on_error disconnects the stream
            return False


# def start_stream(tweets_listener, keywords, api):
#     try:
#         stream = tweepy.Stream(api.auth, tweets_listener)
#         stream.filter(track=keywords, languages=["en"])
#     except ReadTimeoutError:
#         stream.disconnect()
#         logger.exception("ReadTimeoutError exception")
#         logger.exception("Restart the stream")
#         start_stream(tweets_listener, keywords, api)
#     except Exception:
#         stream.disconnect()
#         logger.exception("Fatal exception. Consult logs.")
#         start_stream(tweets_listener, keywords, api)


def main(keywords):
    api = create_api()
    tweets_listener = RetweetListener(api)
    start_stream(tweets_listener, keywords, api)


def start_stream(tweets_listener, keywords, api, max_retries=5, retry_count=0):
    stream = tweepy.Stream(api.auth, tweets_listener)

    # Add sleep function
    sleep_time = 900

    while True:
        try:
            stream.filter(track=keywords, languages=["en"])
        except tweepy.RateLimitError:
            logger.exception("Rate limit reached. Sleeping for %d seconds", sleep_time)
            sleep(sleep_time)
        except ReadTimeoutError:
            stream.disconnect()
            logger.exception("ReadTimeoutError exception")
            return
        except Exception:
            stream.disconnect()
            logger.exception("Fatal exception. Consult logs.")

        if retry_count >= max_retries:
            logger.exception("Max retries reached. Aborting.")
            return
        else:
            logger.exception("Restarting the stream")
            start_stream(tweets_listener, keywords, api, max_retries, retry_count + 1)


if __name__ == "__main__":
    # main(["python"])
    keywords = ["code review", "code reviews", "#codereviews", "codereviews", "reviewing code", "PR review",
                "pull request", "merge request"]
    main(keywords)
