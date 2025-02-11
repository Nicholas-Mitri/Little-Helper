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
        messages=messages,  # type: ignore
        response_format=response_format if response_format else None,  # type: ignore
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


def read_sys_prompt(filename):
    """
    Read and return the system prompt from a text file.

    Parameters:
    filename (str): Path to the file containing the system prompt.

    Returns:
    str: The system prompt text if successful, error message if failed.
    """
    try:
        with open(filename, "r") as f:
            system_prompt = f.read().strip()
            return system_prompt
    except FileNotFoundError:
        return "No system prompt file found"
    except Exception as e:
        return f"Error reading system prompt: {str(e)}"


def read_response_format(filename):
    """
    Read and parse the response format from a JSON file.

    Parameters:
    filename (str): Path to the JSON file containing response format.

    Returns:
    dict: The parsed response format if successful, error message if failed.
    """
    try:
        with open(filename, "r") as f:
            response_format = json.loads(f.read())
            return response_format
    except FileNotFoundError:
        return "No format file file found"
    except Exception as e:
        return f"Error reading format file: {str(e)}"


if __name__ == "__main__":
    # Load system prompt from configuration file
    system_prompt = read_sys_prompt("system_prompt.txt")

    # Example user prompt for testing
    user_prompt = "add hello world code to file with path /usr/hajj/main.py. import numpy in file with path /usr/hajj2/main.py and calculate the mean of an array"

    # Load response format configuration
    response_format = read_response_format("response_format.json")

    # Get and time the response from the model
    time_start = time.perf_counter()
    response_text = send_system_and_user_prompts(
        system_prompt, user_prompt, response_format
    )
    time_stop = time.perf_counter()
    print(f"GPT-4 Response in {time_stop - time_start:.2f} seconds:\n\n{response_text}")
