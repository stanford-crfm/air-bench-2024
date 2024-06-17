import csv
import random
from gpt_batch.batcher import GPTBatcher
import datasets
import os
from dotenv import load_dotenv

test_data = datasets.load_dataset("stanford-crfm/air-bench-2024", "default", split="test")

system = """You are a helpful assistant."""

load_dotenv()
openai_key = os.getenv('OPENAI_KEY')

batcher = GPTBatcher(api_key=openai_key,
                     model_name='gpt-4-turbo',
                     system_prompt=system,
                     temperature=0,
                     num_workers=64,
                     timeout_duration=60,
                     retry_attempts=2,
                    )


row_list = []
question_list = []

for l2 in range(1, 17):
    l2_specific_rows = []

    for i,data in enumerate(test_data):
        cate_idx, l2_name, l3_name, l4_name, prompt = data.values()
        l2_index = int(cate_idx.split('.')[0])

        if l2_index == l2:
            l2_specific_rows.append((cate_idx, l2_name, l3_name, l4_name, prompt))

    # Randomly sample up to 5 rows from the eligible rows
    sampled_rows = random.sample(l2_specific_rows, 5)

    for cate_idx, l2_name, l3_name, l4_name, prompt in sampled_rows:
        question_list.append(prompt)
        row_list.append([cate_idx, l2_name, l3_name, l4_name, prompt])
        print(f"cate-idx: {cate_idx}")

result_list = batcher.handle_message_list(question_list)

with open('./evaluation/example_response.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['cate-idx', 'l2-name', 'l3-name', 'l4-name', 'prompt', 'response'])

    for i, row in enumerate(row_list):
        cate_idx, l2_name, l3_name, l4_name, prompt = row
        response = result_list[i]
        writer.writerow([cate_idx, l2_name, l3_name, l4_name, prompt, response])