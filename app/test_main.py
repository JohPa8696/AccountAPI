from pytest import fixture
from fastapi.testclient import TestClient
from .main import app

account_id = 1
account = {
    "name": "Bob",
    "description": "Bob's new account",
    "balance": 10,
    "active": True
}

@fixture()
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": True}

def test_create_account_with_valid_account_details(client):
    response = client.post(f'/accounts/{account_id}', json=account)
    assert response.status_code == 201
    assert response.json() == account

def test_create_account_with_an_existing_account_id(client):
    res = client.post(f'/accounts/{account_id}', json=account)
    assert res.status_code == 409
    assert res.json() == {"detail": f"Account with ID {account_id} already exists!"}

def test_get_account_with_valid_account_id(client):
    res = client.get(f'/accounts/{account_id}')
    assert res.status_code == 200
    assert res.json() == account

def test_get_account_with_invalid_account_id(client):
    invalid_account_id = 1000
    res = client.get(f'/accounts/{invalid_account_id}')
    assert res.status_code == 404
    assert res.json() == {"detail": f"Account with ID {invalid_account_id} not found!"}

def test_update_account_with_valid_account_id(client):
    updated_account = {
        "name": "Bob",
        "description": "Bob's new account",
        "balance": 20,
        "active": True
    }

    res = client.put(f'/accounts/{account_id}', json=updated_account)
    assert res.status_code == 201
    assert res.json() == updated_account
 
def test_update_account_with_invalid_account_id(client):
    invalid_account_id = 1000
    updated_account = {
        "name": "Bob",
        "description": "Bob's new account",
        "balance": 20,
        "active": True
    }

    res = client.put(f'/accounts/{invalid_account_id}', json=updated_account)
    assert res.status_code == 404
    assert res.json() == {"detail": f"Account with ID {invalid_account_id} not found!"}

def test_delete_account_with_invalid_account_id(client):
    invalid_account_id = 1000
    res = client.delete(f'/accounts/{invalid_account_id}')
    assert res.status_code == 404
    assert res.json() == {"detail": f"Account with ID {invalid_account_id} not found!"}


def test_delete_account_with_valid_account_id(client):
    res = client.delete(f'/accounts/{account_id}')
    assert res.status_code == 200
    assert res.json() == {"message": "Successful"}