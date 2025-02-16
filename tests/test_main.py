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