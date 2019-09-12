# module for searching and pulling out pricing data from mongo documents
import pymongo
from pymongo_db import db
import re
import pickle
from typing import Union
# $\d\d\d shipped
# $\d\d\d + shipping
# asking $\d\d\d shipped
# asking $\d\d\d after shipping and fees
# asking $\d\d\d OBO
# \nNAMEOFPRODUCT | $\d\d\d

def pull_pricing_draft(comparison_set: set, bad_set: set, collection_name: str='reddit', limit: Union[None,int]=10):
    collection = db[collection_name]
    if limit:
        cursor = collection.find(limit=limit)
    else:
        cursor = collection.find()
    regex = re.compile(r'\$(\d{2,3})+.?(shipp)?(ed|ing)?(OBO)?', re.IGNORECASE) #Searches for $ two or 3 numbers and shipp (ing or ed) or OBO optional.

    power_count = 0
    entries_count = 0
    for submission in cursor:
        entries_count +=1
        title = submission['title'].lower()

        text = submission['self_text'].split('\n')
        match_set, selling_title_substring, power = gpu_likelihood_value(title, comparison_set, bad_set)
        if power > 3:
            power_count +=1
            # print(match_set)
            # print(selling_title_substring)
            # print(f'power: {power}')
            # print()
    print(f'total entries: {entries_count}')
    print(f'entries over power 2: {power_count}')

    
def gpu_likelihood_value(title: str, comparison_set: set, bad_set: set=None):
    """
    Creates an int value to weight how likely a post has a gpu based on how many matches in set and how important the match is
    :param title: title of set
    :param comparison_set: comparison set to check against
    :return: the matching words, selling substring, power num tuple
    """
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
    pull_pricing_draft(comparison_set, bad_set=bad_set, limit=None)