
def baseline(question: str) -> str:
    """
    Zero-shot: just the question, nothing added.
    This is the control condition everything else is compared against.
    """
    return question
 
 
def few_shot(question: str) -> str:
    """
    Shows the model 1-2 solved examples before the real question, so it
    can pattern-match the expected reasoning style and answer format.
 
    The examples here are deliberately unrelated to the benchmark
    questions (different topic) — we're teaching a *pattern*, not
    giving away the answer.
    """
    examples = (
        "Q: A shirt costs $20 and is on sale for 25% off. What is the sale price?\n"
        "A: 25% of $20 is $5. $20 - $5 = $15. The sale price is $15.\n\n"
        "Q: If a car travels 120 miles in 2 hours, what is its speed?\n"
        "A: Speed = distance / time = 120 / 2 = 60. The speed is 60 mph.\n\n"
    )
    return examples + f"Q: {question}\nA:"
 
 
def chain_of_thought(question: str) -> str:
    """
    Explicitly instructs the model to reason step by step before
    answering, rather than jumping straight to a final answer.
    """
    return f"{question}\nLet's think step by step, then give the final answer."
 
 
def role_prompting(question: str) -> str:
    """
    Assigns the model an expert persona before asking the question.
    Tests whether framing changes depth/rigor of the answer, even though
    the underlying question is identical.
    """
    return (
        "You are a meticulous expert who double-checks every claim before "
        "answering and never guesses.\n\n"
        f"{question}"
    )
 
 
def self_critique(question: str) -> str:
    """
    Asks the model to answer, then review and correct its own answer,
    in a single prompt. Tests whether models catch their own mistakes
    when explicitly told to check.
    """
    return (
        f"{question}\n\n"
        "First give your answer. Then, in a section labeled 'Self-check:', "
        "review your own answer for mistakes and correct it if needed."
    )
 
 
def least_to_most(question: str) -> str:
    """
    Asks the model to break the problem into smaller sub-questions first,
    then solve each one before combining into a final answer. Different
    from chain_of_thought: CoT asks for reasoning narration, this asks
    for explicit problem decomposition first.
    """
    return (
        f"{question}\n\n"
        "Break this into smaller sub-questions first, solve each "
        "sub-question one at a time, then combine them into a final answer."
    )
 
 
# Registry so the runner can loop over techniques by name
TECHNIQUES = {
    "baseline": baseline,
    "few_shot": few_shot,
    "chain_of_thought": chain_of_thought,
    "role_prompting": role_prompting,
    "self_critique": self_critique,
    "least_to_most": least_to_most,
}
