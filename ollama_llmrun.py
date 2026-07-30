import json
import time
from pathlib import Path
 
import ollama
 
from benchmarking_llm import TASKS
from models_figu import OLLAMA_MODELS
import prompting_techniques as pt

# For quick runs limit to two fast techniques: baseline and few_shot
TECHNIQUES = {k: v for k, v in pt.TECHNIQUES.items() if k in ("baseline", "few_shot")}
 
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
 
 
def run_all() -> dict:
    results = {}
 
    for model_name, model_tag in OLLAMA_MODELS.items():
        print(f"\n=== {model_name} ({model_tag}) ===")
        results[model_name] = {"tag": model_tag, "categories": {}}
 
        for category, tasks in TASKS.items():
            results[model_name]["categories"][category] = []
 
            for i, task in enumerate(tasks):
                # Run this same question through every prompting technique
                task_result = {
                    "base_prompt": task["prompt"],
                    "notes": task["notes"],
                    "techniques": {},
                }
 
                for technique_name, technique_fn in TECHNIQUES.items():
                    wrapped_prompt = technique_fn(task["prompt"])
                    print(
                        f"  [{category} #{i+1} / {technique_name}] running...",
                        end=" ",
                        flush=True,
                    )
                    try:
                        result = run_single_task(model_tag, wrapped_prompt)
                        print(f"done ({result['elapsed_seconds']}s)")
                    except Exception as e:
                        result = {"error": str(e)}
                        print(f"FAILED: {e}")
 
                    task_result["techniques"][technique_name] = result
 
                results[model_name]["categories"][category].append(task_result)
 
    return results
 
 
def save_results(results: dict):
    RESULTS_PATH.parent.mkdir(exist_ok=True)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {RESULTS_PATH}")
 
 
def print_summary(results: dict):
    print("\n" + "=" * 60)
    print("SUMMARY (avg response time by technique)")
    print("=" * 60)
    for model_name, data in results.items():
        # Flatten every technique-result across every task into one list
        all_results = []
        for cat in data["categories"].values():
            for task_result in cat:
                for technique_name, r in task_result["techniques"].items():
                    if "error" not in r:
                        all_results.append((technique_name, r))
 
        if not all_results:
            print(f"{model_name}: all tasks failed")
            continue
 
        print(f"\n{model_name}:")
        for technique_name in TECHNIQUES:
            times = [r["elapsed_seconds"] for name, r in all_results if name == technique_name]
            if times:
                avg = sum(times) / len(times)
                print(f"    {technique_name:20s} avg_time={avg:.2f}s  (n={len(times)})")
 
 
if __name__ == "__main__":
    results = run_all()
    save_results(results)
    print_summary(results)
 