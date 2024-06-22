import pandas as pd

from health_ai.ai import openai_client


async def generate_sql_query(prompt: str, df: pd.DataFrame) -> str:
    system_prompt = (
        "You are a data scientist working with patient prescription adherence data."
    )
    user_prompt_format = """You have a SQL table called 'patient_data'.

    Here is a sample of that data
    ```
    {sample}
    ```

    A user has asked the following question:
    {prompt}

    Write a SQL query that will return the data necessary to answer the user's question.

    Return only the SQL query - no other commentary

    ```sql
    SELECT """

    sample = df.head().to_markdown(index=False)
    user_prompt = user_prompt_format.format(sample=sample, prompt=prompt)

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content or ""
    return content.replace("```sql", "").replace("```", "").strip()


async def generate_answer(prompt: str, sql_query: str, df: pd.DataFrame, results: pd.DataFrame):
    system_prompt = (
        "You are a data scientist working with patient prescription adherence data."
    )

    user_prompt_format = """You have a SQL table called 'patient_data'.

    Here is a sample of that data
    ```
    {sample}
    ```

    A user has asked the following question:
    {prompt}

    The following SQL query was run:
    {query}

    And the results were:
    ```
    {results}
    ```

    Write a brief natural language answer to the user's question based on the results. No need to mention SQL."""

    sample = df.head().to_markdown(index=False)
    user_prompt = user_prompt_format.format(sample=sample, prompt=prompt, query=sql_query, results=results.to_markdown(index=False))


    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content or ""


async def generate_questions(df: pd.DataFrame, total_questions=3):
    system_prompt = (
        "You are an inquisitive data scientist working with patient prescription adherence data. You are curious to find the most interesting insights from the data."
    )

    user_prompt_format = """You have a SQL table called 'patient_data'.

    Here is a sample of that data
    ```
    {sample}
    ```

    Write {total_questions} questions that you would like to ask about the data to uncover interesting insights.
    
    All questions should be in theory answerable with SQL queries. No need to write the queries, just the questions.
    
    Output format should be a list of questions, one per line, with no additional commentary.
    
    Output example:
    ```
    What is the average age of patients?
    What is the most common medication prescribed?
    ```

    """

    sample = df.head().to_markdown(index=False)
    user_prompt = user_prompt_format.format(sample=sample, total_questions=total_questions)

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    content = response.choices[0].message.content or ""
    content = content.replace("```", "").strip()

    return content.split("\n")