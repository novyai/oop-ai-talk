from typing import Tuple

from health_ai.ai import openai_client


async def generate_response(messages) -> str:
    system_prompt = "You're a helpful assistant, but also a homie. You're brief, casual, and to the point. Don't over do it just be norma Don't over do it just be normall" 
    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            *messages,
        ],
    )

    return response.choices[0].message.content or ""

async def generate_call_center_response(messages, name="Sam") -> Tuple[str, bool]:
    system_prompt = f"""You are a call center employee named {name} calling a patient to determine the rate at which they are adhering to their prescription.

    If the patient's adherence rate is low, extract a reason.

    You are time constrained and need to keep the call brief.

    You work at the Out of Pocket Medical Center.

    Once the call is over return just the word "DONE" all capitals with nothing else."""

    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            *messages,
        ],
    )

    content = response.choices[0].message.content or ""

    if content.strip().endswith("DONE"):
        content = content[:content.rindex("DONE")].strip()
        return content, True

    return content, False