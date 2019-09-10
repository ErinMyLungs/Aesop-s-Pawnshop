import praw
from psaw import PushshiftAPI
from secrets import reddit_app_key, reddit_secret_key
import pandas as pd
from GPUNameScrape import pd_series_to_set
from pymongo_db import db, insert_reddit_submission_dict

reddit = praw.Reddit(
    client_id=reddit_app_key,
    client_secret=reddit_secret_key,
    user_agent="HardwareScrape",
)

psaw_api = PushshiftAPI(reddit)

nvidia_names = pd.read_csv(
    "/home/erin/PycharmProjects/HardwareScrape/data/nvidia_clean_names.csv", index_col=0
).rename({"0": "name"}, axis=1)
gpu_name_set = pd_series_to_set(nvidia_names["name"])


def scrape_hws_psaw_style(gpu_name_set: set, psaw_api=psaw_api, limit: int = None):
    """
    Uses PSAW and PRAW to scrape reddit posts and insert submissions that match criteria into mongodb.
    :param gpu_name_set: set of strings to search - typically created by pd_series_to_set helper func
    :param psaw_api: psaw api object
    :param limit: number of submissions to fetch
    :return: None, prints number of posts processed
    """
    generator = psaw_api.search_submissions(subreddit='hardwareswap', before=1568147665, after=1546300800,
                                            limit=limit)  # scraping between 9/10/19 13:36 and 1/1/19 00:00
    posts_processed = 0
    while True:
        try:
            submission_object = next(generator)
            submission_dict = None

            if submission_object.link_flair_text not in {"SELLING", "CLOSED"}:
                posts_processed += 1
                continue

            title = submission_object.title.split()
            for word in title:
                if word.lower() in gpu_name_set:
                    submission_dict = {'_id': submission_object.id,
                                       'title': submission_object.title,
                                       'self_text': submission_object.selftext,
                                       'created': submission_object.created,
                                       'author_info': {'author_id': submission_object.author_fullname,
                                                       'author_name': submission_object.author.name,
                                                       'author_trade_info': submission_object.author_flair_text}
                                       }

            if not submission_dict:
                posts_processed +=1
                continue

            posts_processed += 1
            insert_reddit_submission_dict(submission_dict)

        except StopIteration:
            print(f'end of loop, {posts_processed} processed')
            break


def scrape_hws_new(gpu_name_set: set, limit: int = None):
    """
    Goes through /r/hardwareswap/new and checks the title for any words to be in the name set AND is a selling post.
    :param gpu_name_set: Set of GPU model words. nvidia, gtx, 1050 etc.
    :param limit: How many submissions to check. When None, treats as limit=1000
    :return: list of submission objects from PRAW
    """
    hardware_new = reddit.subreddit("HardwareSwap").new(limit=limit)
    result_list = list()
    for submission in hardware_new:
        title = submission.title.split()
        for word in title:
            if word.lower() in gpu_name_set and submission.link_flair_text in {"SELLING", "CLOSED"}:
                print(submission.title)
                result_list.append(submission)
                break
    return result_list


if __name__ == "__main__":
    scrape_hws_psaw_style(gpu_name_set=gpu_name_set, limit=10)
