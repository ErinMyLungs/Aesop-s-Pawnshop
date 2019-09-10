# Module to scrape wikipedia tables for GPU names and helper functions
import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_gpu_names_wikipedia(url: str, csv_filepath: str, return_dataframe=False):
    """
    Scrapes wikipedia url taking the first column string and dumps the text into a csv file
    :param url: url string for wikipedia page to be scraped. Only tested with gpu pages!!
    :param csv_filepath: CSV filepath to dump to.
    :param return_dataframe: If true returns pandas df of names for manipulation.
    :return: Dumped CSV file
    """
    # TODO: Improve so this only scrapes between two sibling tags?
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Response is invalid! Error: {response.status_code}")

    soup = BeautifulSoup(response.content, "html5lib")
    names = soup.find_all(
        "th", style="text-align:left;"
    )  # th tags with this style yield gpu names

    gpu_names_dataframe = pd.DataFrame([name.text for name in names])
    gpu_names_dataframe.to_csv(csv_filepath)

    if return_dataframe:
        return gpu_names_dataframe


def name_cleanup(name: str, char_search_list=["(", "[", "{", "*"]):
    """
    Slices string to instance of character in search list. Assumes all info to the right of the left-most char found is garbage.
    :param name: string to cleanup, used often with single values from pd series with applymap
    :param char_search_list: list of single characters to search for
    :return: string cleaned up and stripped
    """
    idx = None
    name = name.replace("\xa0", " ")
    for char in char_search_list:

        potential_index = name.find(char)

        if potential_index != -1 and idx:
            idx = min(idx, potential_index)

        elif potential_index != -1 and not idx:
            idx = potential_index

    if idx:
        return name[:idx].strip()
    return name.strip()


def remove_adjectives_from_names(name: str):
    """
    Replaces all weird adjectives with blank space so the set isn't cluttered with adjectives that are unhelpful
    :param name: name to remove adjectives from
    :return: cleaned name
    """
    bad_list = [
        "Black",
        "Boost",
        "Core 216",
        "448 Cores",
        "DDR2",
        "Edition",
        "Green",
        "rev.2",
        "rev.3",
        "Ultra",
        "Rev. 2",
        "Rev. 3",
        "192-bit",
    ]
    for adj in bad_list:
        name = name.replace(adj, "")
    return name.strip()


def pd_series_to_set(series):
    """
    Takes in pd series (or col of dataframe) and returns a set of the name parts that are greater than len 1
    :param series: pd series of strings
    :return: set of unique words in entire column
    """
    result_set = set()
    for value in series:
        holder_set = {item for item in value.split()}
        for string in holder_set:
            if len(string) > 2:
                result_set.add(remove_adjectives_from_names(string).lower())
    return result_set


def prior_main_call():
    nvidia_url = (
        "https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units"
    )
    nvidia_raw_csv = (
        "/home/erin/PycharmProjects/HardwareScrape/data/nvidia_gpu_names.csv"
    )
    nvidia_cleaned_csv = (
        "/home/erin/PycharmProjects/HardwareScrape/data/nvidia_clean_names.csv"
    )
    nv_df = scrape_gpu_names_wikipedia(
        nvidia_url, nvidia_raw_csv, return_dataframe=True
    )
    nv_df.rename({"0": "name"}, axis=1, inplace=True)
    nv_df = nv_df.applymap(lambda x: name_cleanup(x))
    nv_df.to_csv(nvidia_cleaned_csv)


if __name__ == "__main__":
    pass
    # TODO: Get this working for webscraping amd card names
    # amd_url = 'https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units'
    # amd_csv = '/home/erin/PycharmProjects/HardwareScrape/data/amd_gpu_names.csv'
    # df = scrape_gpu_names_wikipedia(amd_url, amd_csv, True)
