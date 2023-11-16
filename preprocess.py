import spacy


def main():
    messages = [
        "Add a feature flag to enable expiration of retry lanes (#27694)",
        "Bump browserify-sign from 4.0.4 to 4.2.2 in /fixtures/expiration (#27600)",
        "Fix: Enable enableUnifiedSyncLane (#27646)",
    ]
    cleaned_messages = cleanup(messages)
    filtered_messages = filter(cleaned_messages)
    print(filtered_messages)


def cleanup(messages):
    cleaned_messages = []
    for message in messages:
        message = "".join(char for char in message if char not in "()")
        message = message[message.find(":") + 1 :].strip()
        message = message[: message.find("#")].strip()
        message = message.lower()
        cleaned_messages.append(message)
    return cleaned_messages


def filter(messages):
    nlp = spacy.load("en_core_web_sm")
    filtered_messages = []
    for message in messages:
        doc = nlp(message)

        # Check for empty messages or messages with fewer than 50 characters
        if len(doc) < 1 or len(message) < 50:
            continue

        # Check for merge and bump
        if doc[0].text == "merge" or doc[0].text == "bump":
            continue

        # Check for verb in either spacy or stanza
        # if len([token.lemma_ for token in doc if token.pos_ == "VERB"]) < 1
        # or TODO:
        # continue

        filtered_messages.append(message)

    return filtered_messages


if __name__ == "__main__":
    main()
