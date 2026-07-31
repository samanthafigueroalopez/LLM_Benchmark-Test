import argparse
import json
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results"


def load_json(path: Path):
    if not path.exists():
        print(f"File not found: {path}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def print_ollama_results(data):
    print("\nOllama benchmark results:\n")
    if not isinstance(data, dict):
        print("Expected Ollama JSON to be a dictionary.")
        return
    for model_name, model_data in data.items():
        print(f"Model: {model_name}")
        for category, tasks in model_data.get("categories", {}).items():
            print(f"  Category: {category}")
            for i, task in enumerate(tasks, start=1):
                result = task.get("result", {})
                print(f"    Task {i} prompt: {task.get('base_prompt')}")
                print(f"      elapsed_seconds: {result.get('elapsed_seconds')}")
                print(f"      output_tokens: {result.get('output_tokens')}")
                print(f"      output: {result.get('output')!r}\n")


def print_hf_results(data):
    print("\nHugging Face benchmark results:\n")
    if not isinstance(data, list):
        print("Expected HF JSON to be a list.")
        return
    for i, item in enumerate(data, start=1):
        print(f"Result {i}: model_id={item.get('model_id')}")
        print(f"  prompt: {item.get('prompt')}")
        print(f"  load_seconds: {item.get('load_seconds')}")
        print(f"  inference_seconds: {item.get('inference_seconds')}")
        print(f"  total_seconds: {item.get('load_seconds',0) + item.get('inference_seconds',0)}")
        print(f"  output: {item.get('output')!r}\n")


def main():
    parser = argparse.ArgumentParser(description="View benchmark results from the results folder.")
    parser.add_argument("--ollama", action="store_true", help="Show Ollama benchmark outputs")
    parser.add_argument("--hf", action="store_true", help="Show Hugging Face benchmark outputs")
    args = parser.parse_args()

    if not args.ollama and not args.hf:
        args.ollama = args.hf = True

    if args.ollama:
        path = RESULTS_DIR / "ollama_results.json"
        data = load_json(path)
        if data is not None:
            print_ollama_results(data)

    if args.hf:
        path = RESULTS_DIR / "hf_results.json"
        data = load_json(path)
        if data is not None:
            print_hf_results(data)


if __name__ == "__main__":
    main()
