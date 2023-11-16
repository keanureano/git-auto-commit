import json
import re
import spacy
import stanza


def main():
    dataset = load_json("all_commits_facebook_react.json")
    cleaned_dataset = cleanup(dataset)
    filtered_dataset = filter(cleaned_dataset)
    save_json(filtered_dataset, "filtered_commits_facebook_react.json")


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def save_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)


def cleanup(dataset):
    cleaned_dataset = []
    for data in dataset:
        cleaned_data = {"message": "", "diff": ""}
        message = data.get("message", "")

        # Keep only the first line of commit message
        message = (
            message[: message.find("\n")].strip()
            if message.find("\n") != -1
            else message.strip()
        )

        print("Raw", message)

        # Remove everything up to the first colon
        message = re.sub(r"^.*?:", "", message)

        # Remove square brackets and their contents
        message = re.sub(r"\[.*?\]", "", message)

        # Remove parentheses and their contents
        message = re.sub(r"\(.*?\)", "", message)

        # Strip and lowercaste message
        message = message.strip().lower()

        # Truncate the diff, will filter this later so it doesn't matter if it's truncated
        diff = data.get("diff", "")
        diff = diff[:10000].strip()

        print("Cleaned", message)

        cleaned_data["message"] = message
        cleaned_data["diff"] = diff
        cleaned_dataset.append(cleaned_data)

    return cleaned_dataset


def filter(dataset):
    spacy_nlp = spacy.load("en_core_web_sm")
    stanza_nlp = stanza.Pipeline("en")

    filtered_dataset = {
        "short_messages": [],
        "large_diffs": [],
        "bot_commits": [],
        "non_verbs": [],
        "non_imperatives": [],
        "passed": [],
    }

    for index, data in enumerate(dataset):
        message = data.get("message")
        diff = data.get("diff")

        # Check for short messages
        if len(message) < 50:
            filtered_dataset["short_messages"].append(message)
            continue

        # Check for large diffs
        if len(diff) > 2000:
            filtered_dataset["large_diffs"].append(message)
            continue

        # Check for bot commits
        if message.split()[0].lower() in ["merge", "bump"]:
            filtered_dataset["bot_commits"].append(message)
            continue

        spacy_doc = spacy_nlp(message)
        stanza_doc = stanza_nlp(message)
        spacy_first = spacy_doc[0]
        stanza_first = stanza_doc.sentences[0].words[0]

        # Check for verb
        if not (spacy_first.pos_ == "VERB" and stanza_first.upos == "VERB"):
            filtered_dataset["non_verbs"].append(message)
            continue

        # Check for imperative
        if not (
            "Inf" in spacy_first.morph.get("VerbForm")
            and stanza_first.deprel == "root"
            and "Mood=Imp" in stanza_first.feats
        ):
            filtered_dataset["non_imperatives"].append(message)
            continue

        print(f"[{index}] Filtered {message}")
        filtered_dataset["passed"].append(data)

    return filtered_dataset


if __name__ == "__main__":
    main()
