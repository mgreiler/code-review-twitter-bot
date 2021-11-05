gaming_related_phrases = [
    "game"
    "nintendo"
    "playstation",
    "playing",
    "receiving a review code",
    "coupon",
    "maker switch",
    "review the code of",
    "death stranding",
    "apply freview code",
    "need that review code",
    "need a review code",
    "request that review code",
    "request a review code",
    "the lost code review",
    "persona 5 royal",
    "doom eternal",
    "quantum manifestation code review",
    "doom 64 remaster",
    "doom 64",
    "streaming",
    "resident evil 3",
    "final fantasy 7",
    "fantasy vii remake",
    "Super Mario",
    "deathstranding",
    "kena bridge",
    "sega",
    "emberlab"
]


def contains_gaming_related_phrases(tweet_text):
    for phrase in gaming_related_phrases:
        if phrase in tweet_text:
            return True
    return False


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
            or ("bitcoin" in tweet_text) \
            or ("BioEnergy" in tweet_text):
        return True
    return False


conspiracy_phrases = [
    "https://lockdownsceptics.g/code-review-of-fergusons-model/",
    "ferguson",
    "lockdown sceptics",
    "imperial college model",
    "covid",
    "cona",
    "lockdownsceptics",
    "crypto"
]


def contains_conspiracy_phrases(tweet_text):
    for phrase in conspiracy_phrases:
        if phrase in tweet_text:
            return True
    return False


def contains_inappropriate_phrases(tweet_text):
    if "sex" in tweet_text:
        return True
    return False


marketing_related_phrases = [
    "product review"
    "discount",
    "referral code",
    "promo code",
    "medici code review",
    "kibo code review"
]


def contains_marketing_related_phrases(tweet_text):
    for phrase in marketing_related_phrases:
        if phrase in tweet_text:
            return True
    return False


def contains_ai_related_phrases(tweet_text):
    if "deepcode taps ai" in tweet_text \
            or "deepcode brings ai-powered code review to c and c++" in tweet_text:
        return True
    return False


code_review_phrases = [
    "code review",
    "reviewing code",
    "codereview",
    "review code",
    "review the code",
    "review your code",
    "review someone's code",
    "review his code",
    " pr freview",
    " pr review ",
    "pull request",
    "merge request"
]


def contains_code_review_phrase(tweet_text):
    for phrase in code_review_phrases:
        if phrase in tweet_text:
            return True
    return False
