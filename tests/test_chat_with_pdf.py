from tests import client
from app import app, chat
import pytest
url = "https://assets.openstax.org/oscms-prodcms/media/documents/ConceptsofBiology-WEB.pdf"

def test_chat_with_pdf_all_pages_success(client):

    data = {"mode": "all", "url": url, "question": "What is this?", "chat_history": []}
    response = client.post("/chat", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'response_data' in response.json
def test_chat_with_pdf_single_page_success(client):

    data = {"mode": "single", "url": url, "question": "What is this?", "chat_history": [], "page_number": 41}
    response = client.post("/chat", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'response_data' in response.json
def test_chat_with_pdf_interval_success(client):

    data = {"mode": "single", "url": url, "question": "What is this?", "chat_history": [], "page_number": 41, "interval":2}
    response = client.post("/chat", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'response_data' in response.json

def test_chat_with_pdf_invalid_mode(client):
    data = {"mode": "invalid_mode", "url": url, "question": "What is this?", "chat_history": []}
    response = client.post("/chat", json=data)
    assert response.status_code == 200
    assert response.json['error'] == True
    assert response.json['message'] == "Failure"
    assert 'reason' in response.json

# Add more test cases for different scenarios

if __name__ == '__main__':
    pytest.main()
