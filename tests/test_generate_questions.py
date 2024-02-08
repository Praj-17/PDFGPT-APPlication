from app import app, generator
import pytest

from tests import client
url = "https://assets.openstax.org/oscms-prodcms/media/documents/ConceptsofBiology-WEB.pdf"
num_questions = 5
page_number = 384
interval = 4

def test_generate_questions_all_text_success(client):
   
    data = {"mode": "all", "url": url, "num_questions": num_questions}
   
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'data' in response.json

def test_generate_questions_single_page_success(client):
    
    data = {"mode": "single", "url": url, "page_number": page_number, "num_questions": num_questions}
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'data' in response.json

def test_generate_questions_invalid_mode(client):
    data = {"mode": "invalid_mode", "url": url, "num_questions": num_questions}
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json['error'] == True
    assert response.json['message'] == "Failure"
    assert 'reason' in response.json

def test_generate_questions_interval_success(client):
    
    data = {"mode": "single", "url": url, "page_number": page_number, "num_questions": num_questions}
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'data' in response.json

# Add more test cases for different scenarios

if __name__ == '__main__':
    pytest.main()
