import time, json
from openai import OpenAI


def send_system_and_user_prompts(system_prompt, user_prompt, response_format=None):
    """
    Send system and user prompts to the OpenAI API and get a structured response.

    Parameters:
    system_prompt (str): The prompt for the system role.
    user_prompt (str): The prompt for the user role.
    response_format (dict, optional): The desired response format specification.
        Example: {"type": "json_object", "schema": {...}}

    Returns:
    str: The response content from the OpenAI model in the specified format.
    """
    client = OpenAI()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages, # type: ignore
        response_format=response_format if response_format else None # type: ignore
    )

    return completion.choices[0].message.content


def transcribe_audio(audio_file_path):
    """
    Transcribe an audio file using OpenAI's Whisper model.

    Parameters:
    audio_file_path (str): The file path to the audio file.

    Returns:
    str: The transcribed text from the audio file.
    """
    client = OpenAI()
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", file=audio_file
        )
    return transcription.text


if __name__ == "__main__":

    # Load system prompt from file
    with open('system_prompt.txt', 'r') as f:
        system_prompt = f.read().strip()

    user_prompt = "add hello world code to file with path /usr/hajj/main.py. import numpy in file with path /usr/hajj2/main.py and calculate the mean of an array"

    # Load response format from JSON file
    with open('response_format.json', 'r') as f:
        response_format = json.loads(f.read())

    # Get the response from the model
    time_start = time.perf_counter()
    response_text = send_system_and_user_prompts(system_prompt, user_prompt, response_format)
    time_stop = time.perf_counter()
    print(f"GPT-4 Response in {time_stop - time_start:.2f} seconds:\n\n{response_text}")
