import requests
import config

class LemmyClient:

    def create_comment(self, post_id: int, content: str, parent_id: int = None) -> dict:
        """
        Creates a comment on a Lemmy post.
        Args:
            post_id (int): The ID of the Lemmy post to comment on.
            content (str): The comment text.
            parent_id (int, optional): The parent comment's ID if this is a reply; otherwise, None.
        Returns:
            dict: The JSON response from the Lemmy API.
        """
        create_comment_endpoint = f"{self.base_url}/api/v3/comment"
        headers = {"Authorization": f"Bearer {self.jwt_token}"}
        payload = {
            "post_id": post_id,
            "content": content,
        }
        if parent_id is not None:
            payload["parent_id"] = parent_id

        response = requests.post(create_comment_endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
