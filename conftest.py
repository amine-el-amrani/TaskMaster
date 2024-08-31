import os
import pytest
from app import create_app, db
@pytest.fixture(scope='module', autouse=True)
def set_env_for_testing():
    os.environ['FLASK_ENV'] = 'testing'

@pytest.fixture(scope='function')
def test_client():
    app = create_app()
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
        yield testing_client
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='function')
def auth_header(test_client):
    """Fixture to handle user authentication and return the authorization header."""
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
    test_client.post('/register', json=user_data)
    response = test_client.post('/login', json={'email': 'testuser@example.com', 'password': 'testpassword'})
    assert response.status_code == 200
    access_token = response.json['access_token']
    return {'Authorization': f'Bearer {access_token}'}