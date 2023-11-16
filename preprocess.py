import json
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
    for index, data in enumerate(dataset):
        cleaned_data = {"message": "", "diff": ""}

        message = data.get("message", "")
        print(f"[{index}] Cleaning {message}")

        message = message[message.find(":") + 1 :].strip()
        message = message[message.find("]") + 1 :].strip()
        message = message[message.find("]") + 1 :].strip()
        message = (
            message[: message.find("\n")].strip()
            if message.find("\n") != -1
            else message.strip()
        )
        message = message[: message.find("(")].strip()
        message = message.lower()

        diff = data.get("diff", "")
        diff = diff[:4096].strip()

        cleaned_data["message"] = message
        cleaned_data["diff"] = diff
        cleaned_dataset.append(cleaned_data)

    return cleaned_dataset


def filter(dataset):
    spacy_nlp = spacy.load("en_core_web_sm")
    stanza_nlp = stanza.Pipeline("en")

    filtered_dataset = []
    for index, data in enumerate(dataset):
        message = data.get("message")
        print(f"[{index}] Filtering {message}")

        # Check for empty messages or messages with fewer than 50 characters
        if len(message) < 1 or len(message) < 50:
            continue

        spacy_doc = spacy_nlp(message)
        stanza_doc = stanza_nlp(message)

        # Check for merge and bump commits
        if spacy_doc[0].text == "merge" or spacy_doc[0].text == "bump":
            continue

        # Check for verb using SpaCy or Stanza
        if (
            spacy_doc[0].pos_ != "VERB"
            or stanza_doc.sentences[0].words[0].upos != "VERB"
        ):
            continue

        filtered_dataset.append(data)

    return filtered_dataset


if __name__ == "__main__":
    main()
