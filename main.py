"""
NewsScraper
Author: 370rokas <https://github.com/370rokas>
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import html
import json

enable_logging = True
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
        return {self.context, self.title, self.summary, self.content}

    def __hash__(self):
        return hash(self.context + self.title + self.summary + self.content)

    def __eq__(self, other):
        return hash(self) == hash(other)


def fetch_abc():
    results = set()

    # ABC Feeds
    feeds = [
        ["US", "http://feeds.abcnews.com/abcnews/topstories"],
        ["GLOBAL", "http://feeds.abcnews.com/abcnews/internationalheadlines"],
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

                results.add(Result(url[1], post["title"], post["summary"], content))
            except:
                continue

    return results


def fetch_yahoo():
    results = set()

    # Load Yahoo cookies from cookies/yahoo.json
    with open('./cookies/yahoo.json', 'r') as jsonfile:
        data = jsonfile.read()

    cookies = json.loads(data)

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
            r = requests.get(post["link"], headers=headers, cookies=cookies)

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


def fetch_data():
    results = set()

    # Fetch ABC results
    results.update(fetch_abc())

    # Fetch Yahoo results
    results.update(fetch_yahoo())

    return results


for i in fetch_abc():
    print(i.json())
