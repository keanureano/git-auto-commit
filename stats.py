import json


def main():
    dataset = load_json("filtered_commits_facebook_react.json")
    for index, data in enumerate(dataset):
        print(f"[{index}] {data.get('message', '')}")


def load_json(file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data


if __name__ == "__main__":
    main()
