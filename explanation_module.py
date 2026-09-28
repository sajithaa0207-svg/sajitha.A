import os

from gemini_client import generate_text


LOCAL_MODEL = None
LOCAL_TOKENIZER = None


def explain_with_local_model(topic: str) -> str:

    global LOCAL_MODEL
    global LOCAL_TOKENIZER

    from transformers import (
        AutoModelForSeq2SeqLM,
        AutoTokenizer
    )

    model_name = os.getenv(
        "LOCAL_EXPLAINER_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )

    if LOCAL_TOKENIZER is None:

        LOCAL_TOKENIZER = AutoTokenizer.from_pretrained(
            model_name
        )

    if LOCAL_MODEL is None:

        LOCAL_MODEL = AutoModelForSeq2SeqLM.from_pretrained(
            model_name
        )

    prompt = f"""
Explain the following topic to a beginner.

Topic:

{topic}

Give:

1. Simple definition
2. Important points
3. Easy example
4. Short recap
"""

    inputs = LOCAL_TOKENIZER(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = LOCAL_MODEL.generate(
        **inputs,
        max_new_tokens=220,
        num_beams=4,
        early_stopping=True
    )

    return LOCAL_TOKENIZER.decode(
        outputs[0],
        skip_special_tokens=True
    ).strip()


def explain_topic(topic: str) -> str:

    use_local_model = os.getenv(
        "LOCAL_EXPLAINER",
        "false"
    ).lower() == "true"

    if use_local_model:

        try:

            return explain_with_local_model(topic)

        except Exception:

            pass

    prompt = f"""
Explain this topic for a beginner student.

Topic:

{topic}

Use this structure:

Simple definition

Key points

Step-by-step explanation if needed

Easy real-life example

One-line recap

Use simple and clear language.
"""

    return generate_text(
        prompt,
        temperature=0.35,
        max_output_tokens=1100
    )