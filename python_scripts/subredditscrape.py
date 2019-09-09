import praw
from secrets import reddit_app_key, reddit_secret_key
import pandas as pd
from GPUNameScrape import pd_series_to_set

reddit = praw.Reddit(
    client_id=reddit_app_key,
    client_secret=reddit_secret_key,
    user_agent="HardwareScrape",
)

nvidia_names = pd.read_csv('/home/erin/PycharmProjects/HardwareScrape/data/nvidia_clean_names.csv', index_col=0).rename({'0':'name'}, axis=1)
gpu_name_set = pd_series_to_set(nvidia_names['name'])


def scrape_hws_new(limit=None):
    hardware_new = reddit.subreddit("HardwareSwap").new(limit=limit)
    result_list = list()
    for submission in hardware_new:
        title = submission.title.split()
        for word in title:
            if word in gpu_name_set and submission.link_flair_text == 'SELLING':
                print(submission.title)
                result_list.append(submission)
                break
    return result_list

if __name__ == '__main__':
    result_list = scrape_hws_new(limit=1000)