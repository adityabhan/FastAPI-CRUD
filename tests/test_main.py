import pprint
import sys
sys.path.append('./app')
pprint.pprint(sys.path)

from fastapi.testclient import TestClient
from app.main import app, Todo

client = TestClient(app)

def test_get_todo():
    response = client.get("/todo/1")
    assert response.status_code == 404

def test_get_department_by_id():
    response = client.get("/department/1")
    assert response.status_code == 200
    expected_response = {"id":1,"name":"Computer Science"}
    assert response.json() == expected_response