"""List locally cached Hugging Face model repos (best-effort).

Prints directories under HF cache. Works on typical setups; adjust HF_HOME
or HF_CACHE_DIR if you customized the environment.
"""
from pathlib import Path
import os

def list_cached_models():
    hf_home = os.environ.get('HF_HOME') or os.environ.get('HUGGINGFACE_HUB_CACHE')
    if not hf_home:
        hf_home = Path.home() / '.cache' / 'huggingface' / 'hub'
    else:
        hf_home = Path(hf_home)

    print('Using HF cache path:', hf_home)
    if not hf_home.exists():
        print('No cache directory found. If you use a different cache, set HF_HOME env var.')
        return

    # List top-level cached repo dirs
    entries = [p for p in hf_home.iterdir() if p.is_dir()]
    if not entries:
        print('No cached model repos found under', hf_home)
        return

    print('\nCached repos:')
    for p in sorted(entries):
        try:
            size = sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
            print(f"- {p.name}  ({size//1024} KB)")
        except Exception:
            print(f"- {p.name}")

if __name__ == '__main__':
    list_cached_models()
