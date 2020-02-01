import pytest
import src.subredditscrape as ss
from unittest.mock import patch


def test_scrape_hws():
    # psaw mock to generate fake posts to run through
    # honestly this needs betamax recorder because mocking this otherwise is insane
    # specific things to check: * submissions with or without author
    # mock insert submission dict to assert it's called
    pass
