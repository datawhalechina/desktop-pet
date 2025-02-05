import json

from gradio_client import Client

class GradioClass(object):
    def __init__(self, url="http://116.62.10.217:8890/"):
        self.chat_history = []

        self.client = Client(url)


    def chat(self, prompt, role='user'):
        result = self.client.predict(
            in_text=prompt,
            api_name="/fn_get_response"
        )
        return result

    def get_llm_answer(self, prompt):
        result = self.client.predict(
            in_text=prompt,
            api_name="/fn_get_response"
        )
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
