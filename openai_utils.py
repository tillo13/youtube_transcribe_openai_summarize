# Filename: openai_utils.py
import os
import time
import openai
from dotenv import load_dotenv

load_dotenv()   # take environment variables from .env.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Please make sure you have set `OPENAI_API_KEY` in your .env file."
MODEL_CHOICE = "gpt-3.5-turbo"

def get_chat_response(prompt):
    start_time = time.time()
    response = get_response(prompt, MODEL_CHOICE, OPENAI_API_KEY)
    duration = time.time() - start_time
    return response, duration

def get_summary_from_transcript(transcript):
    start_time = time.time()
    summary = get_summary(transcript, MODEL_CHOICE, OPENAI_API_KEY)
    duration = time.time() - start_time
    return summary, duration

def get_response(prompt, model, openai_secret_key):
    openai.api_key = openai_secret_key

    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,     # Lower temperature for more deterministic output.
        max_tokens=200       # Set a limit on response length for concise response.
    )
    return response.choices[0].message['content'].strip()

def get_summary(transcript, model, openai_secret_key):
    openai.api_key = openai_secret_key
    prompt = f"I have a transcript for a video that has up to 10 bullet points. Here is the transcript:\n\n{transcript}\n\nCould you provide a concise summary?"

    if model == "gpt-3.5-turbo":
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=0.2,     # Lower temperature for more deterministic output.
            max_tokens=200       # Set a limit on response length for concise summary.
        )
        summary = response.choices[0].message['content'].strip()

    else:
        raise ValueError('Model not recognized. Please use "gpt-3.5-turbo".')

    return summary

if __name__ == "__main__":
    prompt = "How was your day?"
    response, duration = get_chat_response(prompt)
    print("AI Response:")
    print(response)
    print(f"Generated in {duration} seconds.")