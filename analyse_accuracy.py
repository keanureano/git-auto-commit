import json
import matplotlib.pyplot as plt
import numpy as np
from nltk.translate import meteor
from nltk.tokenize import word_tokenize
import nltk

def main():
    nltk.download("punkt")
    nltk.download("wordnet")
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")

    base_scores = evaluate_accuracy(base_dataset, "Base")
    finetuned_scores = evaluate_accuracy(finetuned_dataset, "Finetuned")
    prompt_engineered_scores = evaluate_accuracy(prompt_engineered_dataset, "Prompt Engineered")

    smoothness_factor = 50  # You can adjust this parameter for more or less smoothing

    plot_scores(
        ["Base", "Finetuned", "Prompt Engineered"],
        [base_scores, finetuned_scores, prompt_engineered_scores],
        smoothness_factor
    )

def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
    return dataset

def evaluate_accuracy(dataset, label):
    meteor_scores = []

    for data in dataset:
        reference = word_tokenize(data["reference"])
        candidate = word_tokenize(data["candidate"])

        # Calculate METEOR score
        meteor_score = meteor([reference], candidate)
        meteor_scores.append(meteor_score)

    # Calculate and return the average METEOR score for the dataset
    average_meteor_score = sum(meteor_scores) / len(meteor_scores)
    print(f"{label} Average METEOR Score: {average_meteor_score:.4f}")
    return meteor_scores

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

def plot_scores(labels, scores, smoothness_factor):
    plt.figure(figsize=(10, 6))
    
    for i in range(len(labels)):
        smoothed_scores = moving_average(scores[i], smoothness_factor)
        plt.plot(smoothed_scores, label=labels[i])

    plt.title("Smoothed METEOR Scores for Different Datasets")
    plt.xlabel("Sample")
    plt.ylabel("METEOR Score")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
