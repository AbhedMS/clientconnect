import os
from modules.pipelines.vector_database import OrganizationPortfolio

def test_vectordb():
    ROOT_DIR = os.getcwd()
    organization_data = OrganizationPortfolio(os.path.join(ROOT_DIR, "data"))
    database = organization_data.initiate_vector_store()
    assert database == True