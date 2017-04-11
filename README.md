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
