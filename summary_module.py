from gemini_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational passage.

Requirements:

- Keep the main ideas.
- Keep important facts.
- Remove repetition.
- Use simple language.
- Make it useful for quick revision.
- Do not add information that is not in the passage.
- Use bullet points when helpful.

Educational passage:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.2,
        max_output_tokens=1400
    )