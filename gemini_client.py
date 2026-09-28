import os
from functools import lru_cache

from google import genai
from google.genai import types


DEFAULT_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
)


@lru_cache(maxsize=1)
def get_client() -> genai.Client:

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    return genai.Client(
        api_key=api_key
    )


def generate_text(
    prompt: str,
    temperature: float = 0.4,
    max_output_tokens: int = 1200
) -> str:

    response = get_client().models.generate_content(

        model=DEFAULT_MODEL,

        contents=prompt,

        config=types.GenerateContentConfig(

            temperature=temperature,

            max_output_tokens=max_output_tokens
        )
    )

    text = (response.text or "").strip()

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text