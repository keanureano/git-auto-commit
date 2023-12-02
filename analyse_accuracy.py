import json
import matplotlib.pyplot as plt
import numpy as np
from nltk.translate.bleu_score import sentence_bleu


def main():
    # You can adjust this parameter for more or less smoothing
    smoothness_factor = 50
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")

    base_scores = evaluate_accuracy(base_dataset, "Base")
    finetuned_scores = evaluate_accuracy(finetuned_dataset, "Finetuned")
    prompt_engineered_scores = evaluate_accuracy(
        prompt_engineered_dataset, "Prompt Engineered"
    )

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
    bleu_scores = []

    for data in dataset:
        reference = data["reference"].split()
        candidate = data["candidate"].split()

        # Calculate BLEU score using sentence_bleu
        bleu_score = calculate_bleu(reference, candidate)
        bleu_scores.append(bleu_score)

    # Calculate and print the average BLEU score for the dataset
    average_bleu_score = sum(bleu_scores) / len(bleu_scores)
    print(f"{label} Average BLEU Score: {average_bleu_score:.4f}")
    return bleu_scores, average_bleu_score


def calculate_bleu(reference, candidate):
    # Calculate BLEU score using sentence_bleu
    bleu_score = sentence_bleu([reference], candidate, weights=(1, 0, 0, 0))
    return bleu_score


def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode="valid")


def plot_scores(labels, scores, smoothness_factor):
    plt.figure(figsize=(10, 6))

    for i in range(len(labels)):
        bleu_scores, average_bleu_score = scores[i]
        smoothed_scores = moving_average(bleu_scores, smoothness_factor)
        plt.plot(smoothed_scores, label=f"{labels[i]} (Avg: {average_bleu_score:.4f})")

    plt.title("Smoothed BLEU Scores for Different Models")
    plt.xlabel("Sample")
    plt.ylabel("BLEU Score")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
