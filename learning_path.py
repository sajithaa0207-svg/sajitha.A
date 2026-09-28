from gemini_client import generate_text


def get_learning_recommendations(
    topic: str
) -> str:

    prompt = f"""
Create a personalized learning path
for the following topic:

{topic}

Organize it as:

1. Learning goal

2. Beginner level

3. Intermediate level

4. Advanced level

5. Practice ideas

6. Project ideas

7. Recommended resource types
   - Videos
   - Articles
   - Books
   - Documentation

8. Suggested weekly progression

Keep it practical for a student.

Do not invent specific website URLs.

Use simple language.
"""

    return generate_text(
        prompt,
        temperature=0.5,
        max_output_tokens=1800
    )