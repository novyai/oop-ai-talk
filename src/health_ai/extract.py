from health_ai.ai import instructor_client
from health_ai.schemas import PatientPrescriptionAdherence


async def extract_adhereance_result(conversation: str) -> PatientPrescriptionAdherence:
    system_prompt = "You an expert healthcare ops person reviewing patient adherence call logs"
    user_prompt_format = """Looking at the following call log:
    {conversation}"

    Determine the rate at which the user is adhering to their prescription.
    If it's low, extract a reason.
    """

    response = await instructor_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_format.format(conversation=conversation)},
        ],
        response_model=PatientPrescriptionAdherence
    )

    return response
