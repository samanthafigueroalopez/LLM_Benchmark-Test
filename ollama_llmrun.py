import json
import time
from pathlib import Path
import argparse

import ollama

from benchmarking_llm import TASKS
from models_figu import OLLAMA_MODELS, QUICK_OLLAMA_MODELS
RESULTS_PATH = Path(__file__).parent / "results" / "ollama_results.json"
 
 
def run_single_task(model_tag: str, prompt: str) -> dict:
    """Send one prompt to one model and capture timing + output."""
    start = time.perf_counter()
    response = ollama.chat(
        model=model_tag,
        messages=[{"role": "user", "content": prompt}],
    )
    elapsed = time.perf_counter() - start
 
    content = response["message"]["content"]
 
    # Ollama returns eval_count (output tokens) and eval_duration (ns) when available
    eval_count = response.get("eval_count")
    eval_duration_ns = response.get("eval_duration")
    tokens_per_sec = None
    if eval_count and eval_duration_ns:
        tokens_per_sec = round(eval_count / (eval_duration_ns / 1e9), 2)
 
    return {
        "output": content,
        "elapsed_seconds": round(elapsed, 2),
        "tokens_per_sec": tokens_per_sec,
        "output_tokens": eval_count,
    }
 
 
def run_all(quick: bool = False, models: dict[str, str] | None = None) -> dict:
    results = {}
    models = models or OLLAMA_MODELS
 
    for model_name, model_tag in models.items():
        print(f"\n=== {model_name} ({model_tag}) ===")
        results[model_name] = {"tag": model_tag, "categories": {}}
 
        for category, tasks in TASKS.items():
            results[model_name]["categories"][category] = []

            iter_tasks = tasks[:1] if quick else tasks

            for i, task in enumerate(iter_tasks):
                task_result = {
                    "base_prompt": task["prompt"],
                    "notes": task["notes"],
                }
 
                prompt = task["prompt"]
                print(f"  [{category} #{i+1}] running...", end=" ", flush=True)
                try:
                    result = run_single_task(model_tag, prompt)
                    print(f"done ({result['elapsed_seconds']}s)")
                except Exception as e:
                    result = {"error": str(e)}
                    print(f"FAILED: {e}")
 
                task_result["result"] = result
                results[model_name]["categories"][category].append(task_result)
 
    return results
 
 
def save_results(results: dict):
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH}")
    # Also save a CSV summary for quick comparison
    csv_path = RESULTS_PATH.with_suffix('.csv')
    try:
        import csv

        with open(csv_path, 'w', newline='', encoding='utf-8') as cf:
            writer = csv.writer(cf)
            writer.writerow(["model", "category", "prompt", "inference_seconds", "output_tokens"])
            for model_name, data in results.items():
                for category, tasks in data.get('categories', {}).items():
                    for t in tasks:
                        r = t.get('result', {})
                        inf = r.get('elapsed_seconds') or r.get('inference_seconds') or ''
                        out_tokens = r.get('output_tokens', '')
                        writer.writerow([model_name, category, t.get('base_prompt'), inf, out_tokens])

        print(f"Saved Ollama CSV summary to {csv_path}")
        # Print small markdown table summary
        print('\nOLLAMA SUMMARY:')
        print('| Model | Category | Inference (s) | Output tokens |')
        print('|---|---|---:|---:|')
        for model_name, data in results.items():
            for category, tasks in data.get('categories', {}).items():
                for t in tasks:
                    r = t.get('result', {})
                    inf = r.get('elapsed_seconds') or r.get('inference_seconds') or ''
                    out_tokens = r.get('output_tokens', '')
                    print(f"| {model_name} | {category} | {inf} | {out_tokens} |")
    except Exception as exc:
        print(f"Could not write Ollama CSV summary: {exc}")
 
 
def print_summary(results: dict):
    print("\n" + "=" * 60)
    print("SUMMARY (average response time)")
    print("=" * 60)
    for model_name, data in results.items():
        all_results = []
        for cat in data["categories"].values():
            for task_result in cat:
                r = task_result["result"]
                if "error" not in r:
                    all_results.append(r)
 
        if not all_results:
            print(f"{model_name}: all tasks failed")
            continue
 
        print(f"\n{model_name}:")
        times = [r["elapsed_seconds"] for r in all_results]
        avg = sum(times) / len(times)
        print(f"    average_response_time={avg:.2f}s  (n={len(times)})")
 
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Ollama local benchmarks.")
    parser.add_argument("--quick", action="store_true", help="Run quick benchmark (only first task per category)")
    parser.add_argument("--small", action="store_true", help="Use a smaller, faster subset of Ollama models")
    args = parser.parse_args()

    if args.small:
        models = QUICK_OLLAMA_MODELS
    else:
        models = OLLAMA_MODELS

    results = run_all(quick=args.quick, models=models)
    save_results(results)
    print_summary(results)
 