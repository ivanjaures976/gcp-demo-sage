"""Reads istruzioni.md from Cloud Storage on every request."""

import asyncio
import logging

from google.cloud import storage

from sage.config import get_app_config

log = logging.getLogger(__name__)


def _read_instructions() -> str:
    config = get_app_config()
    if not config.instructions_bucket:
        return ""
    client = storage.Client(project=config.project_id)
    blob = client.bucket(config.instructions_bucket).blob(config.instructions_object)
    return blob.download_as_text(encoding="utf-8")


async def load_instructions() -> str:
    try:
        return await asyncio.to_thread(_read_instructions)
    except Exception:
        log.exception("Impossibile leggere le istruzioni da Cloud Storage")
        return ""
