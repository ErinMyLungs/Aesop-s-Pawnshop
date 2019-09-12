# module for searching and pulling out pricing data from mongo documents
import pymongo
from pymongo_db import db
import re
import pickle
from typing import Union
import pandas as pd
# $\d\d\d shipped
# $\d\d\d + shipping
# asking $\d\d\d shipped
# asking $\d\d\d after shipping and fees
# asking $\d\d\d OBO
# \nNAMEOFPRODUCT | $\d\d\d

def pull_pricing_draft(comparison_set: set, bad_set: set, collection_name: str='reddit', limit: Union[None,int]=10):
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
    regex = re.compile(r'\$(\d{2,3})+.?(shipp)?(ed|ing)?(OBO)?', re.IGNORECASE) #Searches for $ two or 3 numbers and shipp (ing or ed) or OBO optional.

    power_count = 0
    entries_count = 0

    empty_df = pd.DataFrame(
        columns=['title_select', 'selected_text', 'full_text', 'location_tag', 'post_id', 'author_id', 'author_trades', 'created'])

    for submission in cursor:
        entries_count +=1

        title = submission['title'].lower()
        text = submission['self_text'].lower()

        if text.find('removed') != -1 or text.find('deleted') != -1:
            continue

        match_set, selling_title_substring, power = gpu_likelihood_value(title, comparison_set, bad_set)

        if power <= 2:
            continue

        power_count +=1
        low_idx = None
        high_idx = None
        for search_term in match_set:
            potential_idx = text.find(search_term)
            term_found = potential_idx != -1
            if term_found and not low_idx:
                low_idx = potential_idx #set low_idx if it doesn't exist
            if term_found and low_idx:
                low_idx = min(term_found, low_idx) #take the left most term

        if not low_idx:
            low_idx = 0

        regex_match = regex.search(text, low_idx)
        if regex_match:
            high_idx = regex_match.end()

            if low_idx ==0:
                low_idx = regex_match.start()
        empty_dict = {'title_select': selling_title_substring,
                            'selected_text': text[low_idx:high_idx],
                            'full_text': submission['self_text'],
                            'location_tag': submission['title'][:8],
                            'post_id': submission['post_id'],
                            'author_id': None,
                            'author_trades': None,
                            'created': submission['created']}
        if submission.get('author_info'):
            empty_dict['author_id'] = submission['author_info']['author_id']
            empty_dict['author_trades'] = submission['author_info']['author_trade_info']

        empty_df = empty_df.append(empty_dict, ignore_index=True)

    print(f'total entries: {entries_count}')
    print(f'entries over power 2: {power_count}')
    return empty_df

def gpu_likelihood_value(title: str, comparison_set: set, bad_set: set=None):
    """
    Creates an int value to weight how likely a post has a gpu based on how many matches in set and how important the match is
    :param title: title of set
    :param comparison_set: comparison set to check against
    :return: the matching words, selling substring, power num tuple
    """
    # TODO: Maybe try splitting title by commas and parse each individually to handle multiitem posts? Future magic
    selling_title_substring = title[title.find('[h]') + 3: title.find('[w]')]
    title_set = set(selling_title_substring.split())
    match_set = title_set & comparison_set
    unmatch_set = title_set & bad_set
    power_num = len(match_set) - len(unmatch_set)
    return match_set, selling_title_substring, power_num

def load_comparison_pickle(filepath: str='/home/erin/PycharmProjects/HardwareScrape/data/comp_set_pickle.P'):
    """
    loads comparison set pickle from filepath
    :param filepath:
    :return: set object
    """
    with open(filepath, 'rb') as pickle_file:
        comparison_set = pickle.load(pickle_file)
    with open('/home/erin/PycharmProjects/HardwareScrape/data/bad_set.P', 'rb') as pickle_file:
        bad_set = pickle.load(pickle_file)
    return comparison_set, bad_set


if __name__ == '__main__':

    comparison_set, bad_set = load_comparison_pickle()
    # if not comparison_set:
    # TODO: Can this be setup so if the pickle fails to load it'll throw an error and stop the execution?
    df = pull_pricing_draft(comparison_set, bad_set=bad_set, limit=None)