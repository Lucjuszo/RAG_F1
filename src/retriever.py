from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

QDRANT_URL      = "http://localhost:6333"
COLLECTION_NAME = "f1_drivers"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K           = 5

class Retriever:
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_URL)
        self.model  = SentenceTransformer(EMBEDDING_MODEL)

    def search(self, query: str, top_k: int = TOP_K, driver: str = None):
        query_vector = self.model.encode(query).tolist()

        search_filter = None
        if driver:
            search_filter = Filter(
                must=[FieldCondition(key="driver", match=MatchValue(value=driver))]
            )

        results = self.client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=top_k,
            with_payload=True,
            query_filter=search_filter,
        ).points

        return [
            {
                "text":     hit.payload["text"],
                "driver":   hit.payload["driver"],
                "score":    round(hit.score, 4),
            }
            for hit in results
        ]
