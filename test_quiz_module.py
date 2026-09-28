from quiz_module import (
    clean_json_block,
    QuizResponse
)


def test_clean_json_block():

    raw = """
    ```json
    {
        "questions": []
    }
    ```
    """

    result = clean_json_block(
        raw
    )

    assert result == """
    {
        "questions": []
    }
    """.strip()


def test_quiz_schema():

    quiz = QuizResponse.model_validate({

        "questions": [

            {

                "question":
                    "What is 2 + 2?",

                "options": [
                    "3",
                    "4",
                    "5",
                    "6"
                ],

                "answer":
                    "4",

                "explanation":
                    "Two plus two equals four."

            }

        ]

    })


    assert (
        quiz.questions[0].answer
        == "4"
    )