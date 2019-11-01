# Aesop's Pawnshop

Webscrape exploratory data analysis of used nvidia graphics cards from [/r/hardwareswap](www.reddit.com/r/hardwareswap) for 2019 to September.
* Crawls with PRAW and PSAW to get posts

## Local Install and Deployment
* Look at python_scripts/example_secrets.py
    * Get reddit API key from account developer settings
    * setup MongoDB and get credentials
    * Create secrets.py file with same format as example_secrets
* run `python_scripts/pymongo_db.py` to initialize mongodb schema
* run `python_scripts/subredditscrape.py` and allow approx ~hour to scrape

You should now have a mongodb with all reddit posts that contain nvidia gpu keywords in the title.

### MongoDB Structure and Notes
* Currently DB name is `Hardwarescrape`
    * Collection name: `reddit`
    
Example Document Structure:

* **post_id**: The unique reddit post_id that ties to the original reddit post.
    * This is set as an index for documents, so you can query for posts directly with this or their original ID auto-assigned by pymongo/MongoDB when first inserted
* **title**: The post title
* **self_text**: The post text full dumped
* **created**: Unix time of post creation date
* **author_info**: a dictoinary of author_id, name, and trade information (scraped from user flair)
    * **author_id**: unique reddit user ID
    * **author_name**: the string user handle of the reddit user
    * **author_trade_info**: the user flair string, on /r/hardwareswap for 2019 it was trading information

##### **WARNING** if a reddit user deleted their account, this is an empty dictionary. If you're trying to work with author information, make sure to use `author_info.get('author_id')` to avoid key errors for deleted users.

               
### TODO:
1. Better testing coverage (testing branch has beginning of refactors and testing with betamax for recording API queries to PSAW)
1. Use NLTK to process post titles and better sort posts in categories of laptop and GPU
    * python_scripts/pricingprocessing.py uses a very rough approach to this problem with comparing key-words
    * TF-IDF on titles and posts, then group with item-item similarity
1. Multi-thread or change api querying style as right now it 'hangs' when author is deleted
    * primary performance issue on the scrape
        * matters less when just keeping database updated with most recent posts
1. Hook data into flask app to create dashboard
1. Command line arguments for running the scraping and database creation scripts
    * start and end date
    * database/collection names
