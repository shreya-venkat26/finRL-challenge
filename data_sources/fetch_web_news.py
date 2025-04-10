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
                full_url = f"https://finance.yahoo.com{a['href']}"
                summary = scrape_yahoo_summary(full_url)
                articles.append({
                    'source': 'YahooFinance',
                    'headline': a.text.strip(),
                    'summary': summary,
                    'url': full_url,
                    'datetime': datetime.datetime.now(datetime.timezone.utc).timestamp()
                })
    except Exception as e:
        print(f"Error scraping Yahoo Finance: {e}")
    return articles

def scrape_yahoo_summary(url):
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.content, "html.parser")
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"].strip()
        paragraphs = soup.find_all("p")
        if paragraphs:
            return paragraphs[0].get_text().strip()
    except Exception as e:
        print(f"Failed to fetch Yahoo summary for {url}: {e}")
    return ""

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
                    'datetime': datetime.datetime.now(datetime.timezone.utc).timestamp()
                })
    except Exception as e:
        print(f"Error scraping MarketWatch: {e}")
    return articles

def fetch_scraped_news():
    yahoo_articles = fetch_yahoo_finance()
    marketwatch_articles = fetch_marketwatch()
    return yahoo_articles + marketwatch_articles
