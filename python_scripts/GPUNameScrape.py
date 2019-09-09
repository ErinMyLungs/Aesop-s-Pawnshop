import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_gpu_names_wikipedia(url:str, csv_filepath:str, return_dataframe=False):
    """
    Scrapes wikipedia url taking the first column string and dumps the text into a csv file
    :param url: url string for wikipedia page to be scraped. Only tested with gpu pages!!
    :param csv_filepath: CSV filepath to dump to.
    :param return_dataframe: If true returns pandas df of names for manipulation.
    :return: Dumped CSV file
    """
    response = requests.get(url)
    if response.status_code != 200:
        print(f'Response is invalid! Error: {response.status_code}')

    soup = BeautifulSoup(response.content, 'html5lib')
    names = soup.find_all('th', style='text-align:left;') # th tags with this style yield gpu names

    gpu_names_dataframe = pd.DataFrame([name.text for name in names])
    gpu_names_dataframe.to_csv(csv_filepath)

    if return_dataframe:
        return gpu_names_dataframe


def name_cleanup(name:str):
    char_search_list = ['(', '[', '{']
    idx = None
    for char in char_search_list:
        potential_index = name.find(char)
        if potential_index != -1 and idx:
            idx = min(idx, potential_index)
        elif potential_index != -1 and not idx:
            idx = potential_index

    if idx:
        return name[:idx].strip()
    return name.strip()

def pd_series_to_set(series):
    result_set = set()
    for value in series:
        holder_set = {item for item in value.split()}
        for string in holder_set:
            result_set.add(string)
    return result_set

if __name__ == '__main__':
    nvidia_url = 'https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units'
    nvidia_raw_csv = '/home/erin/PycharmProjects/HardwareScrape/data/nvidia_gpu_names.csv'
    nvidia_cleaned_csv = '/home/erin/PycharmProjects/HardwareScrape/data/nvidia_clean_names.csv'
    nv_df = scrape_gpu_names_wikipedia(nvidia_url, nvidia_raw_csv, return_dataframe=True)
    nv_df.rename({'0': 'name'}, axis=1, inplace=True)
    nv_df = nv_df.applymap(lambda x: name_cleanup(x))
    nv_df.to_csv(nvidia_cleaned_csv)
    # TODO: Get this working for webscraping amd card names
    # amd_url = 'https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units'
    # amd_csv = '/home/erin/PycharmProjects/HardwareScrape/data/amd_gpu_names.csv'
    # df = scrape_gpu_names_wikipedia(amd_url, amd_csv, True)