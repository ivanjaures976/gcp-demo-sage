"""Reads and writes on the `chunks` collection: vector search at request time, and the
writes used by utils/ingest_documents.py to populate the knowledge base."""

from functools import lru_cache

from google.cloud import firestore
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google.cloud.firestore_v1.vector import Vector

from sage.config import get_app_config
from sage.domain.qa.models import Chunk


@lru_cache
def _collection():
    config = get_app_config()
    db = firestore.Client(project=config.project_id, database=config.firestore_database)
    return db.collection(config.firestore_collection)


def find_nearest_chunks(embedding: list[float]) -> list[Chunk]:
    config = get_app_config()
    query = _collection().find_nearest(
        vector_field="embedding",
        query_vector=Vector(embedding),
        distance_measure=DistanceMeasure.COSINE,
        limit=config.top_k,
    )
    chunks = []
    for doc in query.stream():
        data = doc.to_dict()
        chunks.append(
            Chunk(
                id=doc.id,
                text=data["text"],
                source=data["source"],
                section=data.get("section"),
                chunk_index=data["chunk_index"],
            )
        )
    return chunks


def delete_chunks_for_source(source: str) -> None:
    """Remove existing chunks for a document, so re-running the ingestion script is safe."""
    for doc in _collection().where("source", "==", source).stream():
        doc.reference.delete()


def add_chunk(
    chunk_id: str,
    text: str,
    embedding: list[float],
    source: str,
    section: str | None,
    chunk_index: int,
) -> None:
    _collection().document(chunk_id).set(
        {
            "text": text,
            "embedding": Vector(embedding),
            "source": source,
            "section": section,
            "chunk_index": chunk_index,
        }
    )
