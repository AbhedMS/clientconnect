import pandas as pd
import chromadb
import uuid
from pathlib import Path
import os


class OrganizationPortfolio:
    def __init__(self, file_path="../../../data"):
        self.chroma_client = chromadb.Client()
        self.data_path = Path(file_path)

    def get_organization_info(self):
        with open(os.path.join(self.data_path, "organization_data.txt"), "r", encoding="utf-8") as file:
            organization_info = file.read()
        return organization_info

    def initiate_vector_store(self):
        try:
            self.collection = self.chroma_client.create_collection(name="serices_info")
            file_data= {}
            for file in os.listdir(self.data_path):
                if file != 'organization_data.txt':
                    with open(os.path.join(self.data_path, file), "r", encoding="utf-8") as f:
                        file_data[file] = f.read()
        except Exception as e:
            print("Data reading unsuccessful.", e)
            return False
            
        try:
            self.collection.add(
                ids=list(file_data.keys()),
                documents=list(file_data.values())
            )
            return True
        except Exception as e:
            print("Vector Database data insertion unsuccessful.", e)
            return False

    def get_matching_services(self, query_text, nr_of_services=3):
        result = self.collection.query(
            query_texts=[query_text],
            n_results=nr_of_services
        )

        best_matches = result['documents'][0]
        services = []
        for match in best_matches:
            services.append(match)

        return services


if __name__ == "__main__":
    print(os.listdir(Path("../../../data")))