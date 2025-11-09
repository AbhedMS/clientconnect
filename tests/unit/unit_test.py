import os
from modules.organization_data import OrganizationPortfolio
from modules.utils import read_yaml_file

ROOT_DIR = os.getcwd()

def test_vectordb():
    organization_data = OrganizationPortfolio(os.path.join(ROOT_DIR, "data"))
    database = organization_data.initiate_vector_store()
    assert database == True

def test_prompt():
    PROMPTS = read_yaml_file(os.path.join(ROOT_DIR, 'prompts.yaml'))["prompts"]
    assert PROMPTS['test_prompt'] == "This is a test prompt."

