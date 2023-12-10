import json
import matplotlib.pyplot as plt
import numpy as np
from rouge import Rouge

def main():
    # You can adjust this parameter for more or less smoothing
    smoothness_factor = 50
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")

    base_scores = evaluate_accuracy(base_dataset, "Base")
    finetuned_scores = evaluate_accuracy(finetuned_dataset, "Finetuned")
    prompt_engineered_scores = evaluate_accuracy(prompt_engineered_dataset, "Prompt Engineered")

    plot_scores(
        ["Base", "Finetuned", "Prompt Engineered"],
        [base_scores, finetuned_scores, prompt_engineered_scores],
        smoothness_factor,
    )

def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
    return dataset

def evaluate_accuracy(dataset, label):
    rouge_scores = []

    for data in dataset:
        reference = data["reference"]
        candidate = data["candidate"]

        # Calculate ROUGE-1 score
        rouge_score = calculate_rouge(reference, candidate)
        rouge_scores.append(rouge_score)

    # Calculate and print the average ROUGE score for the dataset
    average_rouge_score = sum(rouge_scores) / len(rouge_scores)
    print(f"{label} Average ROUGE Score: {average_rouge_score:.4f}")
    return rouge_scores, average_rouge_score

def calculate_rouge(reference, candidate):
    # Calculate ROUGE-1 score using the rouge library
    rouge = Rouge()
    scores = rouge.get_scores(candidate, reference)
    rouge_score = scores[0]["rouge-1"]["f"]
    return rouge_score

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")

def plot_scores(labels, scores, smoothness_factor):
    plt.figure(figsize=(10, 6))

    for i in range(len(labels)):
        rouge_scores, average_rouge_score = scores[i]
        smoothed_scores = moving_average(rouge_scores, smoothness_factor)
        plt.plot(smoothed_scores, label=f"{labels[i]} (Avg: {average_rouge_score:.4f})")

    plt.title("Smoothed ROUGE-1 Scores for Different Models")
    plt.xlabel("Sample")
    plt.ylabel("ROUGE-1 Score")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
