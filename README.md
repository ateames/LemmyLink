# LemmyLink Bot

LemmyLink is a cross-platform bridge bot that connects Reddit and specific Lemmy communities. When a user triggers the bot on Reddit by including the phrase **"LemmyLink!"** in a comment, the bot creates a corresponding post on your Lemmy instance and replies on Reddit with the link to that post.

## Features

- **Reddit Trigger:** Listens for the "LemmyLink!" phrase in Reddit comments.
- **Lemmy Post Creation:** Automatically creates a corresponding post on a Lemmy instance e.g. https://lemmy.world/c/lemmylink
- **Mapping Database:** Maintains SQLite-based mappings for both posts and comments to avoid duplicate syncing.
- **Bidirectional Comment Sync:** WORK IN PROGRESS: Synchronizes new comments between Reddit and Lemmy (for now, as top-level comments).

**If you implement this, PLEASE MARK YOUR ACCOUNT AS A BOT ACCOUNT IN LEMMY!**

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ateames/LemmyLink.git
   cd lemmylink_bot

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Configuration:**
Update the `config.py` file with your credentials and settings. For example:

   ```bash
    # Reddit credentials (get these from https://www.reddit.com/prefs/apps)
    REDDIT_CLIENT_ID = "YOUR_CLIENT_ID"
    REDDIT_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
    REDDIT_USERNAME = "YOUR_BOT_USERNAME"
    REDDIT_PASSWORD = "YOUR_BOT_PASSWORD"
    REDDIT_USER_AGENT = "LemmyLinkBot/0.1 by /u/YOUR_BOT_USERNAME"

    # Lemmy credentials and instance settings
    LEMMY_BASE_URL = "https://your-lemmy-instance.example"
    LEMMY_USERNAME = "your_lemmy_bot_username"
    LEMMY_PASSWORD = "your_lemmy_bot_password"
    LEMMY_COMMUNITY_ID = 1  # The community ID where posts will be created

5. **Database Setup:**
The project uses SQLite for storing mappings between Reddit and Lemmy content.
Run these commands once to create the required tables:
    ```bash
    python mapping_db.py
    python comment_mapping_db.py
This will create a `mapping.db` file in your project directory with the necessary tables.

## Running the Bot
There are two main components:
1. **Trigger Listener:**
Run `main.py` to start the Reddit listener that detects the "LemmyLink!" trigger, creates a corresponding Lemmy post, and replies on Reddit:
    ```bash
    python main.py

2. **Bidirectional Comment Sync:**
Run `bidirectional_sync.py` in a separate terminal (or as a background process) to synchronize comments between Reddit and Lemmy:
    ```bash
    python bidirectional_sync.py

## License 
This project is licensed under the <a href="https://opensource.org/license/mit" target="_blank">MIT License.</a> 
