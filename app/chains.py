import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader
from search import MatchingServices

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="openai/gpt-oss-20b")
        

    def sumerize_service(self, service: str): 

        prompt_email = PromptTemplate.from_template(
            """
            Surmarize below service provided by a firm. Don't helusinate and stick to facts.
            I DON'T NEED ANY PREAMBLE. NO PREAMBLE AT ALL!

            {service_details}

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"service_details": service})
        return res.content


    def extract_info(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from a potential client page of a website.
            Your job is to extract imformations like clients name, industry, business, products and 
            return a summary of clients business.
            ### I DON'T NEED ANY PREAMBLE. NO PREAMBLE AT ALL!
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        return res.content


    def write_mail(self, client_info, evolver_info, services):

        prompt_email = PromptTemplate.from_template(
            """
            ### Client Data:
            {client_details}

            ### INSTRUCTION:
            You are Sale Executive in a company called Evolver. Details of the firm Evolver is as below:
            {evolver_details}

            Your job is to write a cold email to the client mentioning what Evolver does and 
            how it will be able to add value to client's business.
            Also add the most relevant services that Evolver provides based on clients business: 
            1. {service1}
            2. {service2}
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"client_details": str(client_info), "evolver_details": evolver_info, 
                                  "service1": services[0], "service2": services[1]})
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
    loader = WebBaseLoader(["https://www.tcs.com/"])
    data = clean_text(loader.load().pop().page_content)
    obj = Chain()
    client_info = obj.extract_jobs(data)

    with open("./app/data/organization_data.txt", "rb") as file:
        evolver_info = file.read()
    
    obj_services = MatchingServices()
    obj_services.load_all_services()
    best_matches = obj_services.find_most_relevant_files(client_info)

    with open(f"app/data/{best_matches[0][0]}", "rb") as file:
        service1 = file.read()

    with open(f"app/data/{best_matches[1][0]}", "rb") as file:
        service2 = file.read()

    service1 = obj.sumerize_service(service1)
    service2 = obj.sumerize_service(service2)
    services = [service1, service2]

    mail_content = obj.write_mail(client_info, evolver_info, services)
    print(mail_content)
