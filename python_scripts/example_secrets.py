# Contains reddit secrets for scraping posts/subreddits
import random
import string

reddit_secret_key = (
    f"{''.join(random.choices(string.ascii_letters + string.digits, k=27))}"
)
reddit_app_key = f"{''.join(random.choices(string.ascii_letters+ string.digits, k=14))}"

# These keys are NOT valid for reddit scraping. Register your app on reddit.com/prefs/apps/ as a personal use script
# and get the app and secret key from there and replace the f strings with your personal key.

if __name__ == "__main__":
    print(reddit_secret_key)
    print(reddit_app_key)
