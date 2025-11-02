from langchain_community.document_loaders import WebBaseLoader

from modules.chains import Chain
from modules.search import MatchingServices
from modules.utils import clean_text
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


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

        with open("./app/data/organization_data.txt", "rb") as file:
            evolver_info = file.read()
        
        matching_services = MatchingServices()
        matching_services.load_all_services()
        best_matches = matching_services.find_most_relevant_files(client_info)

        with open(f"app/data/{best_matches[0][0]}", "rb") as file:
            service1 = file.read()

        with open(f"app/data/{best_matches[1][0]}", "rb") as file:
            service2 = file.read()

        service1 = chain.sumerize_service(service1)
        service2 = chain.sumerize_service(service2)
        services = [service1, service2]

        mail_content = chain.write_mail(client_info, evolver_info, services)

        client_info = client_info.replace("*", "")
        client_info = client_info.replace("|", "")
        mail_content = mail_content.replace("*", "")
        mail_content = mail_content.replace("|", "")

        return jsonify({"description": client_info, "email": mail_content})


if __name__ == "__main__":
    app.run(debug=True)