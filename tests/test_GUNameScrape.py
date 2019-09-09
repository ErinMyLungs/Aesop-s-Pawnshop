# Tests the GPUNameScrape.py module
import pytest
import pandas as pd
import python_scripts.GPUNameScrape as gp

test_name_list = [
    "GeForce 9300 GS[15]",
    "GeForce 8800 GT (G92)",
    "GeForce GTX 1080 (Notebook)[149]",
    "V100 GPU accelerator (mezzanine)[188][189][190]",
    "Nvidia TITAN\xa0RTX"
]


def test_name_cleanup():
    result_list = [
        "GeForce 9300 GS",
        "GeForce 8800 GT",
        "GeForce GTX 1080",
        "V100 GPU accelerator",
        "Nvidia TITAN RTX"
    ]
    assert [gp.name_cleanup(name) for name in test_name_list] == result_list

    assert [
        gp.name_cleanup(name, char_search_list=[]) for name in test_name_list
    ] == [value.replace(u'\xa0', ' ').strip() for value in test_name_list] # These are funcs applied to all values regardless of if any chars are searched/found.


def test_pd_series_to_set():
    test_df = pd.DataFrame(test_name_list, columns=["name"])
    test_series = pd.Series(test_name_list)
    result_set = {
        "(G92)",
        "(Notebook)[149]",
        "(mezzanine)[188][189][190]",
        "1080",
        "8800",
        "9300",
        "GPU",
        "GS[15]",
        "GT",
        "GTX",
        "GeForce",
        "V100",
        "accelerator",
        "Nvidia",
        "RTX",
        "TITAN"
    }
    assert gp.pd_series_to_set(test_df['name']) == result_set
    assert gp.pd_series_to_set(test_series) == result_set

def test_scrape_gpu_names_wikipedia():
    pass
    # TODO: Create this test. Possibly use betamax? Or download html and pass raw html to BS4?