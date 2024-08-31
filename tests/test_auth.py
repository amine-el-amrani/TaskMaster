import pytest

@pytest.fixture
def create_user(test_client):
    test_client.post('/register', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    return test_client

def test_login(create_user):
    response = create_user.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_login_invalid_credentials(create_user):
    response = create_user.post('/login', json={
        'email': 'testuser@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert 'access_token' not in response.json

def test_login_no_user(create_user):
    response = create_user.post('/login', json={
        'email': 'nonexistentuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 401
    assert 'access_token' not in response.json

def test_logout(test_client, auth_header):
    response = test_client.post('/logout', headers=auth_header)
    assert response.status_code == 200
    assert response.json['message'] == 'User logged out successfully'