import spacy
import stanza


def main():
    messages = [
        "Add a feature flag to enable expiration of retry lanes (#27694)",
        "Bump browserify-sign from 4.0.4 to 4.2.2 in /fixtures/expiration (#27600)",
        "Fix: Enable enableUnifiedSyncLane (#27646)",
    ]
    cleaned_messages = cleanup(messages)
    filtered_messages = filter(cleaned_messages)

    print("Filtered Messages:", filtered_messages)


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
    spacy_nlp = spacy.load("en_core_web_sm")
    stanza_nlp = stanza.Pipeline("en")

    filtered_messages = []
    for message in messages:
        spacy_doc = spacy_nlp(message)
        stanza_doc = stanza_nlp(message)

        # Check for empty messages or messages with fewer than 50 characters
        if len(spacy_doc) < 1 or len(message) < 50:
            continue

        # Check for merge and bump commits
        if spacy_doc[0].text == "merge" or spacy_doc[0].text == "bump":
            continue

        # Check for atleast 1 verb using SpaCy or Stanza
        if (
            len([token.lemma_ for token in spacy_doc if token.pos_ == "VERB"]) < 1
            or len(
                [
                    word.text
                    for sent in stanza_doc.sentences
                    for word in sent.words
                    if word.upos == "VERB"
                ]
            )
            < 1
        ):
            continue

        filtered_messages.append(message)

    return filtered_messages


if __name__ == "__main__":
    main()
