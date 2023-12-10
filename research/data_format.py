import json
import random


def main():
    dataset = load_json("raw_data/filtered_commits.json")

    # Grab the commit messages that passed the filter, randomize after
    dataset = dataset.get("passed")
    random.shuffle(dataset)

    # Only grab 500 items, randomize again
    dataset = dataset[:500]
    random.shuffle(dataset)

    total_size = len(dataset)
    # Training data will be 70%
    train_size = int(0.7 * total_size)

    # Testing data will be 15%
    test_size = int(0.15 * total_size)

    # Validation data will be 15%
    val_size = total_size - train_size - test_size

    train_data = dataset[:train_size]
    test_data = dataset[train_size : train_size + test_size]
    val_data = dataset[total_size - val_size :]

    print("Total Data:", total_size)
    print("Training Data:", train_size)
    print("Testing Data:", test_size)
    print("Validation Data:", val_size)

    # Write datasets to separate jsonl files
    write_jsonl(train_data, "train.jsonl")
    write_jsonl(test_data, "test.jsonl")
    write_jsonl(val_data, "val.jsonl")


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_jsonl(dataset, filename):
    with open(filename, "w") as file:
        for data in dataset:
            json.dump(format_as_prompt(data), file)
            file.write("\n")


def format_as_prompt(data):
    # Format the data as an openai prompt
    prompt = {
        "messages": [
            {
                "role": "system",
                "content": "Summarize diff logs with a commit message.",
            },
            {"role": "user", "content": data.get("diff")},
            {
                "role": "assistant",
                "content": data.get("message"),
            },
        ]
    }
    return prompt


if __name__ == "__main__":
    main()
