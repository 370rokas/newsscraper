"""
   ______________             __
  |__  /__  / __ \_________  / /______ ______
   /_ <  / / / / / ___/ __ \/ //_/ __ `/ ___/
 ___/ / / / /_/ / /  / /_/ / ,< / /_/ (__  )
/____/ /_/\____/_/   \____/_/|_|\__,_/____/

NewsScraper

A simple Python 3 module to get crypto or news articles and their content from various RSS feeds.

Author: 370rokas <https://github.com/370rokas/newsscraper>
Created: 1st January, 2022
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}


class Result:
    def __init__(self, context, title, summary, content):
        self.context = context
        self.title = title
        self.summary = summary
        self.content = content

    def json(self):
        return {
            "context": self.context,
            "title": self.title,
            "summary": self.summary,
            "content": self.content
        }

    def __hash__(self):
        return hash(self.context + self.title + self.summary + self.content)

    def __eq__(self, other):
        return hash(self) == hash(other)


def fetch_abc():
    results = set()

    # ABC Feeds
    feeds = [
        ["GLOBAL", "http://feeds.abcnews.com/abcnews/internationalheadlines"],
        ["US", "http://feeds.abcnews.com/abcnews/topstories"],
        ["US", "http://feeds.abcnews.com/abcnews/entertainmentheadlines"],
        ["US", "http://feeds.abcnews.com/abcnews/technologyheadlines"],
        ["US", "http://feeds.abcnews.com/abcnews/travelheadlines"],
    ]

    for url in feeds:
        feed = feedparser.parse(url[1])
        for post in feed.entries:
            r = requests.get(post["link"], headers=headers)

            soup = BeautifulSoup(r.content, 'html.parser')
            article_content_element = soup.select_one('.Article__Content')

            try:
                content = ""

                for p_element in article_content_element.findChildren("p", recursive=False):
                    content = content + html.unescape(p_element.get_text()) + "\n"

                results.add(Result(url[0], post["title"], post["summary"], content))
            except:
                continue

    return results


def fetch_yahoo():
    results = set()

    # Yahoo Feeds
    feeds = [
        ["US", "https://www.yahoo.com/news/rss/us"],
        ["GLOBAL", "https://www.yahoo.com/news/rss/world"],
        ["GLOBAL", "https://www.yahoo.com/news/rss/health"],
        ["GLOBAL", "https://finance.yahoo.com/news/rssindex"],
    ]

    for url in feeds:
        feed = feedparser.parse(url[1])
        for post in feed.entries:
            r = requests.get(post["link"])

            soup = BeautifulSoup(r.content, 'html.parser')
            article_content_element = soup.select_one('.caas-body')

            try:
                content = ""

                for p_element in article_content_element.findChildren("p", recursive=False):
                    content = content + html.unescape(p_element.get_text()) + "\n"

                results.add(Result(url[0], post["title"], "", content))
            except:
                continue

    return results


def fetch_cnn():
    results = set()

    # CNN Feeds
    feeds = [
        ["GLOBAL", "http://rss.cnn.com/rss/edition_world.rss"],
        ["US", "http://rss.cnn.com/rss/edition_us.rss"],
        ["EU", "http://rss.cnn.com/rss/edition_europe.rss"],
    ]

    for url in feeds:
        feed = feedparser.parse(url[1])
        for post in feed.entries:
            r = requests.get(post["link"])

            soup = BeautifulSoup(r.content, 'html.parser')
            article_content_element = soup.find("section", {"id": "body-text"})

            try:
                results.add(Result(url[0], post["title"], "", html.unescape(article_content_element.get_text())))
            except:
                continue

    return results


def fetch_fox_news():
    results = set()

    # Fox News feeds
    feeds = [
        ["US", "http://feeds.foxnews.com/foxnews/national"],
        ["US", "http://feeds.foxnews.com/foxnews/politics"],
        ["GLOBAL", "http://feeds.foxnews.com/foxnews/world"],
    ]

    for url in feeds:
        feed = feedparser.parse(url[1])
        for post in feed.entries:
            r = requests.get(post["link"])

            soup = BeautifulSoup(r.content, 'html.parser')
            article_content_element = soup.select_one('.article-body')

            try:
                content = ""

                for p_element in article_content_element.findChildren("p", recursive=False):
                    # Filter out links to other articles, AD's to install the Fox News App
                    if not (p_element.findChildren("a", {}) and p_element.findChildren("strong", {})):
                        content = content + html.unescape(p_element.get_text()) + "\n"

                results.add(Result(url[0], post["title"], "", content))
            except:
                continue

    return results


def fetch_coinjournal():
    results = set()

    # CoinJournal feeds
    feeds = [
        ["CRYPTO", "https://coinjournal.net/news/feed/"],
        ["BLOCKCHAIN", "https://coinjournal.net/news/tag/blockchain/feed/"],
        ["BTC", "https://coinjournal.net/news/tag/bitcoin/feed/"],
        ["ETH", "https://coinjournal.net/news/tag/ethereum/feed/"],
        ["LTC", "https://coinjournal.net/news/tag/litecoin/feed/"],
    ]

    for url in feeds:
        feed = feedparser.parse(url[1])
        for post in feed.entries:
            r = requests.get(post["link"], headers=headers)

            soup = BeautifulSoup(r.content, 'html.parser')
            article_content_element = soup.find("article", {"class": "relative"})
            article_content_element = article_content_element.find("div", {"class":"flow-root mb-4 prose-sm prose md:prose max-w-none"})

            try:
                content = ""

                for p_element in article_content_element.findChildren("p", recursive=False):
                    content = content + html.unescape(p_element.get_text()) + "\n"

                results.add(Result(url[0], post["title"], "", content))
            except:
                continue

    return results


def fetch_cryptocurrencynews():
    results = set()

    # Crypto Currency News feeds
    feeds = [
        ["CRYPTO", "https://cryptocurrencynews.com/daily-news/crypto-news/feed/"],
    ]

    for url in feeds:
        feed = feedparser.parse(url[1])
        for post in feed.entries:
            r = requests.get(post["link"], headers=headers)

            soup = BeautifulSoup(r.content, 'html.parser')
            article_content_element = soup.find("div", {"class": "entry-content clearfix custom-blogpost"})

            try:
                # Go through nested <div>'s to the content <div>

                for x in range(4):
                    article_content_element = article_content_element.find("div", {
                        "class": "Ov(h) Trs($transition-readmore) Mah(999999px)"})

                content = ""

                for p_element in article_content_element.findChildren("p", recursive=False):
                    content = content + html.unescape(p_element.get_text()) + "\n"

                results.add(Result(url[0], post["title"], "", content))
            except:
                continue

    return results


def fetch_news_data():
    results = set()

    # Fetch ABC results
    results.update(fetch_abc())

    # Fetch Yahoo results
    results.update(fetch_yahoo())

    # Fetch CNN results
    results.update(fetch_cnn())

    # Fetch Fox News results
    results.update(fetch_fox_news())

    return results


def fetch_crypto_data():
    results = set()

    # Fetch CoinJournal results
    results.update(fetch_coinjournal())

    # Fetch Crypto Currency News results
    results.update(fetch_cryptocurrencynews())

    return results


def fetch_all():
    results = set()

    # Fetch News data
    results.update(fetch_news_data())

    # Fetch Crypto News data
    results.update(fetch_crypto_data())

    return results
