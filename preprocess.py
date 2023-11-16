def main():
    messages = [
        "Add a feature flag to enable expiration of retry lanes (#27694)",
        "Bump browserify-sign from 4.0.4 to 4.2.2 in /fixtures/expiration (#27600)",
        "Fix: Enable enableUnifiedSyncLane (#27646)",
    ]
    print(cleanup(messages))


def cleanup(messages):
    cleaned_messages = []
    for message in messages:
        message = "".join(char for char in message if char not in "()")
        message = message[message.find(":") + 1 :].strip()
        message = message[: message.find("#")].strip()
        message = message.lower()
        cleaned_messages.append(message)
    return cleaned_messages


if __name__ == "__main__":
    main()
