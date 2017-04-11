## news-crawler

_Python library for crawling and enriching RSS news feeds._

I'm using this library to generate a dataset for training classifiers to distinguish between
liberal and conservative news sources.  After hand-curating a list of tagged RSS feeds (see [`rss`](rss)),
the library enables the following:

* Pull down an RSS file for each feed, containig URL's and metadata for each article.
* For each feed, check whether or not the URLs have already been crawled by querying against a SQL db.
* If a URL has not been seen before:
    * Send it to the AlchemyAPI `URLGetCombinedData` endpoint.   This scrapes and cleans the text, and adds
      NLP "enrichments" to each document such as entities, keywords, and taxonomy labels.
    * Add it to the SQL db so we don't crawl it more than once.

The AlchemyAPI endpoint makes is simple to scrape a given URL, and the NLP metadata can be used later
to further filter down the types of articles we use for training.  If you don't want to use Alchemy 
for crawling, you could replace this piece with, e.g., [BeautifulSoup](https://pypi.python.org/pypi/beautifulsoup4).

The core functionality in Python is in the [news-crawler](news-crawler) directory.  Utility scripts used for 
running on AWS and syncing the files to my local machine are in the [`bin`](bin) directory.

__How I'm using it:__  This could be made a lot easier to use, with a little work!

* Install Anaconda and create a `default` environment.

        conda create -n default

* Clone repo into `$HOME/gitrepos/.`

* Install python dependencies:

        cd $HOME/gitrepos/news-crawler
        pip install -r requirements.txt

* Drop APIKEY into `$HOME/gitrepos/news-crawler/news-crawler/key.txt`.
* Create screen to run crawler in:

        screen -S crawl     # creates screen

* Poor mans cron job:
 
        screen -r crawl
        cd $HOME/gitrepos/news-crawler/bin/
        ./keep-running run.sh 28800
        # `ctrl-a d` to detach before exiting

* Sync files to local machine:

        cd $HOME/gitrepos/news-crawler/bin
        ./download.sh
        
