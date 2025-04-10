from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import hashlib

# loading the huggingface model
model = SentenceTransformer("BAAI/bge-base-en-v1.5")
collection_name = "financial_news"

# establish qdrant connection
client = QdrantClient(host="localhost", port=6333)

if collection_name not in [col.name for col in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
    )

def embed_and_store(articles):
    points = []
    for article in articles:
        try:
            text = f"{article['headline']} {article.get('summary', '')}"
            embedding = model.encode(text)

            uid = hashlib.sha256(text.encode()).hexdigest()

            points.append(PointStruct(
                id=uid,
                vector=embedding.tolist(),
                payload={
                    "source": article.get("source"),
                    "headline": article.get("headline"),
                    "summary": article.get("summary"),
                    "ticker": article.get("ticker", ""),
                    "datetime": article.get("datetime"),
                    "url": article.get("url", "")
                }
            ))
        except Exception as e:
            print(f"[Embed/Qdrant] Failed to embed or store article: {e}")

    if points:
        client.upsert(collection_name=collection_name, points=points)
        print(f"[Qdrant] Stored {len(points)} embedded articles.")
    else:
        print("[Qdrant] No points to store.")