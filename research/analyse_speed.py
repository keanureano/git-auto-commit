import json
import matplotlib.pyplot as plt
import numpy as np


def main():
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")
    plot_response_time(base_dataset, "Base Model")
    plot_response_time(finetuned_dataset, "Fine-tuned Model")
    plot_response_time(prompt_engineered_dataset, "Prompt Engineered Model")
    plt.xlabel("Log Entry")
    plt.ylabel("Response Time (seconds)")
    plt.title("Response Time for Different Models")
    plt.legend()
    plt.show()


def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
    return dataset


def plot_response_time(dataset, label):
    response_times = [entry["time"] for entry in dataset]
    average_time = np.mean(response_times)
    std_deviation = np.std(response_times)

    plt.plot(response_times, label=f"{label}")
    plt.axhline(y=average_time, linestyle="--", color="gray", label=f"(Avg: {average_time:.2f}, Std Dev: {std_deviation:.2f})")


if __name__ == "__main__":
    main()
