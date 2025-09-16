import erniebot
import json

class ErnieClass(object):
    """
    ErnieBot API封装类

    Args:
        access_token (str): 用于访问ErnieBot API的access token。
        api_type (str, optional): 使用的ErnieBot API的类型。默认为"aistudio"。

    Returns:
        None

    """
    def __init__(self, access_token, api_type="aistudio"):
        erniebot.api_type = api_type
        erniebot.access_token = access_token
        self.chat_history = []

    def chat(self, prompt, role='user'):
        self.chat_history.append({'role': role, 'content': prompt})
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=self.chat_history,
            top_p=0,
            temperature = 0.1,
        )
        result = response.get_result()
        self.chat_history.append({'role': 'assistant', 'content': result})
        return result

    def get_llm_answer_with_msg(self, msg):
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=msg,
            top_p=0,
            temperature = 0.1,
        )
        result = response.get_result()
        return result

    def get_llm_answer(self, prompt):
        response = erniebot.ChatCompletion.create(
            model='ernie-3.5',
            messages=[{'role': 'user', 'content': prompt}],
            top_p=0,
            temperature=0.1,
        )
        result = response.get_result()
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