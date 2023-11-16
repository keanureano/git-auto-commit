import json
import spacy
import stanza


def main():
    data = load_json("all_commits_facebook_react.json")
    messages = [item["message"] for item in data]
    cleaned_messages = cleanup(messages)
    filtered_messages = filter(cleaned_messages[0:100])
    print("Filtered Messages:", filtered_messages[0:10])


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


def cleanup(messages):
    cleaned_messages = []
    for message in messages:
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
        cleaned_messages.append(message)
    return cleaned_messages


def filter(messages):
    spacy_nlp = spacy.load("en_core_web_sm")
    stanza_nlp = stanza.Pipeline("en")

    filtered_messages = []
    for message in messages:
        print("Filtering", message)

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

        filtered_messages.append(message)

    return filtered_messages


if __name__ == "__main__":
    main()
