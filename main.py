"""
NewsScraper
Author: 370rokas <https://github.com/370rokas>
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

            content = ""

            for p_element in article_content_element.findChildren("p", recursive=False):
                # Filter out links to other articles, AD's to install the Fox News App
                if not (p_element.findChildren("a", {}) and p_element.findChildren("strong", {})):
                    content = content + html.unescape(p_element.get_text()) + "\n"

            results.add(Result(url[0], post["title"], "", content))

    return results


def fetch_data():
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
