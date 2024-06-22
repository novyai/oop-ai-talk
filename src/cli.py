import pandas as pd
import pandasql as psql
from async_typer import AsyncTyper
from elevenlabs import play
from health_ai.audio import record_until_silence
from health_ai.bot import generate_call_center_response, generate_response
from health_ai.email import generate_email_summary
from health_ai.extract import extract_adhereance_result
from health_ai.sql import generate_answer, generate_questions, generate_sql_query
from health_ai.transcribe import transcribe
from health_ai.tts import text_to_speech

cli = AsyncTyper()


@cli.command()
def hello(name: str):
    print(f"Hello {name}!")


@cli.command()
async def ask(prompt: str):
    messages = [
        {"role": "user", "content": prompt},
    ]

    response = await generate_response(messages)
    print(response)


@cli.command()
async def speak(text: str):
    voice_id = "Xb7hH8MSUJpSbSDYk0k2"
    audio = await text_to_speech(voice_id, text)
    play(audio)


@cli.command()
async def converse():
    messages = []

    voice_id = "Xb7hH8MSUJpSbSDYk0k2"

    while True:
        print("Listening...")
        audio = record_until_silence()
        print("Stopped listening.")

        transcript = await transcribe(audio)
        text = transcript.text

        messages.append({"role": "user", "content": text})

        assistant_response = generate_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})

        assistant_audio = await text_to_speech(voice_id, assistant_response)
        play(assistant_audio)

        print(f"Assistant: {assistant_response}")


@cli.command()
async def call():
    messages = []

    voice_id = "Xb7hH8MSUJpSbSDYk0k2"

    while True:
        print("Listening...")
        audio = record_until_silence()
        print("Stopped listening.")

        transcript = await transcribe(audio)
        text = transcript.text

        messages.append({"role": "user", "content": text})

        assistant_response, done = await generate_call_center_response(messages)
        messages.append({"role": "assistant", "content": assistant_response})

        assistant_audio = await text_to_speech(voice_id, assistant_response)
        play(assistant_audio)

        print(f"Assistant: {assistant_response}")

        if done:
            print("Call done")
            break

    conversation = "\n".join([
        f"{message['role']}: {message['content']}"
        for message in messages
    ])

    extraction = await extract_adhereance_result(conversation)
    print(extraction.model_dump_json(indent=2))

        
@cli.command()
async def query(filepath: str, prompt: str):
    df = pd.read_csv(filepath)
    result = psql.sqldf(prompt, {"patient_data": df})
    print(result)


@cli.command()
async def analyze(filepath: str, prompt: str):
    df = pd.read_csv(filepath)

    sql_query = await generate_sql_query(prompt, df)
    # print(sql_query)

    result = psql.sqldf(sql_query, {"patient_data": df})
    # print(result)

    response = await generate_answer(prompt, sql_query, df, result)
    print(response)



@cli.command()
async def email(filepath: str):
    df = pd.read_csv(filepath)

    questions = await generate_questions(df)
    print(questions)

    answers = []

    for question in questions:
        print(f"Question: {question}")
        sql_query = await generate_sql_query(question, df)

        result = psql.sqldf(sql_query, {"patient_data": df})
        response = await generate_answer(question, sql_query, df, result)
        print(f"Answer: {response}")

        answers.append(response)

    email = await generate_email_summary(questions, answers)
    print(email)


if __name__ == "__main__":
    cli()
