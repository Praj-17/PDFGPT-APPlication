
from app import app, url_to_somethig, embed_pdf, faiss_search
from tests import client

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_metadata_success(client):
    url = "http://example.com"
    data = {"url": url}
    response = client.post("/create_metadata", json=data)
    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'data' in response.json

def test_create_metadata_invalid_url(client):
    url = "invalid_url"
    data = {"url": url}
    response = client.post("/create_metadata", json=data)
    assert response.status_code == 200
    assert response.json['error'] == True
    assert response.json['message'] == "Failure"
    assert 'reason' in response.json

# Add more test cases for different scenarios

if __name__ == '__main__':
    pytest.main()
