from argparse import ArgumentParser
from pathlib import Path
from huggingface_hub import snapshot_download

DEFAULT_MODELS = [
    "google/flan-t5-small",
]


def download_models(model_ids, cache_dir=None, resume=True):
    for model_id in model_ids:
        print(f"Downloading {model_id}...")
        path = snapshot_download(
            repo_id=model_id,
            cache_dir=cache_dir,
            resume_download=resume,
            local_files_only=False,
        )
        print(f"Downloaded {model_id} to {path}\n")


def parse_args():
    parser = ArgumentParser(description="Download Hugging Face model repositories locally.")
    parser.add_argument(
        "models",
        nargs="*",
        default=DEFAULT_MODELS,
        help="Hugging Face model IDs to download (default: google/flan-t5-small)",
    )
    parser.add_argument(
        "--cache-dir",
        default=None,
        help="Optional cache directory for Hugging Face downloads.",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Do not resume partial downloads.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    cache_dir = Path(args.cache_dir) if args.cache_dir else None
    download_models(args.models, cache_dir=cache_dir, resume=not args.no_resume)
