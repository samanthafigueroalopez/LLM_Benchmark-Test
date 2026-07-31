"""Minimal local Hugging Face benchmark for small/pre-loaded models."""
from pathlib import Path
import argparse
import time

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
except ImportError as exc:
    raise SystemExit(
        "transformers is not installed. Run `python -m pip install transformers torch` in the venv."
    )


DEFAULT_MODELS = [
    "Qwen/Qwen2.5-1.5B-Instruct",
    "mistralai/Ministral-3-3B-Instruct-2512",
]

PROMPTS = [
    "Summarize the following in one sentence: The quick brown fox jumps over the lazy dog.",
    "Translate to Spanish: The weather is pleasant today.",
]


def benchmark_model(model_id: str, prompt: str):
    print(f"\n== Benchmarking {model_id} ==")
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")

    start = time.perf_counter()
    result = pipe(prompt, max_new_tokens=64, do_sample=False, num_return_sequences=1)
    elapsed = time.perf_counter() - start
    print(f"Prompt: {prompt}")
    print(f"Output: {result[0]['generated_text']}\nTime: {elapsed:.2f}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a tiny local HF benchmark.")
    parser.add_argument("models", nargs="*", default=DEFAULT_MODELS)
    args = parser.parse_args()

    for model_id in args.models:
        for prompt in PROMPTS:
            try:
                benchmark_model(model_id, prompt)
            except Exception as exc:
                print(f"Failed for {model_id}: {exc}")
