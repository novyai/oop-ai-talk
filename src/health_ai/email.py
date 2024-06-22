from health_ai.ai import openai_client


async def generate_email_summary(questions: list[str], answers: list[str]) -> str:
    system_prompt = "You are a data scientist and and excellent writer. You are writing an update to your manager about the results of patient adherence data analysis."
    user_prompt_format = """You have asked and answered for yourself the following questions:
    ```
    {question_answers}
    ```

    Write an email to your manager summarizing the results of your analysis."""

    question_answers = "\n".join(
        [f"Q: {question}\nA: {answer}" for question, answer in zip(questions, answers)]
    )

    user_prompt = user_prompt_format.format(question_answers=question_answers)

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content or ""