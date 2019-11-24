# module for searching and pulling out pricing data from mongo documents
import pymongo
from .pymongo_db import db
import re
import pickle
from typing import Union
import pandas as pd
import numpy as np
import os


def pull_pricing_draft(
    comparison_set: set,
    bad_set: set,
    collection_name: str = "reddit",
    limit: Union[None, int] = 10,
):
    """
    Goes through collection attempting to pull out pricing data for each entry and discarding entries that are unlikely to have gpus
    :param comparison_set: key terms to match
    :param bad_set: key terms to avoid
    :param collection_name: mongo collection name
    :param limit: how many entries to check. None returns all
    :return: dataframe of data
    """
    collection = db[collection_name]
    if limit:
        cursor = collection.find(limit=limit)
    else:
        cursor = collection.find()
    # regex_2 = re.compile(r'\$(\d{2,3})+.?(shipp)?(ed|ing)?(OBO)?', re.IGNORECASE) #Searches for $ two or 3 numbers and shipp (ing or ed) or OBO optional.
    regex = re.compile(r"\$(\d{2,3})+", re.IGNORECASE)
    power_count = 0
    entries_count = 0
    result_df = pd.DataFrame(
        columns=[
            "title_select",
            "selected_text",
            "full_text",
            "full_title",
            "location_tag",
            "post_id",
            "author_id",
            "author_trades",
            "created",
        ]
    )

    for submission in cursor:
        entries_count += 1

        title = submission["title"].lower()
        text = submission["self_text"].lower()

        if text.find("removed") != -1 or text.find("deleted") != -1:
            continue

        if len(regex.findall(text)) != 1:
            continue

        match_set, selling_title_substring, power = gpu_likelihood_value(
            title, comparison_set, bad_set
        )

        if power <= 2:
            continue

        power_count += 1

        high_idx, low_idx = search_for_price_regex(match_set, regex, text)

        result_df = append_results_to_df(
            high_idx, low_idx, selling_title_substring, submission, text, result_df
        )

    print(f"total entries: {entries_count}")
    print(f"entries over power 2: {power_count}")
    return result_df


def append_results_to_df(
    high_idx, low_idx, selling_title_substring, submission, text, df
):
    """
    Appends parsed results to df as new row
    :param high_idx:
    :param low_idx:
    :param selling_title_substring:
    :param submission:
    :param text:
    :param df:
    :return:
    """
    result_dict = {
        "title_select": selling_title_substring,
        "selected_text": text[low_idx:high_idx],
        "full_text": submission["self_text"],
        "full_title": submission["title"],
        "location_tag": submission["title"][: submission["title"].find("]") + 1],
        "post_id": submission["post_id"],
        "author_id": None,
        "author_trades": None,
        "created": submission["created"],
    }
    if submission.get("author_info"):
        result_dict["author_id"] = submission["author_info"]["author_id"]
        result_dict["author_trades"] = submission["author_info"]["author_trade_info"]
    df = df.append(result_dict, ignore_index=True)
    return df


def search_for_price_regex(match_set, regex, text):
    low_idx = 0
    high_idx = None
    # for search_term in match_set:
    #     potential_idx = text.find(search_term)
    #     term_found = potential_idx != -1
    #     if term_found and not low_idx:
    #         low_idx = potential_idx  # set low_idx if it doesn't exist
    #     if term_found and low_idx:
    #         low_idx = min(term_found, low_idx)  # take the left most term
    # if not low_idx:
    #     low_idx = 0
    regex_match = regex.search(text, low_idx)
    if regex_match:
        high_idx = regex_match.end()

        # if low_idx == 0:
        low_idx = regex_match.start()
    return high_idx, low_idx


def gpu_likelihood_value(title: str, comparison_set: set, bad_set: set = None):
    """
    Creates an int value to weight how likely a post has a gpu based on how many matches in set and how important the match is
    :param title: title of set
    :param comparison_set: comparison set to check against
    :return: the matching words, selling substring, power num tuple
    """
    # TODO: Maybe try splitting title by commas and parse each individually to handle multiitem posts? Future magic
    selling_title_substring = title[title.find("[h]") + 3 : title.find("[w]")]
    title_set = set(selling_title_substring.split())
    match_set = title_set & comparison_set
    unmatch_set = title_set & bad_set
    power_num = len(match_set) - len(unmatch_set)
    return match_set, selling_title_substring, power_num


def load_comparison_pickle(
    comparison_filepath: str = "data/comp_set_pickle.P",
    bad_filepath: str = "data/bad_set.P",
):
    """
    loads comparison set pickle from filepath
    :param comparison_filepath: filepath to comparison pickle, by default in data folder
    :param bad_filepath: filepath to bad set pickle, default in data folder
    :return: set object
    """
    if not os.path.exists(comparison_filepath):
        raise ValueError(f"Error, filepath {comparison_filepath} does not exist")
    if not os.path.exists(bad_filepath):
        raise ValueError(f"Error, filepath {bad_filepath} does not exist")

    with open(comparison_filepath, "rb") as pickle_file:
        comparison_set = pickle.load(pickle_file)

    with open(bad_filepath, "rb") as pickle_file:
        bad_set = pickle.load(pickle_file)

    return comparison_set, bad_set


def create_price_column(
    dataframe: pd.core.frame.DataFrame,
    column_name: str = "selected_text",
    target_column: str = "price",
):
    """
    Uses regex to parse out price and turn to int for easy statistics
    :param dataframe: dataframe of GPU information
    :param column_name: string column (object) to parse
    :param target_column: column to create
    :return: dataframe with new target column created
    """
    dataframe.loc[:, target_column] = dataframe.loc[:, column_name].map(
        lambda x: int(x[x.find("$") + 1 :])
    )
    return dataframe


def extract_model_information(dataframe: pd.core.frame.DataFrame):
    """
    Create df with model and ti status returned
    :param dataframe:
    :return: dataframe with two new columns
    """
    model_info_frame = dataframe.title_select.str.extract(
        pat=r"(\d{3,4})[^(4790k)](ti)?", flags=re.IGNORECASE
    )
    dataframe = pd.concat([dataframe, model_info_frame], axis=1)
    dataframe = dataframe.rename(columns={0: "model", 1: "is_ti"})

    dataframe.loc[:, "is_ti"] = dataframe.is_ti.notna()
    dataframe.loc[:, "model"] = dataframe.model.astype(int)

    return dataframe


def extract_trades_info(dataframe):
    """
    Extracts trade number and sets NaNs to 0 (assumes no trades)
    :param dataframe: dataframe to transform
    :return: dataframe with 'trades' column
    """
    trades = dataframe.author_trades.str.extract(pat=r"(\d{1,3})")
    dataframe = pd.concat([dataframe, trades], axis=1).rename(columns={0: "trades"})
    dataframe.loc[:, "trades"] = dataframe.trades.map(
        lambda x: int(x) if not np.isnan(float(x)) else 0
    )
    return dataframe


def front_end_data_cleanup(dataframe):
    # TODO: Clean and refactor this up so it's a lot more presentable
    dataframe = create_price_column(dataframe)
    dataframe = extract_model_information(dataframe)
    dataframe = extract_trades_info(dataframe)
    return dataframe


if __name__ == "__main__":

    comparison_set, bad_set = load_comparison_pickle()
    # if not comparison_set:
    # TODO: Can this be setup so if the pickle fails to load it'll throw an error and stop the execution?
    df = pull_pricing_draft(comparison_set, bad_set=bad_set, limit=None)
