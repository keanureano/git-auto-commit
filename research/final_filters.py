import json
import matplotlib.pyplot as plt

def main():
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")

    combined_filtered, combined_failed, combined_total_ratio = combine_filters(
        base_dataset, finetuned_dataset, prompt_engineered_dataset, "candidate"
    )

    print_total_ratio("Combined", combined_total_ratio)

    plot_pie_chart("Combined", combined_filtered, combined_failed)

def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def combine_filters(base_dataset, finetuned_dataset, prompt_engineered_dataset, key):
    combined_filtered, combined_failed = [], []

    for index, dataset in enumerate([base_dataset, finetuned_dataset, prompt_engineered_dataset]):
        filtered, failed, _ = apply_filters(dataset, key)
        combined_filtered.extend(filtered)
        combined_failed.extend(failed)

    combined_total_ratio = len(combined_filtered) / sum(len(dataset) for dataset in [base_dataset, finetuned_dataset, prompt_engineered_dataset])

    return combined_filtered, combined_failed, combined_total_ratio

def apply_filters(dataset, key):
    filtered, failed = [], []
    for index, data in enumerate(dataset):
        if is_valid_data(data.get(key, ""), index):
            filtered.append(data)
        else:
            failed.append(data)

    total_ratio = len(filtered) / len(dataset)
    return filtered, failed, total_ratio

def is_valid_data(text, index):
    return len(text) >= 40

def print_total_ratio(model_name, total_ratio):
    print(f"{model_name} Total Ratio: {total_ratio:.1%}")

def plot_pie_chart(model_name, filtered_dataset, failed_dataset):
    sizes = [len(filtered_dataset), len(failed_dataset)]

    # Remove labels
    labels = ["" for _ in sizes]

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=['green', 'red'])
    plt.axis("equal")
    plt.title("Prompts Passed and Failed the Filter ( N Total )")

    # Add legend
    plt.legend(["Passed", "Failed"], loc="upper right")
    
    plt.show()

if __name__ == "__main__":
    main()
