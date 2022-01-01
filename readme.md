# NewsScraper

A simple Python 3 module to get crypto or news articles and their content from various RSS feeds.

## 🔧 Installation

1. Clone the repo locally.
2. Use the package manager [pip][url_pip] to install the requirements.
```bash
pip install -r requirements.txt
```

## ✨ Basic Usage

```python
import NewsScraper

all_data = NewsScraper.fetch_all()
news_data = NewsScraper.fetch_news_data()
crypto_data = NewsScraper.fetch_crypto_data()
```

---

<details>
<summary>fetch_all()</summary>

Returns a set of ``NewsScraper.Result`` containing fetched results from all available RSS feeds
      
Can include categories: ``GLOBAL``, ``US``, ``EU``, ``CRYPTO``, ``BLOCKCHAIN``, ``BTC``, ``ETH``, ``LTC``.
</details>
<details>
<summary>fetch_news_data()</summary>

Returns a set of ``NewsScraper.Result`` containing fetched results from CNN, ABC News, Yahoo News, Fox News RSS feeds
      
Can include categories: ``GLOBAL``, ``US``, ``EU``.
</details>
<details>
<summary>fetch_crypto_data()</summary>

Returns a set of ``NewsScraper.Result`` containing fetched results from CoinJournal, Crypto Currency News RSS feeds.
      
Can include categories: ``CRYPTO``, ``BLOCKCHAIN``, ``BTC``, ``ETH``, ``LTC``.
</details>

## 🔨 Advanced Usage

### NewsScraper.Result class
A class used to represent a returned article.

<details>
<summary><b>Attributes</b></summary>

- ##### context : str
    
    A string describing the category of the article.
    
    ex. ``"GLOBAL"``, ``"US"``, ``"BLOCKCHAIN"``, ``"BTC"``.
- ##### title : str
    
    A string containing the name of the article.
- ##### summary : str
    
    A string containing the summary of the article.
    
    NOTE: sometimes it can have the value of ``""``, because the RSS feed didn't provide a summary.
- ##### content : str
    
    A string containing the content of the article.
</details>
<details>
<summary><b>Methods</b></summary>

- ##### Result.json()
    
    Returns a dictionary with the attributes of the class formatted in JSON.
    
    ex.
```json
{
  "context": "global",
  "title": "title of the article",
  "summary": "summary of the article",
  "content": "content of the article"
}
 ```
</details>

---

### News RSS Feeds
All of these functions return a set of ``NewsScraper.Result`` containing fetched results of the described RSS feeds.
```python
fetch_abc()
fetch_cnn()
fetch_yahoo()
fetch_fox_news()
```
Can include categories: ``GLOBAL``, ``US``, ``EU``.

Alternatively, you can use ``fetch_news_data()`` to receive results from all of them.

---

### Crypto RSS Feeds
All of these functions return a set of ``NewsScraper.Result`` containing fetched results of the described RSS feeds.
```python
fetch_coinjournal()
fetch_cryptocurrencynews()
```
Can include categories: ``CRYPTO``, ``BLOCKCHAIN``, ``BTC``, ``ETH``, ``LTC``.

Alternatively, you can use ``fetch_news_data()`` to receive results from all of them.

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License
This project is licensed under the [MIT][url_mit] license.

[url_pip]: https://pip.pypa.io/en/stable/
[url_mit]: https://choosealicense.com/licenses/mit/