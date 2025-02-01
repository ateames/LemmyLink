# lemmy_client.py

import requests
import config

class LemmyClient:
    def __init__(self):
        self.base_url = config.LEMMY_BASE_URL
        self.username = config.LEMMY_USERNAME
        self.password = config.LEMMY_PASSWORD
        self.jwt_token = None  # Will store the auth token after login

    def login(self):
        """
        Logs into Lemmy with the username/password from config and stores the JWT token.
        """
        login_endpoint = f"{self.base_url}/api/v3/user/login"
        payload = {
            "username_or_email": self.username,
            "password": self.password
        }

        try:
            response = requests.post(login_endpoint, json=payload)
            response.raise_for_status()
            json_data = response.json()

            # Lemmy returns: { "jwt": "<token>" } on success
            self.jwt_token = json_data["jwt"]
        except Exception as e:
            raise RuntimeError(f"Failed to login to Lemmy: {e}")

    def create_post(self, community_id: int, title: str, body: str = "") -> dict:
        """
        Creates a new post in Lemmy under the given community_id with the provided title and body.
        Returns the JSON response from Lemmy, which includes the post link/ID.
        """
        if not self.jwt_token:
            raise RuntimeError("No JWT token found. Call login() first.")

        create_post_endpoint = f"{self.base_url}/api/v3/post"
        headers = {
            "Authorization": f"Bearer {self.jwt_token}"
        }
        payload = {
            "community_id": community_id,
            "name": title,
            "body": body
        }

        try:
            response = requests.post(create_post_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()  # Should contain "post": {...}
        except Exception as e:
            raise RuntimeError(f"Failed to create post on Lemmy: {e}")

    def create_comment(self, post_id: int, content: str, parent_id: int = None) -> dict:
        """
        Creates a comment on a Lemmy post.
        Args:
            post_id (int): The Lemmy post ID to comment on.
            content (str): The text of the comment.
            parent_id (int, optional): The parent comment's ID if replying; otherwise, None.
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

    def get_comments(self, post_id: int) -> list:
        """
        Retrieves comments for a given Lemmy post.
        Returns a list of comment dicts. If the post isn't found, returns an empty list.
        """
        get_comments_endpoint = f"{self.base_url}/api/v3/post/comments"
        params = {"post_id": post_id}
        headers = {"Authorization": f"Bearer {self.jwt_token}"}
        response = requests.get(get_comments_endpoint, params=params, headers=headers)
        if response.status_code == 404:
            print(f"Warning: Post {post_id} not found on Lemmy (404 returned).")
            return []
        response.raise_for_status()
        json_data = response.json()
        return json_data.get("comments", [])
