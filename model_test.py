import json
import os
import time
from openai import APITimeoutError, OpenAI


prompt_engineered_text = """
Given a user-provided Git diff, generate a concise commit message summarizing the changes.
Follow the pattern: <action> <module/functionality> <details>.
Use all lowercase letters, use imperative action verbs, write just one line of commit message and nothing else.
"""

model_used = {
    "base": "gpt-3.5-turbo",
    "prompt_engineered": "gpt-3.5-turbo",
    "finetuned": "ft:gpt-3.5-turbo-0613:personal:git-auto-commit:8LkKaBz2",
}

client = OpenAI()


def main():
    dataset = load_jsonl("training_data/test.jsonl")

    # Test the base gpt 3.5 model
    base_model_results = test_model(dataset, "base")
    write_jsonl(base_model_results, "base_model_results.jsonl")

    # Test the prompt engineered model
    prompt_engineered_model_results = test_model(dataset, "prompt_engineered")
    write_jsonl(
        prompt_engineered_model_results, "prompt_engineered_model_results.jsonl"
    )

    # Test the finetuned model
    finetuned_model_results = test_model(dataset, "finetuned")
    write_jsonl(finetuned_model_results, "finetuned_model_results.jsonl")


def load_jsonl(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            data.append(json.loads(line).get("messages"))
    return data


def test_model(dataset, mode, max_retries=3, retry_interval=5):
    results = []

    print("Mode:", mode)

    for index, data in enumerate(dataset):
        start_time = time.time()  # Record the start time
        input_message = data[:2]
        reference = data[-1].get("content")

        print(f"[{index}] Reference:", reference)

        if mode == "prompt_engineered":
            # Replaces prompt
            input_message[0]["content"] = prompt_engineered_text

        retries = 0
        while retries < max_retries:
            try:
                response = client.chat.completions.create(
                    model=model_used.get(mode),
                    messages=input_message,
                    timeout=30,  # Set the timeout here
                )
                candidate = response.choices[0].message.content
                end_time = time.time()  # Record the end time
                result = {
                    "time": end_time - start_time,
                    "reference": reference,
                    "candidate": candidate,
                    "input": input_message,
                }
                print(f"[{index}] Candidate:", candidate)
                results.append(result)
                break  # Break out of the retry loop if successful

            except APITimeoutError:
                retries += 1
                print(f"Timeout occurred. Retrying ({retries}/{max_retries})...")
                time.sleep(
                    retry_interval
                )  # Wait for the specified interval before retrying

        if retries == max_retries:
            print(
                f"Max retries reached. No response within the specified time for input: {input_message}"
            )

    return results


def write_jsonl(dataset, filename):
    folder = "test_results"

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Combine the folder path and filename
    file_path = os.path.join(folder, filename)

    with open(file_path, "w") as file:
        for data in dataset:
            json.dump(data, file)
            file.write("\n")


if __name__ == "__main__":
    main()
