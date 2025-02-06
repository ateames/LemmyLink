# main.py

from reddit_client import get_reddit_client
from bridge_manager import BridgeManager
import config

def main():
    # Initialize Reddit
    reddit = get_reddit_client()

    # Use the subreddit name from config.py
    subreddit = reddit.subreddit(config.SUBREDDIT_NAME)
    print(f"Listening for comments in r/{config.SUBREDDIT_NAME}...")

    # Initialize BridgeManager (which logs into Lemmy)
    bridge_manager = BridgeManager()

    # Monitor new submissions (posts) in the subreddit
    for submission in subreddit.stream.submissions(skip_existing=True):
        # Check if the trigger phrase is in the post title or body
        if "LemmyLink!" in submission.title or "LemmyLink!" in submission.selftext:
            print(f"[DEBUG] Trigger found in post {submission.id} by {submission.author}")
            bridge_manager.handle_trigger(submission)

    # Use PRAW's streaming feature to get new comments as they appear
    for comment in subreddit.stream.comments(skip_existing=True):
        # If the trigger phrase is in the comment body (case-sensitive)
        if "LemmyLink!" in comment.body:
            print(f"[DEBUG] Trigger phrase found in comment {comment.id} by {comment.author}")
            bridge_manager.handle_trigger(comment)

if __name__ == "__main__":
    main()
    
