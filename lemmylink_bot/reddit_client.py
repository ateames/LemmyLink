# reddit_client.py

import praw
import config

def get_reddit_client():
    """
    Initialize and return a PRAW Reddit instance
    using credentials from config.py
    """
    reddit = praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD,
        user_agent=config.REDDIT_USER_AGENT,
    )
    return reddit
