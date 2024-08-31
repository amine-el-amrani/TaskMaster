import pytest

@pytest.fixture
def task_id(test_client, auth_header):
    response = test_client.post('/tasks', headers=auth_header, json={
        'title': 'Test Task',
        'description': 'This is a test task',
        'priority': 'High',
        'due_date': '2024-12-31'
    })
    print('Create Task Response:', response.status_code, response.data)
    assert response.status_code == 201
    response_json = response.get_json()
    assert isinstance(response_json, dict)
    return response_json.get('id')

def test_get_tasks(test_client, auth_header, task_id):
    try:
        print("Fetching tasks...")
        response = test_client.get('/tasks', headers=auth_header)
        print("Tasks fetched")
        print('Get Tasks Response:', response.status_code, response.get_json())
    except Exception as e:
        print(f"An error occurred: {e}")
        raise e
    assert response.status_code == 200
    tasks = response.get_json()
    print("Tasks:", tasks)
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    assert 'title' in tasks[0]
    assert 'description' in tasks[0]

def test_update_task(test_client, auth_header, task_id):
    response = test_client.put(f'/tasks/{task_id}', headers=auth_header, json={
        'title': 'Updated Task',
        'description': 'Updated description',
        'priority': 'Low'
    })
    print('Update Task Response:', response.status_code, response.get_json())
    assert response.status_code == 200

def test_delete_task(test_client, auth_header, task_id):
    response = test_client.delete(f'/tasks/{task_id}', headers=auth_header)
    print('Delete Task Response:', response.status_code, response.get_json())
    assert response.status_code == 200