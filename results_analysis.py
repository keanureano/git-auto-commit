import json


def main():
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")


def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
    return dataset


if __name__ == "__main__":
    main()
