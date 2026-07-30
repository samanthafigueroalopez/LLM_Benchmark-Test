import sys, importlib
p = r'c:/Users/saman/Downloads/FA26 -LLM(exp)'
sys.path.insert(0, p)
print('FS read of benchmarking_llm.py:')
with open(p + '/benchmarking_llm.py', 'rb') as f:
    data = f.read()
    print('bytes len', len(data))
    print(data[:400].decode('utf-8', errors='replace'))
try:
    m = importlib.import_module('benchmarking_llm')
    print('\nMODULE __file__:', m.__file__)
    print('dir keys sample (first 100):', list(dir(m))[:100])
    print('TASKS in globals:', 'TASKS' in getattr(m, '__dict__', {}))
    print('globals keys upper-only:', [k for k in m.__dict__.keys() if k.isupper()])
except Exception as e:
    print('IMPORT ERROR:', e)
