from pathlib import Path
import importlib.util
import os

print('Python executable:', os.sys.executable)
for pkg in ['transformers', 'torch', 'accelerate', 'huggingface_hub']:
    spec = importlib.util.find_spec(pkg)
    print(f'{pkg}:', 'installed' if spec else 'missing')

hf_home = os.environ.get('HF_HOME') or os.environ.get('HUGGINGFACE_HUB_CACHE') or Path.home() / '.cache' / 'huggingface' / 'hub'
print('HF cache path:', hf_home)
print('Exists:', hf_home.exists())
if hf_home.exists():
    entries = sorted([p.name for p in hf_home.iterdir() if p.is_dir()])
    print('Repo count:', len(entries))
    print('Sample entries:', entries[:20])
