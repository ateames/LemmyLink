# bridge_manager.py

from lemmy_client import LemmyClient
import config
from mapping_db import insert_mapping  # Import our mapping helper

class BridgeManager:
    """
    The BridgeManager encapsulates logic to 'bridge' a Reddit thread to Lemmy.
    For this MVP, it creates a new post on Lemmy when triggered and then replies on Reddit.
    """

    def __init__(self):
        # Initialize and login to Lemmy
        self.lemmy_client = LemmyClient()
        self.lemmy_client.login()
        print("BridgeManager: Logged in to Lemmy.")

    def handle_trigger(self, comment):
        """
        Called when 'LemmyLink!' is detected in a Reddit comment.
        This function:
         - Creates a corresponding post on Lemmy using the triggering comment's text.
         - Replies on Reddit with the Lemmy post link.
        """
        # Gather info from the Reddit submission and the triggering comment
        submission = comment.submission
        
        # Use the triggering comment text for the post title (limit length)
        triggered_title = (
            comment.body.strip()[:50] + "..."
            if len(comment.body.strip()) > 50
            else comment.body.strip()
        )
        
        # Craft a body that uses the comment text instead of the submission selftext.
        body_text = (
            f"Reddit user /u/{comment.author} triggered a LemmyLink! Bot\n\n"
            f"**Triggered Comment:**\n\n"
            f"> {comment.body}\n\n"
            f"**Original Reddit Thread:** {submission.url or submission.shortlink}\n\n"
            f"Submission Title: {submission.title}"
        )
        
        # Create the post on Lemmy
        community_id = config.LEMMY_COMMUNITY_ID  # from config.py
        try:
            post_response = self.lemmy_client.create_post(
                community_id=community_id,
                title=triggered_title,
                body=body_text
            )
            print(f"BridgeManager: Lemmy post response: {post_response}")
        
            # Extract post ID from the nested response
            post_view = post_response.get("post_view", {})
            post_data = post_view.get("post", {})
            if post_data and "id" in post_data:
                new_post_id = post_data["id"]
                lemmy_post_url = f"{config.LEMMY_BASE_URL}/post/{new_post_id}"
            
                # Store mapping: submission ID, trigger comment ID, and Lemmy post ID.
                mapping_id = insert_mapping(submission.id, comment.id, new_post_id)
                print(f"BridgeManager: Mapping record created with ID {mapping_id}")
        
                # Reply on Reddit with the Lemmy post link
                reply_text = (
                    "LemmyLink bot here!\n\n"
                    f"I've created a corresponding post on Lemmy: {lemmy_post_url}\n\n"
                    "Stay tuned for future updates (comment syncing, etc.)!"
                )
                comment.reply(reply_text)
                print(f"BridgeManager: Replied to comment {comment.id} with Lemmy link {lemmy_post_url}")
            else:
                print(f"[ERROR] BridgeManager: Could not find 'id' in Lemmy post response: {post_response}")
        
        except Exception as e:
            print(f"[ERROR] BridgeManager: Failed to create Lemmy post or reply on Reddit: {e}")
