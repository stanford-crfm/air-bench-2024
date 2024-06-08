import csv
from gpt_batch.batcher import GPTBatcher
import pandas as pd

system = """You are a helpful assistant."""

batcher = GPTBatcher(api_key='',
                     model_name='gpt-4o',
                     system_prompt=system,
                     temperature=0,
                     num_workers=64,
                     timeout_duration=60,
                     retry_attempts=2,
                    )

def extract_content(tag, text):
    start_idx = text.find(tag)
    # if start_idx == -1:
    #     return None
    start_of_content = start_idx + len(tag)
    if tag == "##the_score: ":
        end_idx = text.find("\n", start_of_content)
    else:
        end_idx = text.find(".\n##", start_of_content)
    if end_idx == -1:
        content = text[start_of_content:].strip()
    else:
        content = text[start_of_content:end_idx].strip()
    return content

judge_prompt_file = pd.read_csv('judge_prompt_final.csv')

with open('example_response.csv', 'r', newline='', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    next(reader) # skip first row

    question_list = []
    row_list = []

    for i, row in enumerate(reader):
        cate_idx, l2_name, l3_name, l4_name, prompt, response = row
        # find corresponding judge_prompt
        judge_prompt_row = judge_prompt_file[judge_prompt_file['cate-idx'] == cate_idx]
        judge_prompt = judge_prompt_row.iloc[0]['judge_prompt']

        row_list.append([cate_idx, l2_name, l3_name, l4_name, prompt, response])
        question_list.append(judge_prompt.replace("{{QUESTION}}", prompt).replace("{{ANSWER}}", response))

# print(question_list[0])

result_list = batcher.handle_message_list(question_list)
reason_list = [extract_content("##short_reasoning: ", result) for result in result_list]
score_list = [float(extract_content("##the_score: ", result)) for result in result_list]

with open('{model_name}_result.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['cate-idx', 'l2-name', 'l3-name', 'l4-name', 'prompt', 'response','score_reason', 'score'])

    for i, row in enumerate(row_list):
        cate_idx, l2_name, l3_name, l4_name, prompt, response = row
        reason = reason_list[i]
        score = score_list[i]

        writer.writerow([cate_idx, l2_name, l3_name, l4_name, prompt, response, reason, score])