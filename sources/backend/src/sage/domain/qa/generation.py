from pathlib import Path

from sage.domain.qa.models import Chunk
from sage.integrations.llm.generate import generate_text
from sage.integrations.storage.instructions import load_instructions

_PROMPT_TEMPLATE = (Path(__file__).parent / "prompts" / "answer_prompt.txt").read_text(
    encoding="utf-8"
)
_NO_DOCUMENTS_CONTEXT = (
    "Nessun documento disponibile (base di conoscenza non ancora popolata o non configurata)."
)
_NO_INSTRUCTIONS = "(nessuna istruzione aggiuntiva)"


def build_prompt(question: str, chunks: list[Chunk], instructions: str = "") -> str:
    context = (
        "\n\n".join(f"[{chunk.source}] {chunk.text}" for chunk in chunks)
        if chunks
        else _NO_DOCUMENTS_CONTEXT
    )
    return _PROMPT_TEMPLATE.format(
        context=context,
        question=question,
        instructions=instructions.strip() or _NO_INSTRUCTIONS,
    )


async def generate_answer(question: str, chunks: list[Chunk]) -> str:
    instructions = await load_instructions()
    prompt = build_prompt(question, chunks, instructions)
    return await generate_text(prompt)
