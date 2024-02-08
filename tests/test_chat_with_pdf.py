from tests import client
from app import app, chat

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chat_with_pdf_all_pages_success(client):
    url = "http://example.com"
    data = {"mode": "all", "url": url, "question": "What is this?", "chat_history": []}
    response = client.post("/chat", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'response_data' in response.json

def test_chat_with_pdf_invalid_mode(client):
    url = "http://example.com"
    data = {"mode": "invalid_mode", "url": url, "question": "What is this?", "chat_history": []}
    response = client.post("/chat", json=data)
    assert response.status_code == 200
    assert response.json['error'] == True
    assert response.json['message'] == "Failure"
    assert 'reason' in response.json

# Add more test cases for different scenarios

if __name__ == '__main__':
    pytest.main()
