from apscheduler.schedulers.blocking import BlockingScheduler
from data_sources.fetch_finnhub_news import fetch_finnhub_news_and_sentiment
from data_sources.fetch_web_news import fetch_scraped_news
from push_to_qdrant import embed_and_store

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', hours=3)
def scheduled_job():
    print("Pulling data on schedule and vectorizing...")

    finnhub_data = fetch_finnhub_news_and_sentiment()
    scraped_data = fetch_scraped_news()

    all_articles = finnhub_data + scraped_data
    embed_and_store(all_articles)

    print(f"[Ingestor] Ingested {len(all_articles)} new articles.")

if __name__ == "__main__":
    print("[Ingestor] Starting 3-hour interval job...")
    scheduler.start()