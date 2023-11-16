import json
import re
import matplotlib.pyplot as plt


def main():
    dataset = load_json("filtered_commits_facebook_react_1.json")
    plot_first_word_frequency(dataset)


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def plot_first_word_frequency(dataset):
    first_words = [
        re.match(r"\b(\w+)\b", data.get("message")).group(1) for data in dataset
    ]
    word_counts = {}
    for word in first_words:
        word_counts[word] = word_counts.get(word, 0) + 1

    # Sort the word counts in descending order
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    # Get the top frequencies
    top_frequency_count = 20

    # Group others into a category
    other_count = sum(count for _, count in sorted_word_counts[top_frequency_count:])
    others_label = f"Others ({other_count} words)"
    word_counts = dict(
        sorted_word_counts[:top_frequency_count] + [(others_label, other_count)]
    )

    labels, counts = zip(*word_counts.items())

    plt.pie(counts, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.axis(
        "equal"
    )  # Equal aspect ratio ensures that the pie chart is drawn as a circle.

    plt.title(
        f"Top {top_frequency_count} Frequencies of First Words in Commit Messages"
    )
    plt.show()


if __name__ == "__main__":
    main()
