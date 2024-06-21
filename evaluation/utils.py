import random

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

def sample_row(raw_data, sample_num):
    sample_row_list = []
    for l2 in range(1, 17):

        l2_specific_rows = []
        for i,data in enumerate(raw_data):
            cate_idx, l2_name, l3_name, l4_name, prompt = data.values()
            l2_index = int(cate_idx.split('.')[0])
            if l2_index == l2:
                l2_specific_rows.append((cate_idx, l2_name, l3_name, l4_name, prompt))
        
        l2_specific_sampled_row = random.sample(l2_specific_rows, sample_num)
        sample_row_list.extend(l2_specific_sampled_row)
    
    return sample_row_list