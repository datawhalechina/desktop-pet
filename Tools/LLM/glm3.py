import json
import argparse
from typing import List, Tuple
from optimum.intel.openvino import OVModelForCausalLM
from transformers import (AutoTokenizer, AutoConfig,
                          TextIteratorStreamer, StoppingCriteriaList, StoppingCriteria)
import gradio as gr

def parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split('`')
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f'<br></code></pre>'
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", "\`")
                    line = line.replace("<", "&lt;")
                    line = line.replace(">", "&gt;")
                    line = line.replace(" ", "&nbsp;")
                    line = line.replace("*", "&ast;")
                    line = line.replace("_", "&lowbar;")
                    line = line.replace("-", "&#45;")
                    line = line.replace(".", "&#46;")
                    line = line.replace("!", "&#33;")
                    line = line.replace("(", "&#40;")
                    line = line.replace(")", "&#41;")
                    line = line.replace("$", "&#36;")
                lines[i] = "<br>" + line
    text = "".join(lines)
    return text


class StopOnTokens(StoppingCriteria):
    def __init__(self, token_ids):
        self.token_ids = token_ids

    def __call__(
            self, input_ids, scores, **kwargs
    ) -> bool:
        for stop_id in self.token_ids:
            if input_ids[0][-1] == stop_id:
                return True
        return False

def convert_history_to_token(history: List[Tuple[str, str]], tokenizer):

    messages = []
    for idx, (user_msg, model_msg) in enumerate(history):
        if idx == len(history) - 1 and not model_msg:
            messages.append({"role": "user", "content": user_msg})
            break
        if user_msg:
            messages.append({"role": "user", "content": user_msg})
        if model_msg:
            messages.append({"role": "assistant", "content": model_msg})

    model_inputs = tokenizer.apply_chat_template(messages,
                                                 add_generation_prompt=True,
                                                 tokenize=True,
                                                 return_tensors="pt")
    return model_inputs

class GLM3Class(object):
    def __init__(self, model_path="Source/Model/chatglm3-6b-ov"):
        self.chat_history = []

        # load model
        model_dir = model_path
        self.max_sequence_length = 256

        ov_config = {"PERFORMANCE_HINT": "LATENCY",
                     "NUM_STREAMS": "1", "CACHE_DIR": ""}

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_dir, trust_remote_code=True)

        print("====Compiling model====")
        self.ov_model = OVModelForCausalLM.from_pretrained(
            model_dir,
            device="CPU",
            ov_config=ov_config,
            config=AutoConfig.from_pretrained(model_dir, trust_remote_code=True),
            trust_remote_code=True,
        )

        self.streamer = TextIteratorStreamer(
            self.tokenizer, timeout=60.0, skip_prompt=True, skip_special_tokens=True
        )
        self.stop_tokens = [0, 2]
        self.stop_tokens = [StopOnTokens(self.stop_tokens)]


    def chat(self, prompt, role='user'):
        self.chat_history.append({'role': role, 'content': prompt})

        print(prompt)
        history = [[parse_text(prompt), ""]]
        model_inputs = convert_history_to_token(history, self.tokenizer)
        generate_kwargs = dict(
            input_ids=model_inputs,
            max_new_tokens=self.max_sequence_length,
            temperature=0.1,
            do_sample=True,
            top_p=1.0,
            top_k=50,
            repetition_penalty=1.1,
            streamer=self.streamer,
            stopping_criteria=StoppingCriteriaList(self.stop_tokens)
        )
        partial_text = self.ov_model.generate(**generate_kwargs)
        # print(f"raw data is: {partial_text}")
        partial_text = self.tokenizer.decode(partial_text[0])
        partial_text = partial_text.split("<|assistant|> \n ")[-1]
        print(partial_text)
        result = partial_text

        self.chat_history.append({'role': 'assistant', 'content': result})
        return result

    def get_llm_answer(self, prompt):
        print(prompt)
        history = [[parse_text(prompt), ""]]
        model_inputs = convert_history_to_token(history, self.tokenizer)
        generate_kwargs = dict(
            input_ids=model_inputs,
            max_new_tokens=self.max_sequence_length,
            temperature=0.1,
            do_sample=True,
            top_p=1.0,
            top_k=50,
            repetition_penalty=1.1,
            streamer=self.streamer,
            stopping_criteria=StoppingCriteriaList(self.stop_tokens)
        )
        partial_text = self.ov_model.generate(**generate_kwargs)
        # print(f"raw data is: {partial_text}")
        partial_text = self.tokenizer.decode(partial_text[0])
        partial_text = partial_text.split("<|assistant|> \n ")[-1]
        print(partial_text)
        result = partial_text
        return result

    def extract_json_from_llm_answer(self, result, start_str="```json", end_str="```", replace_list=["\n"]):
        s_id = result.index(start_str)
        e_id = result.index(end_str, s_id+len(start_str))
        json_str = result[s_id+len(start_str):e_id]
        for replace_str in replace_list:
            json_str = json_str.replace(replace_str,"")
        # print(json_str)
        try:
            json_dict = json.loads(json_str)
        except Exception as e:
            print("Error: ", e)
            print("json_str: ", json_str)
            json_dict = {}
        return json_dict

    def get_llm_json_answer(self, prompt):
        result = self.get_llm_answer(prompt)
        json_dict = self.extract_json_from_llm_answer(result)
        return json_dict