import json
import re
from typing import List

from pydantic import BaseModel, Field, field_validator

from gemini_client import generate_text


class QuizQuestion(BaseModel):

    question: str

    options: List[str] = Field(
        min_length=4,
        max_length=4
    )

    answer: str

    explanation: str = ""

    @field_validator("answer")
    @classmethod
    def answer_must_be_an_option(
        cls,
        value,
        info
    ):

        options = info.data.get(
            "options",
            []
        )

        if options and value not in options:

            raise ValueError(
                "Answer must match one of the options."
            )

        return value


class QuizResponse(BaseModel):

    questions: List[QuizQuestion] = Field(
        min_length=1,
        max_length=10
    )


def clean_json_block(text: str) -> str:

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "No JSON object found."
        )

    return text[start:end + 1]


def generate_quiz(
    topic_or_text: str
) -> QuizResponse:

    prompt = f"""
Create exactly 3 multiple-choice questions
for a student based on the following topic.

Topic:

{topic_or_text}

Return ONLY valid JSON.

Use exactly this structure:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}

Rules:

- Exactly 3 questions.
- Exactly 4 options per question.
- Only one correct answer.
- The answer must exactly match one option.
- Questions should test understanding.
- Do not use Markdown.
"""

    raw_response = generate_text(
        prompt,
        temperature=0.3,
        max_output_tokens=1800
    )

    cleaned_response = clean_json_block(
        raw_response
    )

    data = json.loads(
        cleaned_response
    )

    quiz = QuizResponse.model_validate(
        data
    )

    if len(quiz.questions) != 3:

        raise ValueError(
            "Gemini did not return exactly 3 questions."
        )

    return quiz