"""Text embedding via Vertex AI (Google Gen AI SDK, ADC-based)."""

from functools import lru_cache

from google import genai
from google.genai import types

from sage.config import get_app_config


@lru_cache
def _get_embedding_client() -> genai.Client:
    config = get_app_config()
    return genai.Client(vertexai=True, project=config.project_id, location=config.region)


def embed_text(text: str) -> list[float]:
    config = get_app_config()
    response = _get_embedding_client().models.embed_content(
        model=config.embedding_model,
        contents=text,
        config=types.EmbedContentConfig(output_dimensionality=config.embedding_dimension),
    )
    return list(response.embeddings[0].values)
