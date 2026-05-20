import json
import pytest
from api import app, STORE


@pytest.fixture(autouse=True)
def clear_store():
    STORE.clear()
    yield
    STORE.clear()


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_list_items_empty(client):
    response = client.get('/items')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item_and_get_item(client):
    payload = {'name': 'test item', 'value': 123}
    create_response = client.post('/items', json=payload)
    assert create_response.status_code == 201
    item = create_response.get_json()
    assert item['data'] == payload
    assert 'id' in item

    get_response = client.get(f"/items/{item['id']}")
    assert get_response.status_code == 200
    assert get_response.get_json() == item


def test_create_item_requires_json(client):
    response = client.post('/items', data='not json', content_type='text/plain')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'JSON body required'}


def test_update_item_with_put(client):
    payload = {'foo': 'bar'}
    create_response = client.post('/items', json=payload)
    item = create_response.get_json()

    update_payload = {'updated': True}
    update_response = client.put(f"/items/{item['id']}", json=update_payload)
    assert update_response.status_code == 200
    updated_item = update_response.get_json()
    assert updated_item['id'] == item['id']
    assert updated_item['data'] == update_payload


def test_update_item_with_patch(client):
    payload = {'foo': 'bar'}
    item = client.post('/items', json=payload).get_json()

    update_payload = {'patched': 1}
    response = client.patch(f"/items/{item['id']}", json=update_payload)
    assert response.status_code == 200
    assert response.get_json()['data'] == update_payload


def test_update_item_requires_json(client):
    item = client.post('/items', json={'value': 1}).get_json()
    response = client.put(f"/items/{item['id']}", data='not json', content_type='text/plain')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'JSON body required'}


def test_get_missing_item_returns_404(client):
    response = client.get('/items/nonexistent')
    assert response.status_code == 404


def test_update_missing_item_returns_404(client):
    response = client.put('/items/nonexistent', json={})
    assert response.status_code == 404


def test_delete_item(client):
    item = client.post('/items', json={'name': 'delete me'}).get_json()
    delete_response = client.delete(f"/items/{item['id']}")
    assert delete_response.status_code == 204
    assert delete_response.data == b''

    missing_response = client.get(f"/items/{item['id']}")
    assert missing_response.status_code == 404


def test_delete_missing_item_returns_404(client):
    response = client.delete('/items/nonexistent')
    assert response.status_code == 404
