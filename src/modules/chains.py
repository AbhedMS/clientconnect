import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from src.modules.utils import read_yaml_file

ROOT_DIR = os.getcwd()
PROMPTS = read_yaml_file(os.path.join(ROOT_DIR, 'prompts.yaml'))["prompts"]

class Chain:
    def __init__(self, GROQ_API_KEY):
        self.llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="openai/gpt-oss-20b")
        

    def summarize_service(self, service: str): 
        summarize_prompt = PROMPTS["summarize"]
        prompt_email = PromptTemplate.from_template(summarize_prompt)
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"service_details": service})
        return res.content


    def extract_info(self, cleaned_text):
        extract_info_prompt = PROMPTS["extract_information"]
        prompt_extract = PromptTemplate.from_template(extract_info_prompt)
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        return res.content


    def write_mail(self, client_info, evolver_info, services):
        write_email_prompt = PROMPTS["write_email"]
        prompt_email = PromptTemplate.from_template(write_email_prompt)
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"client_details": str(client_info), "evolver_details": evolver_info, 
                                  "service1": services[0], "service2": services[1]})
        return res.content
