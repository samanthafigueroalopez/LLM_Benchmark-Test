# test the llms and benchmark them
# all llms with ollama downloaded locally

TASKS = {
    "reasoning": [
        {
            "prompt": (
                "A total of 20 students did the homework assignement. But only 7 did it correctly . "
                "How many students did the homework assignment incorrectly? Explain your reasoning briefly."
            ),
            "notes": "Classic trick question, answer is 13. Checks careful reading vs pattern-matching.",
        },
        {
            "prompt": (
                "Three friends split a restaurant bill of $87 evenly, then "
                "a $12 tip is added and split evenly too. How much does "
                "each person pay in total?"
            ),
            "notes": "Answer: $33 each. Checks multi-step arithmetic reasoning.",
        },
    ],
    "coding": [
        {
            "prompt": (
                "Write a Python function `is_palindrome(s)` that returns "
                "True if a string is a palindrome, ignoring case, spaces, "
                "and punctuation. Include one example call."
            ),
            "notes": "Checks correctness, edge-case handling, and code cleanliness.",
        },
        {
            "prompt": (
                "Here is buggy Python code:\n\n"
                "def get_average(nums):\n"
                "    total = 0\n"
                "    for n in nums:\n"
                "        total =+ n\n"
                "    return total / len(nums)\n\n"
                "Find and fix the bug. Explain what was wrong."
            ),
            "notes": "Bug is `=+` instead of `+=`. Checks bug-spotting, not just code generation.",
        },
    ],
    "math": [
        {
            "prompt": (
                "If a train travels 60 miles in 45 minutes, what is its "
                "speed in miles per hour? Show your work."
            ),
            "notes": "Answer: 80 mph. Checks unit conversion + arithmetic.",
        },
    ],
    "instruction_following": [
        {
            "prompt": (
                "Write exactly three bullet points (no more, no less) "
                "summarizing why unit tests are useful. Each bullet must "
                "be under 12 words."
            ),
            "notes": "Checks strict constraint-following (count + length limits).",
        },
        {
            "prompt": (
                "Respond to this message with valid JSON only, no other "
                "text, with keys 'summary' and 'sentiment': "
                "'I waited two hours for support and nobody ever called back.'"
            ),
            "notes": "Checks structured-output reliability — common agent/tool-use skill.",
        },
    ],
}
