import requests
from bs4 import BeautifulSoup
import datetime

def fetch_yahoo_finance():
    url = "https://finance.yahoo.com/"
    articles = []
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.content, "html.parser")
        headlines = soup.select("h3")
        for h in headlines:
            a = h.find("a")
            if a and a.text and a["href"]:
                articles.append({
                    'source': 'YahooFinance',
                    'headline': a.text.strip(),
                    'summary': '',
                    'url': f"https://finance.yahoo.com{a['href']}",
                    'datetime': datetime.datetime.utcnow().timestamp()
                })
    except Exception as e:
        print(f"[Yahoo] Error scraping Yahoo Finance: {e}")
    return articles

def fetch_marketwatch():
    url = "https://www.marketwatch.com/latest-news"
    articles = []
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.content, "html.parser")
        stories = soup.select(".article__content")
        for story in stories:
            h = story.find("a")
            p = story.find("p")
            if h and h.text:
                articles.append({
                    'source': 'MarketWatch',
                    'headline': h.text.strip(),
                    'summary': p.text.strip() if p else '',
                    'url': h['href'],
                    'datetime': datetime.datetime.utcnow().timestamp()
                })
    except Exception as e:
        print(f"[MarketWatch] Error scraping MarketWatch: {e}")
    return articles

def fetch_scraped_news():
    yahoo_articles = fetch_yahoo_finance()
    marketwatch_articles = fetch_marketwatch()
    return yahoo_articles + marketwatch_articles
