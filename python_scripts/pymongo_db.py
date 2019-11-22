# Module creating and handling local MongosDB
from pymongo import MongoClient
import pymongo
from .secrets import mongos_secrets

client = MongoClient(mongos_secrets["host"], mongos_secrets["port"])
db = client["Hardwarescrape"]


def insert_reddit_submission_dict(submission: dict, collection):
    """
    Takes in submission dictionary created from submission object and inserts to mongodb
    :param submission: dictionary created from submission via PRAW
    :param collection: pymongo collection object to insert submission into
    :return: none
    """
    if not submission:
        return "Error, submission object is None"
    if collection.find_one({"post_id": submission["post_id"]}):
        print(f'post_id : {submission["post_id"]} is already in database!')
        return
    collection.insert_one(submission)


def init_db(
    collection: pymongo.collection.Collection = db.reddit, index_name: str = "post_id"
):
    """
    Creates an index for the collection. Intended to be used by running this module directly.
    :param collection_name: Name of the collection
    :param index_name: Name of the attribute to make an index
    :return: Nothing
    """

    collection.create_index([(index_name, pymongo.TEXT)], unique=True)


if __name__ == "__main__":
    init_db()
