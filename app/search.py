import os
from pathlib import Path
from sentence_transformers import SentenceTransformer, util

class MatchingServices:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.directory = Path('./app/data')

    def load_all_services(self):
        self.file_embeddings = {}
        for filename in os.listdir(self.directory):
            if filename.startswith('service') and filename.endswith('.txt'):
                filepath = os.path.join(self.directory, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    embedding = self.model.encode(content, convert_to_tensor=True)
                    self.file_embeddings[filename] = embedding

    def find_most_relevant_files(self, query, matches=3):
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        scores = {
            filename: util.cos_sim(query_embedding, embedding).item()
            for filename, embedding in self.file_embeddings.items()
        }
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:matches]


if __name__ == "__main__":

    user_query = "Tax auditing company"
    obj = MatchingServices()
    obj.load_all_services()
    best_matches = obj.find_most_relevant_files(user_query)

    print(f"Most relevant file: {best_matches[0][0]} with score {best_matches[0][1]}.")