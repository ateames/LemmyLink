# main.py

from reddit_client import get_reddit_client
from bridge_manager import BridgeManager

def main():
    # Initialize Reddit
    reddit = get_reddit_client()

    # Choose the subreddit you want to monitor
    subreddit_name = "LemmyLink"  # or your test subreddit
    subreddit = reddit.subreddit(subreddit_name)
    print(f"Listening for comments in r/{subreddit_name}...")

    # Initialize BridgeManager (which logs into Lemmy)
    bridge_manager = BridgeManager()

    # Use PRAW's streaming feature to get new comments as they appear
    for comment in subreddit.stream.comments(skip_existing=True):
        # If the trigger phrase is in the comment body (case-sensitive)
        if "LemmyLink!" in comment.body:
            print(f"[DEBUG] Trigger phrase found in comment {comment.id} by {comment.author}")
            bridge_manager.handle_trigger(comment)

if __name__ == "__main__":
    main()
