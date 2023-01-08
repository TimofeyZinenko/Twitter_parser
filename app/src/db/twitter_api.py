from functools import lru_cache

import tweepy
from core.config import config_settings
from pydantic import BaseSettings


def twitter_api_auth(settings: BaseSettings):
    """Authenticate to Twitter and get API object.

    Args:
        setings (BaseSettings): config settings instance
    """
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(settings.api_key, settings.api_secret_key)
    auth.set_access_token(settings.api_access_token, settings.api_access_token_secret)

    # Create the API object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    return api


@lru_cache
def get_twitter_api():
    return twitter_api_auth(config_settings)
