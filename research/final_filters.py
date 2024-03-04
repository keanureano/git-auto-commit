import json
import matplotlib.pyplot as plt

def main():
    dataset = load_dataset("base_model_results")
    print("Dataset:")
    print(json.dumps(dataset, indent=2))  
    plt.show()

def load_dataset(data_path):
    with open(f"test_results/{data_path}.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f]
    return dataset

if __name__ == "__main__":
    main()
