from langchain_community.document_loaders import WebBaseLoader

from modules.chains import Chain
from modules.search import MatchingServices
from modules.pipelines.vector_database import OrganizationPortfolio
from modules.utils import clean_text
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

CURRENT_DIR = os.path.abspath(__file__)
ROOT_DIR = os.getcwd()

organization_data = OrganizationPortfolio(os.path.join(ROOT_DIR, "data"))
database = organization_data.initiate_vector_store()
if database:
    print("Database successfully initiated!")
else:
    print("Database NOT successfully initiated!")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    
    if request.method == "POST":
        data = request.get_json()
        client_url = data.get('url') 

        loader = WebBaseLoader([client_url])
        data = clean_text(loader.load().pop().page_content)

        chain = Chain()
        client_info = chain.extract_info(data)

        with open(os.path.join(ROOT_DIR, "data/organization_data.txt"), "r", encoding="utf-8") as file:
            evolver_info = file.read()
        
        result = organization_data.get_matching_services(client_info)
        best_matches = result['documents'][0]

        print("Number of documents: ", len(best_matches))

        service1 = chain.sumerize_service(best_matches[0])
        service2 = chain.sumerize_service(best_matches[1])
        services = [service1, service2]

        mail_content = chain.write_mail(client_info, evolver_info, services)

        client_info = client_info.replace("*", "")
        client_info = client_info.replace("|", "")
        mail_content = mail_content.replace("*", "")
        mail_content = mail_content.replace("|", "")

        return jsonify({"description": client_info, "email": mail_content})


if __name__ == "__main__":
    app.run(debug=True)

