from fastapi.testclient import TestClient
from main
from models.db import db
from models.models import Sheep

client = TestClient(app)

def setup_module(module):
    # Initialize the fake database with sample data
    db.data = {
        1: Sheep(id=1, name="Spice", breed="Gotland", sex="ewe"),
        2: Sheep(id=2, name="Blondie", breed="Polypay", sex="ram"),
        3: Sheep(id=3, name="Deedee", breed="Jacobs Four Horns", sex="ram"),
        4: Sheep(id=4, name="Rommy", breed="Romney", sex="ewe"),
        5: Sheep(id=5, name="Vala", breed="Valais Blacknose", sex="ewe"),
        6: Sheep(id=6, name="Esther", breed="Border Leicester", sex="ewe"),
    }

def test_read_sheep():
    response = client.get("/sheep/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    new_sheep_data = {
        "id": 7,
        "name": "Bella",
        "breed": "F1",
        "sex": "ewe",
    }

    response = client.post("/sheep", json=new_sheep_data)
    assert response.status_code == 201, f"Expected status code 201, got {response.status_code}"
    assert response.json() == new_sheep_data, "Response data does not match the new sheep data."

    get_response = client.get(f"/sheep/{new_sheep_data['id']}")
    assert get_response.status_code == 200, f"Expected status code 200 for retrieval, got {get_response.status_code}"
    assert get_response.json() == new_sheep_data, "Retrieved sheep data does not match the new sheep data."



# Delete Sheep
def test_delete_sheep():
    # Ensure the sheep exists before deletion
    response = client.get("/sheep/1")
    assert response.status_code == 200  # Sheep should be found

    # Now delete the sheep
    response = client.delete("/sheep/1")
    assert response.status_code == 204  # Correctly expect No Content

    # Verify that the sheep has been deleted
    get_response = client.get("/sheep/1")
    assert get_response.status_code == 404  # Not Found


# Update Sheep
def test_update_sheep():
    # Ensure the sheep exists for the update
    sheep_data = {
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }
    client.post("/sheep", json=sheep_data)  # Ensure the sheep exists

    # Updated sheep data
    updated_sheep_data = {
        "id": 1,  # Include ID since it's required in the model
        "name": "Spice",
        "breed": "Dorper",
        "sex": "ewe",
    }

    response = client.put("/sheep/1", json=updated_sheep_data)

    # Check for the expected status code and response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Verify the response data
    assert response.json() == updated_sheep_data, "Response data does not match the updated sheep data."

    # Verify the update by retrieving the sheep
    get_response = client.get("/sheep/1")
    assert get_response.status_code == 200, f"Expected status code 200 for retrieval, got {get_response.status_code}"
    assert get_response.json() == updated_sheep_data, "Retrieved sheep data does not match the updated sheep data."



# Reads All Sheep
def test_read_all_sheep():
    response = client.get("/sheep")
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    # Verify that we have at least one sheep in the response
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Response list should contain at least one sheep"

    # Verify that the specific sheep exists in the list
    assert any(sheep["id"] == 1 and sheep["name"] == "Spice" for sheep in data), \
        "Expected to find 'Spice' in the list of sheep"
