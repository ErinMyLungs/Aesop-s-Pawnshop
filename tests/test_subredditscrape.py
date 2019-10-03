import pytest
import python_scripts.subredditscrape as ss
from unittest.mock import patch

def test_scrape_hws(mock_psaw):
    # psaw mock to generate fake posts to run through
    # honestly this needs betamax recorder because mocking this otherwise is insane
    # specific things to check: * submissions with or without author
    # mock insert submission dict to assert it's called
    pass