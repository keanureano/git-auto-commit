import json
import spacy
import matplotlib.pyplot as plt

def main():
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")

    base_filtered_dataset, base_failed_dataset, base_total_ratio = apply_filters(base_dataset, "candidate")
    finetuned_filtered_dataset, finetuned_failed_dataset, finetuned_total_ratio = apply_filters(finetuned_dataset, "candidate")
    prompt_engineered_filtered_dataset, prompt_engineered_failed_dataset, prompt_engineered_total_ratio = apply_filters(prompt_engineered_dataset, "candidate")

    print(f"Base Total Ratio: {base_total_ratio:.1%}")
    print(f"Fine-tuned Total Ratio: {finetuned_total_ratio:.1%}")
    print(f"Prompt Engineered Total Ratio: {prompt_engineered_total_ratio:.1%}")

    plot_pie_chart(
        "Base",
        ["Base Passed", "Base Failed"],
        [len(base_filtered_dataset), len(base_failed_dataset)]
    )

    plot_pie_chart(
        "Fine-tuned",
        ["Fine-tuned Passed", "Fine-tuned Failed"],
        [len(finetuned_filtered_dataset), len(finetuned_failed_dataset)]
    )

    plot_pie_chart(
        "Prompt Engineered",
        ["Prompt Engineered Passed", "Prompt Engineered Failed"],
        [len(prompt_engineered_filtered_dataset), len(prompt_engineered_failed_dataset)]
    )

def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
    return dataset

def apply_filters(dataset, key):
    spacy_nlp = spacy.load("en_core_web_sm")

    filtered_dataset = []
    failed_dataset = []
    for data in dataset:
        # Retained Spacy filters for 'candidate'
        if spacy_filter(data.get(key, ""), spacy_nlp) and len(data.get(key, "")) >= 50:
            filtered_dataset.append(data)
        else:
            failed_dataset.append(data)

    total_ratio = len(filtered_dataset) / len(dataset)
    return filtered_dataset, failed_dataset, total_ratio

def spacy_filter(text, spacy_nlp):
    spacy_doc = spacy_nlp(text)

    # Check if the Spacy document is not empty
    if spacy_doc and len(spacy_doc) > 0:
        spacy_first = spacy_doc[0]

        # Retained Spacy filters: Include only samples where the first word is a verb and the message is imperative
        return spacy_first.pos_ == "VERB" and (
            "Inf" in spacy_first.morph.get("VerbForm") or (
                spacy_first.dep_ == "ROOT" and spacy_first.morph.get("Mood") == "Imp"
            )
        )
    else:
        # Return False if the document is empty
        return False

def plot_pie_chart(model_name, labels, sizes):
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=['green', 'red'])
    plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(f"Items Passed and Failed the Filter - {model_name}")
    plt.show()

if __name__ == "__main__":
    main()
