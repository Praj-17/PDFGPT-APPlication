
from app import app, url_to_somethig, embed_pdf, faiss_search
from tests import client
import pytest

import os
url = "https://assets.openstax.org/oscms-prodcms/media/documents/ConceptsofBiology-WEB.pdf"
def delete_folder_contents(folder_path):
    try:
        # Iterate over all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            # Check if it's a file and delete it
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"Deleted file: {item_path}")
            
            # Check if it's a directory and delete it recursively
            elif os.path.isdir(item_path):
                delete_folder_contents(item_path)
                os.rmdir(item_path)
                print(f"Deleted directory: {item_path}")

        print(f"All contents in {folder_path} deleted successfully.")

    except Exception as e:
        print(f"Error deleting contents of {folder_path}: {e}")


def test_create_metadata_success(client):
    delete_folder_contents("/pdfs")
    data = {"url": url, "page_number_locations": ['lc'], "page_number_style": ["alpha_numeric"]}
    response = client.post("/create_metadata", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'data' in response.json
    assert response.json['data']['json_path']
    assert response.json['data']['file_path']
    assert response.json['data']['index_path']
    assert response.json['data']['embedding_path']

def test_create_metadata_invalid_url(client):
    delete_folder_contents("/pdfs")
    data = {"url": url, "page_number_locations": ['lc'], "page_number_style": ["alpha_numeric"]}
    response = client.post("/create_metadata", json=data)
    assert response.status_code == 200
    assert response.json['error'] == True
    assert response.json['message'] == "Failure"
    assert 'reason' in response.json

# Add more test cases for different scenarios

if __name__ == '__main__':
    pytest.main()
