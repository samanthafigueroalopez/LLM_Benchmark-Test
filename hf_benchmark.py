from pathlib import Path
import argparse
import time
import json

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
except ImportError as exc:
    raise SystemExit(
        "transformers is not installed. Run `python -m pip install transformers torch` in the venv."
    )

from models_figu import HF_MODELS, QUICK_HF_MODELS

DEFAULT_MODELS = [
    HF_MODELS["qwen2.5"],
    HF_MODELS["mistralai-3b"],
]

# Small default prompt set for quick benchmarks
PROMPTS = [
    "Summarize briefly: The quick brown fox jumps over the lazy dog.",
]


def benchmark_model(model_id: str, prompt: str, max_new_tokens: int = 32):
    print(f"\n== Benchmarking {model_id} ==")
    load_start = time.perf_counter()
    model = AutoModelForCausalLM.from_pretrained(model_id, trust_remote_code=True)
    tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, device_map="auto")
    load_time = time.perf_counter() - load_start

    start = time.perf_counter()
    result = pipe(prompt, max_new_tokens=max_new_tokens, do_sample=False, num_return_sequences=1)
    elapsed = time.perf_counter() - start

    output_text = result[0].get("generated_text") or result[0].get("text")
    print(f"Prompt: {prompt}")
    print(f"Output: {output_text}\nLoad: {load_time:.2f}s Inference: {elapsed:.2f}s")

    return {
        "model_id": model_id,
        "prompt": prompt,
        "output": output_text,
        "load_seconds": round(load_time, 2),
        "inference_seconds": round(elapsed, 2),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a tiny local HF benchmark.")
    parser.add_argument("models", nargs="*", default=DEFAULT_MODELS)
    parser.add_argument("--max-tokens", type=int, default=32, help="Max new tokens for generation (default 32)")
    parser.add_argument("--quick", action="store_true", help="Run quick benchmark (only first prompt)")
    parser.add_argument("--small", action="store_true", help="Use a smaller, faster subset of Hugging Face models")
    parser.add_argument("--save", action="store_true", help="Save results to results/hf_results.json")
    args = parser.parse_args()

    results = []
    prompts = PROMPTS if not args.quick else PROMPTS[:1]
    models = QUICK_HF_MODELS.values() if args.small else args.models

    for model_id in models:
        for prompt in prompts:
            try:
                r = benchmark_model(model_id, prompt, max_new_tokens=args.max_tokens)
                results.append(r)
            except Exception as exc:
                print(f"Failed for {model_id}: {exc}")

    if args.save:
        out_path = Path(__file__).parent / "results" / "hf_results.json"
        out_path.parent.mkdir(exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"Saved HF results to {out_path}")
        # Also write a CSV summary for easy comparison
        csv_path = out_path.with_suffix('.csv')
        try:
            import csv

            with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
                writer = csv.writer(cf)
                writer.writerow(["model_id", "prompt", "load_seconds", "inference_seconds", "total_seconds"])
                for r in results:
                    load = r.get('load_seconds', '')
                    inf = r.get('inference_seconds', '')
                    total = (load or 0) + (inf or 0) if (load is not None and inf is not None) else ''
                    writer.writerow([r.get('model_id'), r.get('prompt'), load, inf, total])

            print(f"Saved HF CSV summary to {csv_path}")
            # Print small markdown table summary
            print('\nHF SUMMARY:')
            print('| Model | Load (s) | Inference (s) | Total (s) |')
            print('|---|---:|---:|---:|')
            for r in results:
                load = r.get('load_seconds', '')
                inf = r.get('inference_seconds', '')
                total = (load or 0) + (inf or 0) if (load is not None and inf is not None) else ''
                print(f"| {r.get('model_id')} | {load} | {inf} | {total} |")
        except Exception as exc:
            print(f"Could not write CSV summary: {exc}")
