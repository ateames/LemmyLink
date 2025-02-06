# bridge_manager.py

from lemmy_client import LemmyClient
import config
from mapping_db import insert_mapping

class BridgeManager:
    """
    The BridgeManager encapsulates logic to 'bridge' a Reddit thread (post or comment) to Lemmy.
    It creates a new post on Lemmy when triggered and then replies on Reddit.
    """

    def __init__(self):
        self.lemmy_client = LemmyClient()
        self.lemmy_client.login()
        print("BridgeManager: Logged in to Lemmy.")

    def handle_trigger(self, trigger):
        """
        Called when "LemmyLink!" is detected in a Reddit submission or comment.
        This function:
         - Creates a corresponding post on Lemmy.
         - Replies on Reddit with the Lemmy post link.
         - Stores a mapping between the Reddit submission and the Lemmy post.
        """
        # Determine if trigger is a submission or a comment.
        # For a submission, it has attributes like 'selftext' and 'title'.
        # For a comment, it has a 'body' attribute.
        if hasattr(trigger, "selftext"):
            # It's a submission trigger.
            submission = trigger
            reddit_post_title = submission.title
            trigger_text = submission.selftext
            reddit_trigger_id = submission.id  # Use the submission id as the trigger ID.
        elif hasattr(trigger, "body"):
            # It's a comment trigger.
            submission = trigger.submission
            reddit_post_title = submission.title
            trigger_text = trigger.body
            reddit_trigger_id = trigger.id
        else:
            print("Unknown trigger type; skipping.")
            return

        # You can combine the post link and title into a single markdown link.
        post_link_line = f"**Original Reddit Post:** [{submission.title}]({submission.url or submission.shortlink})"

        # Construct the body text for the Lemmy post.
        body_text = (
            f"Reddit user /u/{trigger.author} triggered a Lemmy link!\n\n"
            f"{post_link_line}\n\n"
            f"**Triggered Content:**\n\n"
            f"> {trigger_text}\n\n"
            f"Link to Comment: https://www.reddit.com{trigger.permalink}"
        )

        # Create the post on Lemmy.
        community_id = config.LEMMY_COMMUNITY_ID
        try:
            post_response = self.lemmy_client.create_post(
                community_id=community_id,
                title=reddit_post_title,
                body=body_text
            )
            print(f"BridgeManager: Lemmy post response: {post_response}")

            # Extract the post ID (using your existing logic).
            post_view = post_response.get("post_view", {})
            post_data = post_view.get("post", {})
            if post_data and "id" in post_data:
                new_post_id = post_data["id"]
                lemmy_post_url = f"{config.LEMMY_BASE_URL}/post/{new_post_id}"

                # Store the mapping.
                # Note: your mapping table has columns for reddit_submission_id and reddit_trigger_comment_id.
                # For a submission trigger, you can store the submission id in both fields or set the trigger comment field to NULL.
                mapping_id = insert_mapping(submission.id, reddit_trigger_id, new_post_id)
                print(f"BridgeManager: Mapping record created with ID {mapping_id}")

                # Reply on Reddit with the Lemmy post link.
                reply_text = (
                    "LemmyLink bot here!\n\n"
                    f"I've created a corresponding post on Lemmy: {lemmy_post_url}\n\n"
                    "Stay tuned for future updates (e.g., comment syncing)!"
                )
                trigger.reply(reply_text)
                print(f"BridgeManager: Replied to trigger {reddit_trigger_id} with Lemmy link {lemmy_post_url}")
            else:
                print(f"[ERROR] BridgeManager: Could not find 'id' in Lemmy post response: {post_response}")

        except Exception as e:
            print(f"[ERROR] BridgeManager: Failed to create Lemmy post or reply on Reddit: {e}")
