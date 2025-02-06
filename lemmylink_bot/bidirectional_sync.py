# bidirectional_sync.py

import time
from reddit_client import get_reddit_client
from lemmy_client import LemmyClient
from mapping_db import get_all_mappings
from comment_mapping_db import (
    get_comment_mapping_by_reddit_comment,
    get_comment_mapping_by_lemmy_comment,
    insert_comment_mapping
)

def sync_reddit_to_lemmy_comments(reddit, lemmy):
    """
    For each mapped Reddit submission, sync any new Reddit comments to Lemmy.
    """
    mappings = get_all_mappings()
    if not mappings:
        print("No post mappings found. Skipping Reddit-to-Lemmy sync.")
        return

    for mapping in mappings:
        # Assuming mapping record structure: (id, reddit_submission_id, reddit_trigger_comment_id, lemmy_post_id, created_at)
        reddit_submission_id = mapping[1]
        lemmy_post_id = mapping[3]

        submission = reddit.submission(id=reddit_submission_id)
        submission.comments.replace_more(limit=0)
        all_comments = submission.comments.list()

        print(f"Processing Reddit submission {reddit_submission_id}: Found {len(all_comments)} comments.")

        for comment in all_comments:
            # Skip if already synced or if it's the bot's own comment.
            if get_comment_mapping_by_reddit_comment(comment.id) is not None:
                continue
            if comment.author and comment.author.name.lower() == reddit.config.username.lower():
                continue

            try:
                # For MVP, post as a top-level comment on Lemmy.
                content = (
                    f"From Reddit user [/u/{comment.author}](https://reddit.com/user/{comment.author})"
                    f"([Link to Reddit Comment](https://www.reddit.com{comment.permalink}))\n\n{comment.body}"
                )

                lemmy_response = lemmy.create_comment(
                    post_id=lemmy_post_id,
                    content=content,
                    parent_id=None  # Extend later to support nested replies.
                )
                # Extract Lemmy comment ID.
                lemmy_comment_id = (
                    lemmy_response.get("comment_view", {})
                                  .get("comment", {})
                                  .get("id")
                )
                if lemmy_comment_id:
                    insert_comment_mapping(comment.id, lemmy_comment_id)
                    print(f"Synced Reddit comment {comment.id} to Lemmy comment {lemmy_comment_id}")
                else:
                    print(f"Failed to extract Lemmy comment ID for Reddit comment {comment.id}. Response: {lemmy_response}")
            except Exception as e:
                print(f"Error syncing Reddit comment {comment.id}: {e}")

def sync_lemmy_to_reddit_comments(reddit, lemmy):
    """
    For each mapped post, sync any new Lemmy comments to Reddit.
    """
    mappings = get_all_mappings()
    if not mappings:
        print("No post mappings found. Skipping Lemmy-to-Reddit sync.")
        return

    for mapping in mappings:
        reddit_submission_id = mapping[1]
        lemmy_post_id = mapping[3]
        submission = reddit.submission(id=reddit_submission_id)

        try:
            lemmy_comments = lemmy.get_comments(lemmy_post_id)
        except Exception as e:
            print(f"Error fetching comments from Lemmy for post {lemmy_post_id}: {e}")
            continue

        print(f"Processing Lemmy post {lemmy_post_id}: Found {len(lemmy_comments)} comments.")

        for comment in lemmy_comments:
            # Drill into the nested structure: assume each comment dict contains a "comment_view" key
            comment_data = comment.get("comment_view", {}).get("comment", {})
            lemmy_comment_id = comment_data.get("id")
            if not lemmy_comment_id:
                continue
            # Skip if already synced
            if get_comment_mapping_by_lemmy_comment(lemmy_comment_id) is not None:
                continue

            try:
                # Extract the content from the nested comment data.
                content = comment_data.get("content", "")
                reddit_comment = submission.reply(content)
                insert_comment_mapping(reddit_comment.id, lemmy_comment_id)
                print(f"Synced Lemmy comment {lemmy_comment_id} to Reddit comment {reddit_comment.id}")
            except Exception as e:
                print(f"Error syncing Lemmy comment {lemmy_comment_id}: {e}")

if __name__ == "__main__":
    # Initialize clients.
    reddit = get_reddit_client()
    lemmy = LemmyClient()
    lemmy.login()

    while True:
        print("Starting bidirectional comment sync...")
        sync_reddit_to_lemmy_comments(reddit, lemmy)
        sync_lemmy_to_reddit_comments(reddit, lemmy)
        print("Bidirectional sync complete. Waiting 60 seconds before next check...")
        time.sleep(60)
