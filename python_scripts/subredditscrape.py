import praw
from secrets import reddit_app_key, reddit_secret_key
import pandas as pd

reddit = praw.Reddit(
    client_id=reddit_app_key,
    client_secret=reddit_secret_key,
    user_agent="HardwareScrape",
)

holder_list = list(pd.read_csv('/home/erin/PycharmProjects/HardwareScrape/data/nvidia_clean_names.csv', index_col=0)['0'])
gpu_name_set = { x.replace(u'\xa0', u' ').split() for x in holder_list}

hardware_new = reddit.subreddit("HardwareSwap").new()

for submission in hardware_new:
    title = submission.title.split()
    for word in title:
        if word in gpu_name_set:
            print(submission.title)

# this currently doens't work, we should separate the name_set more so that it includes geforce, numbers, and things like that separately
