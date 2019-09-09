from python_scripts import secrets
import praw
import datetime
from .secrets import reddit_app_key, reddit_secret_key

reddit = praw.Reddit(
    client_id=reddit_app_key,
    client_secret=reddit_secret_key,
    user_agent="HardwareScrape",
)

hardware_new = reddit.subreddit("HardwareSwap").new(limit=1)


def cutoff_date_comparison(submission_object, delta=183):
    """
    Returns UTC Date of specified days in the past for comparison of post age.
    :param days: Int of days in the past
    :return: UTC date stamp
    """
    # time_delta = days * 24 * 60 * 60 # Dimensional analysis to convert days to seconds
    submission_date = datetime.date.fromtimestamp(submission_object.created_utc)
    current_date = datetime.date.today()
    return current_date - submission_date < datetime.timedelta(days=delta)


for submission in hardware_new:
    if cutoff_date_comparison(submission_object=submission):
        print(submission.title, datetime.datetime.fromtimestamp(submission.created_utc))
        print(submission.link_flair_text)
        print(submission.selftext)
print("Search complete")

