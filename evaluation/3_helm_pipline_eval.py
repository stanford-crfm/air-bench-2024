import datasets

test_data = datasets.load_dataset("stanford-crfm/air-bench-2024", "default", split="test")
judge_prompt = datasets.load_dataset("stanford-crfm/air-bench-2024", "judge_prompts", split="test")

