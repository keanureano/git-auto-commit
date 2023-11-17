import json
import re
import matplotlib.pyplot as plt


def main():
    dataset = load_json("filtered_commits.json")
    plot_first_word_frequency(dataset)
    plot_category_distribution(dataset)
    plt.show()


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def plot_first_word_frequency(dataset):
    passed = dataset.get("passed")
    first_words = [
        re.match(r"\b(\w+)\b", data.get("message")).group(1) for data in passed
    ]
    word_counts = {}
    for word in first_words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Sort the word counts in descending order
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Get the top frequencies
    top_frequency_count = 9

    # Group others into a category
    other_count = sum(count for _, count in sorted_word_counts[top_frequency_count:])
    others_label = f"Others ({other_count} words)"
    word_counts = dict(
        sorted_word_counts[:top_frequency_count] + [(others_label, other_count)]
    )

    labels, counts = zip(*word_counts.items())

    plt.figure()
    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.title(
        f"Top {top_frequency_count} Frequencies of First Words in Commit Messages"
    )


def plot_category_distribution(dataset):
    categories_count = {}

    # Iterate through messages to identify unique categories
    for category in dataset:
        if category:
            categories_count.setdefault(category, 0)
        for _ in category:
            categories_count[category] = categories_count.get(category, 0) + 1

    labels = list(categories_count.keys())
    counts = list(categories_count.values())

    plt.figure()
    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.axis("equal")
    plt.title("Distribution of Message Categories")


if __name__ == "__main__":
    main()
