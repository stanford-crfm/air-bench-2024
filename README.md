# air-bench-2024
AIR-Bench 2024 is a safety benchmark that aligns with emerging government regulations and company policies.



# eval tutorial

We have 3 pipelines:

- pipeline1 & pipeline2:

  - Step1 uses our prompt to attack one specific model, generate the model response.

  - Step2 uses gpt-4o to output a score and a short reason given the attack prompt and the model response. (We always use gpt-4o to evaluate.)

- pipeline3: using [HELM](https://github.com/stanford-crfm/helm/) to execute the whole pipeline.

For pipeline1 & pipeline2, please firstly create an `.env` file at root directory, include your OPENAI_KEY or TOGETHERAI_KEY in the file.

```
OPENAI_KEY = 'yourkey'
TOGETHERAI_KEY = 'yourkey'
```

you may need to install the following package:

```
pip install gpt_batch together
```



## Pipeline1: QA_eval

The pipeline1's file format is `json`.

- `pipeline1_step1_model_response.ipynb`: sample 5 prompt in each l2 index from air-bench, then use [together.ai](https://www.together.ai/) to generate response for a specific model. In our code, we use Llama-3-8b. You can change the model by editing the following code:

  ```
  model_name = 'Llama-3-8b' # will appear in the output file name
  ```

  ```
  llama3_8b_response = response("meta-llama/Llama-3-8b-chat-hf", system)
  # model string can be found at https://docs.together.ai/docs/inference-models
  ```
  
  the [together.ai doc](https://docs.together.ai/docs/quickstart) may be helpful reference.
  
  You may also change the together.ai module into API of other companies.

- `pipeline1_step2_QA_eval.ipynb`: use gpt-4o for evaluation.

  if you changed the model in step1, you should also edit:

  ```
  model_name = 'Llama-3-8b' # appear in the input & output file name
  ```



## Pipeline2: csv_eval

The pipeline2's file format is `csv`.

- `pipeline2_step1_model_response.ipynb`: sample 5 prompt in each l2 index from air-bench, then use [gpt_batch](https://github.com/fengsxy/gpt_batch) (this is a tool to batch process messages using OpenAI's GPT models) to generate response for a specific model. In our code, we use gpt-4-turbo. You can change the model by editing the following code:

  ```
  model_name = 'gpt-4-turbo'
  ```
  
  You may also change the gpt_batch module into API of other companies.

- `pipeline2_step2_csv_eval.ipynb`: use gpt-4o for evaluation.

  if you changed the model in step1, you should also edit:

  ```
  model_name = 'gpt-4-turbo'
  ```

  

## Pipeline3: HELM

example command-line commands:

```
pip install crfm-helm
export OPENAI_API_KEY="yourkey"
helm-run --run-entries air_bench_2024:model=text --models-to-run openai/gpt2 --suite run1 --max-eval-instances 10000
helm-summarize --suite run1
helm-server
```

then go to http://localhost:8000/ in your browser.

For details, please refer to the [HELM documentation](https://crfm-helm.readthedocs.io/) and the article on [reproducing leaderboards](https://crfm-helm.readthedocs.io/en/latest/reproducing_leaderboards/).

