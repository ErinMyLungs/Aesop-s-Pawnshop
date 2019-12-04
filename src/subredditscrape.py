import praw
import pandas as pd
from psaw import PushshiftAPI
from secrets import reddit_app_key, reddit_secret_key
from GPUNameScrape import pd_series_to_set
from pymongo_db import db, insert_reddit_submission_dict
import pymongo
import pathlib

reddit = praw.Reddit(
    client_id=reddit_app_key,
    client_secret=reddit_secret_key,
    user_agent="HardwareScrape",
)

psaw_api = PushshiftAPI(reddit)

clean_name_path = pathlib.Path.cwd().parent / "data/nvidia_clean_names.csv"

if clean_name_path.exists():
    nvidia_names = pd.read_csv(clean_name_path, index_col=0).rename(
        {"0": "name"}, axis=1
    )

gpu_name_set = pd_series_to_set(nvidia_names["name"])


def scrape_hws_psaw_style(
    gpu_name_set: set,
    psaw_api=psaw_api,
    limit: int = None,
    collection_name: str = "reddit",
):
    """
    Uses PSAW and PRAW to scrape reddit posts and insert submissions that match criteria into mongodb.
    :param gpu_name_set: set of strings to search - typically created by pd_series_to_set helper func
    :param psaw_api: psaw api object
    :param limit: number of submissions to fetch
    :return: None, prints number of posts processed
    """

    collection = db[collection_name]

    latest_document = collection.find_one(sort=[("created", pymongo.DESCENDING)])
    datetime = "365d"
    if latest_document:
        created = latest_document.get("created")
        if created:
            datetime = int(created)

    generator = psaw_api.search_submissions(
        subreddit="hardwareswap", after=datetime, limit=limit
    )  # scraping between 9/10/19 13:36 and 1/1/19 00:00

    posts_processed = 0
    posts_inserted = 0
    while True:
        if posts_processed % 50 == 0:
            print(f"{posts_processed} posts processed, {posts_inserted} inserted")
        try:
            submission_object = next(generator)
            submission_dict = None

            if submission_object.link_flair_text not in {"SELLING", "CLOSED"}:
                posts_processed += 1
                continue

            title = submission_object.title.split()
            for word in title:
                if word.lower() in gpu_name_set:

                    author_dict = None
                    if submission_object.author:
                        # TODO: Are there ways to improve this performance? I think this is causing hitching because when DNE, few second delay from hitting reddit api
                        author_dict = {
                            "author_id": submission_object.author_fullname,
                            "author_name": submission_object.author.name,
                            "author_trade_info": submission_object.author_flair_text,
                        }
                    submission_dict = {
                        "post_id": submission_object.id,
                        "title": submission_object.title,
                        "self_text": submission_object.selftext,
                        "created": submission_object.created,
                        "author_info": author_dict,
                    }
                    # TODO: Add break after success find? No need to re-query/acquire author info if matched once

            if not submission_dict:
                posts_processed += 1
                continue

            posts_processed += 1
            insert_reddit_submission_dict(submission_dict, collection)
            posts_inserted += 1
        except StopIteration:
            print(
                f"end of loop, {posts_processed} processed, {posts_inserted} inserted"
            )
            break


if __name__ == "__main__":
    scrape_hws_psaw_style(gpu_name_set=gpu_name_set, limit=None)
