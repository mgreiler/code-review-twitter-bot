
def contains_tweets_that_come_up_too_often(tweet_text):
    if ("amazon codeguru reviewer announces pull request dashboard " in tweet_text) \
            or ("Code Review from the Command Line" in tweet_text) \
            or ("even better code review in gitHub for mobile:" in tweet_text):
        return True
    return False


def contains_unrelated_phrases(tweet_text):
    if ("highway code review" in tweet_text) \
            or ("oracle hosting tiktok us data" in tweet_text) \
            or ("$yfms code review" in tweet_text) \
            or ("bitcoin" in tweet_text)\
            or ("BioEnergy" in tweet_text):
        return True
    return False


def contains_gaming_related_phrases(tweet_text):
    if ("review code" in tweet_text and "game" in tweet_text) \
            or ("review code" in tweet_text and "nintendo" in tweet_text) \
            or ("review code" in tweet_text and "playstation" in tweet_text) \
            or ("review code" in tweet_text and "playing" in tweet_text) \
            or ("receiving a review code" in tweet_text) \
            or ("coupon" in tweet_text) \
            or ("maker switch" in tweet_text) \
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
            or "doom 64 remaster" in tweet_text \
            or "doom 64" in tweet_text \
            or "streaming" in tweet_text \
            or "resident evil 3" in tweet_text \
            or "final fantasy 7" in tweet_text \
            or "fantasy vii remake" in tweet_text \
            or "Super Mario" in tweet_text \
            or "deathstranding" in tweet_text \
            or "kena bridge" in tweet_text \
            or "sega" in tweet_text \
            or "emberlab" in tweet_text:
        return True
    return False


def contains_conspiracy_phrases(tweet_text):
    if ("https://lockdownsceptics.org/code-review-of-fergusons-model/" in tweet_text) \
            or "ferguson" in tweet_text \
            or "lockdown sceptics" in tweet_text \
            or "imperial college model" in tweet_text \
            or "covid" in tweet_text \
            or "corona" in tweet_text \
            or "lockdownsceptics" in tweet_text\
            or "crypto" in tweet_text:
        return True
    return False


def contains_inappropriate_phrases(tweet_text):
    if "sex" in tweet_text:
        return True
    return False


def contains_marketing_related_phrases(tweet_text):
    if "product review" in tweet_text \
            or "discount" in tweet_text \
            or "referral code" in tweet_text \
            or "promo code" in tweet_text \
            or "medici code review" in tweet_text \
            or "kibo code review" in tweet_text:
        return True
    return False


def contains_ai_related_phrases(tweet_text):
    if "deepcode taps ai" in tweet_text \
            or "deepcode brings ai-powered code review to c and c++" in tweet_text:
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
            or "review his code" in tweet_text \
            or " pr for review" in tweet_text \
            or (" pr review " in tweet_text) \
            or ("pull request" in tweet_text and "review" in tweet_text) \
            or ("merge request" in tweet_text and "review" in tweet_text):
        # logger.info("Exact Match found in: " + tweet_text)
        return True
    return False
