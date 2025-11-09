from langchain_community.document_loaders import WebBaseLoader

from src.modules.chains import Chain
from src.modules.organization_data import OrganizationPortfolio
from src.modules.utils import clean_text, final_text_cleanup
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

CURRENT_DIR = os.path.abspath(__file__)
ROOT_DIR = os.getcwd()

my_organization = OrganizationPortfolio(os.path.join(ROOT_DIR, "data"))
database = my_organization.initiate_vector_store()
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

        with open('/run/secrets/api_key', 'r') as file:
            GROQ_API_KEY = file.read().strip()

        chain = Chain(GROQ_API_KEY)
        client_info = chain.extract_info(data)

        organization_info = my_organization.get_organization_info()
        services = my_organization.get_matching_services(client_info)

        mail_content = chain.write_mail(client_info, organization_info, services)

        client_info, mail_content = final_text_cleanup([client_info, mail_content])
        return jsonify({"description": client_info, "email": mail_content})


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

