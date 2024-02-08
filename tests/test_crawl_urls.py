
from app import app, crawler
from tests import client
import pytest

url = "https://ciet.ncert.gov.in/activity/internationalictconference"
depth = 1

def test_crawl_urls_success(client):
    data = {"url": url, "depth": depth}
    response = client.post("/crawl", json=data)

    assert response.status_code == 200
    assert response.json['error'] == False
    assert response.json['message'] == "Success"
    assert 'data' in response.json 
    assert response.json['data'] != []


def test_crawl_urls_invalid_url(client):
    url = "invalid_url"
    data = {"url": url}
    response = client.post("/crawl", json=data)
    assert response.status_code == 200
    assert response.json['error'] == True
    assert 'data' in response.json 
    assert response.json['data'] == []

# Add more test cases for different scenarios

if __name__ == '__main__':
    pytest.main()
