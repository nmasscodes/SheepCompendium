from typing import Dict
from models.models import Sheep

class FakeDB:
    def __init__(self):
        self.data: Dict[int, Sheep] = {}

    def get_sheep(self, id: int) -> Sheep:
        return self.data.get(id)

    def add_sheep(self, sheep: Sheep) -> Sheep:
        if sheep.id in self.data:
            raise ValueError("Sheep with this ID already exists")
        self.data[sheep.id] = sheep
        return sheep

    def delete_sheep(self, id: int):
        if id not in self.data:
            raise ValueError("Sheep not found")
        del self.data[id]

    def update_sheep(self, id: int, sheep: Sheep):
        if id not in self.data:
            raise ValueError("Sheep not found")
        self.data[id] = sheep
        return sheep

# Initialize the fake database and add some sample data
db = FakeDB()
db.data = {
    1: Sheep(id=1, name="Spice", breed="Gotland", sex="ewe"),
    2: Sheep(id=2, name="Blondie", breed="Polypay", sex="ram"),
    3: Sheep(id=3, name="Deedee", breed="Jacobs Four Horns", sex="ram"),
    4: Sheep(id=4, name="Rommy", breed="Romney", sex="ewe"),
    5: Sheep(id=5, name="Vala", breed="Valais Blacknose", sex="ewe"),
    6: Sheep(id=6, name="Esther", breed="Border Leicester", sex="ewe"),
}
