import ollama

response = ollama.chat(
    model="phi4-mini",
    messages=[{"role": "user", "content": "What is 2 + 2?"}]
)

print(response["message"]["content"])