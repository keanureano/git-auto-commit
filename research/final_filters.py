import json
import spacy
import matplotlib.pyplot as plt

def main():
    base_dataset = load_dataset("base_model_results")
    finetuned_dataset = load_dataset("finetuned_model_results")
    prompt_engineered_dataset = load_dataset("prompt_engineered_model_results")

    base_filtered, base_failed, base_total_ratio = apply_filters(base_dataset, "candidate")
    finetuned_filtered, finetuned_failed, finetuned_total_ratio = apply_filters(finetuned_dataset, "candidate")
    prompt_engineered_filtered, prompt_engineered_failed, prompt_engineered_total_ratio = apply_filters(prompt_engineered_dataset, "candidate")

    print_total_ratio("Base", base_total_ratio)
    print_total_ratio("Fine-tuned", finetuned_total_ratio)
    print_total_ratio("Prompt Engineered", prompt_engineered_total_ratio)

    plot_pie_chart("Base", base_filtered, base_failed)
    plot_pie_chart("Fine-tuned", finetuned_filtered, finetuned_failed)
    plot_pie_chart("Prompt Engineered", prompt_engineered_filtered, prompt_engineered_failed)

def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

def apply_filters(dataset, key):
    spacy_nlp = spacy.load("en_core_web_sm")

    filtered, failed = [], []
    for data in dataset:
        if is_valid_data(data.get(key, ""), spacy_nlp, key):
            filtered.append(data)
        else:
            failed.append(data)

    total_ratio = len(filtered) / len(dataset)
    return filtered, failed, total_ratio

def is_valid_data(text, spacy_nlp, key):
    spacy_doc = spacy_nlp(text)

    if spacy_doc and len(spacy_doc) > 0:
        spacy_first = spacy_doc[0]
        return spacy_first.pos_ == "VERB" and (
            "Inf" in spacy_first.morph.get("VerbForm") or (
                spacy_first.dep_ == "ROOT" and spacy_first.morph.get("Mood") == "Imp"
            )
        ) and len(text) >= 50
    else:
        return False

def print_total_ratio(model_name, total_ratio):
    print(f"{model_name} Total Ratio: {total_ratio:.1%}")

def plot_pie_chart(model_name, filtered_dataset, failed_dataset):
    sizes = [len(filtered_dataset), len(failed_dataset)]
    labels = [f"{model_name} Passed", f"{model_name} Failed"]

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=['green', 'red'])
    plt.axis("equal")
    plt.title(f"Items Passed and Failed the Filter - {model_name}")
    plt.show()

if __name__ == "__main__":
    main()
