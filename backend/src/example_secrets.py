# Contains reddit secrets and database connection info
import string
import random

reddit_secret_key = (
    f"{''.join(random.choices(string.ascii_letters + string.digits, k=27))}"
)
reddit_app_key = f"{''.join(random.choices(string.ascii_letters+ string.digits, k=14))}"

# These keys are NOT valid for reddit scraping. Register your app on reddit.com/prefs/apps/ as a personal use script
# and get the app and secret key from there and replace the f strings with your personal key.

mongos_secrets = {
    "host": "localhost",
    "port": 27017,
}  # If your mongoserver is local, default values are fine.

if __name__ == "__main__":
    print(reddit_secret_key)
    print(reddit_app_key)
    print(mongos_secrets)
