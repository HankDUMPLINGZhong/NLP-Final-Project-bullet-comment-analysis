from openai import OpenAI
openai_api_key = "{your openai api key}"
deepseek_api_key = "{your deepseek api key}"
client = OpenAI(api_key = openai_api_key)
deepseek_client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
MY_COOKIE = "{your cookie}"