from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
import json
import os
import copy
from templates.nodule_template import nodule_template, nodule_candidates, encode_candidate_tokens

model_id = "/space/chuang/MetaModels/Meta-Llama-3.1-405B-Instruct-FP8-dynamic-HF"

number_gpus = 8

sampling_params = SamplingParams(temperature=1.0, top_p=0.9, max_tokens=8192*2)

special_tokens = list(nodule_candidates.keys())
tokenizer = AutoTokenizer.from_pretrained(model_id, additional_special_tokens=special_tokens)

candidate_tokens_dict = encode_candidate_tokens(tokenizer, candidate_dict=nodule_candidates)

system_instruction_path = 'templates/nodule_instruction.txt'
free_text_reports_folder = 'free_text_reports'
structured_reports_folder = 'structured_reports'

if not os.path.exists(structured_reports_folder):
    os.makedirs(structured_reports_folder)

with open(system_instruction_path, 'r') as f:
    system_instruction = f.read()

report_files = os.listdir(free_text_reports_folder)

prompts_all = []
template_all = []
report_ids = []
date_all = []
num_data = len(report_files)
for n in range(0, num_data):

    file_name = report_files[n]
    report_id = file_name.split('.')[0]

    report_file_path = '{}/{}'.format(free_text_reports_folder, file_name)

    with open(report_file_path, 'r') as f:
        report = f.read()

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": report},
    ]

    prompts = tokenizer.apply_chat_template(messages, add_generation_prompt=True, tokenize=False)

    prompts_all.append(prompts)
    report_ids.append(report_id)
    template_all.append(copy.deepcopy(nodule_template))


llm = LLM(model=model_id, tensor_parallel_size=number_gpus, max_model_len=16384*2, additional_special_tokens=special_tokens)
outputs = llm.generate(prompts_all, sampling_params, templates=template_all, candidate_tokens_dict=candidate_tokens_dict)

num_outputs = len(outputs)
for n in range(0, num_outputs):
    report_id = report_ids[n]
    result_txt = outputs[n].outputs[0].text
    try:
        nodules_list = json.loads(result_txt)
        print(report_id, n, num_outputs)

        with open('{}/{}.json'.format(structured_reports_folder, report_id), 'w') as json_file:
            json.dump(nodules_list, json_file, indent=4)
    except:
        print(report_id, result_txt)

