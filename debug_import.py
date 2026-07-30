import sys, importlib
sys.path.insert(0, r'c:/Users/saman/Downloads/FA26 -LLM(exp)')
try:
    m = importlib.import_module('benchmarking_llm')
    print('MODULE FILE:', getattr(m, '__file__', None))
    print('MODULE DIR LISTING SAMPLE:', [n for n in dir(m) if n.isupper()][:20])
    print('HAS TASKS ATTR:', hasattr(m, 'TASKS'))
    if hasattr(m, 'TASKS'):
        try:
            print('TASKS TYPE:', type(m.TASKS))
            print('TASKS KEYS:', list(m.TASKS.keys()))
        except Exception as e:
            print('ERROR reading TASKS:', e)
except Exception as e:
    print('IMPORT ERROR:', repr(e))
