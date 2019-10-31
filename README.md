# Aesop's Pawnshop

Webscrape exploratory data analysis of used nvidia graphics cards from [/r/hardwareswap](www.reddit.com/r/hardwareswap) for 2019 to September.
* data/df.P is a dataframe of ~900 posts that have been cleaned to a minor extent and can be used for simple EDA

## Local Install and Deployment
* Look at python_scripts/example_secrets.py
    * Get reddit API key from account developer settings
    * setup MongoDB and get credentials
    * Create secrets.py file with same format as example_secrets
* run `python_scripts/pymongo_db.py` to initialize mongodb schema
* run `python_scripts/subredditscrape.py` and allow approx ~hour to scrape

You should now have a mongodb with all reddit posts that contain nvidia gpu keywords in the title.