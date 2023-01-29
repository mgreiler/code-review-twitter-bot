def contains_only_allowed_code_review_phrases(tweet_text):
    tweet_text = tweet_text.lower()

    unwanted_phrases_to_check = [unrelated_phrases, ai_related_phrases, gaming_related_phrases, inappropriate_phrases,
                                 marketing_related_phrases, conspiracy_phrases, noisy_phrases]

    for phrase_set in unwanted_phrases_to_check:
        if contains_phrases(tweet_text, phrase_set):
            return False
    if contains_phrases(tweet_text, code_review_phrases):
        return True
    return False


def contains_phrases(tweet_text, phrases):
    return bool(phrases.intersection(set(tweet_text.split())))


gaming_related_phrases = set(map(str.lower, {
    "game",
    "nintendo",
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
}))

noisy_phrases = set(map(str.lower, {"amazon codeguru reviewer announces pull request dashboard ",
                                    "Code Review from the Command Line",
                                    "even better code review in gitHub for mobile:"}))

unrelated_phrases = set(map(str.lower,
                            {"highway code review", "oracle hosting tiktok us data", "$yfms code review", "bitcoin",
                             "BioEnergy"}))

conspiracy_phrases = set(map(str.lower, {
    "https://lockdownsceptics.g/code-review-of-fergusons-model/",
    "ferguson",
    "lockdown sceptics",
    "imperial college model",
    "covid",
    "cona",
    "lockdownsceptics",
    "crypto"
}))

marketing_related_phrases = set(map(str.lower, {
    "product review"
    "discount",
    "referral code",
    "promo code",
    "medici code review",
    "kibo code review"
}))

ai_related_phrases = set(map(str.lower, {"deepcode taps ai", "deepcode brings ai-powered code review to c and c++"}))

inappropriate_phrases = set(map(str.lower, {"sex", "penis", "boobs", "vagina"}))

code_review_phrases = set(map(str.lower, {
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
}))
