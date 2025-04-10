import requests
import datetime
from config import FINNHUB_API_KEY, FINNHUB_TICKERS

BASE_URL = "https://finnhub.io/api/v1"

HEADERS = {
    'X-Finnhub-Token': FINNHUB_API_KEY
}

def fetch_finnhub_news_and_sentiment():
    all_articles = []
    now = datetime.timezone.utc
    start = (now - datetime.timedelta(hours=3)).strftime('%Y-%m-%d')

    for ticker in FINNHUB_TICKERS:
        ## hopefully reads in company-specific news
        url = f"{BASE_URL}/company-news?symbol={ticker}&from={start}&to={now.strftime('%Y-%m-%d')}"
        try:
            news_resp = requests.get(url, headers=HEADERS).json()
            for item in news_resp:
                article = {
                    'ticker': ticker,
                    'source': 'FinnhubNews',
                    'headline': item.get('headline'),
                    'summary': item.get('summary'),
                    'datetime': item.get('datetime')
                }
                all_articles.append(article)
        except Exception as e:
            print(f"[Finnhub] Error fetching news for {ticker}: {e}")

        # quantitative analyst sentiment; TODO: extend to qualitative
        try:
            sentiment_url = f"{BASE_URL}/stock/recommendation?symbol={ticker}"
            sentiment_data = requests.get(sentiment_url, headers=HEADERS).json()
            if sentiment_data:
                s = sentiment_data[0]
                sentiment_article = {
                    'ticker': ticker,
                    'source': 'FinnhubSentiment',
                    'headline': f"Analyst sentiment for {ticker}",
                    'summary': f"Buy: {s['buy']}, Hold: {s['hold']}, Sell: {s['sell']}, Period: {s['period']}",
                    'datetime': now.timestamp()
                }
                all_articles.append(sentiment_article)
        except Exception as e:
            print(f"[Finnhub] Sentiment error for {ticker}: {e}")

    return all_articles