MAX_CAPACITY = 16
from datetime import time

class Truck:
    def __init__(self, id):
        self.id = id
        self.odometer = 0
        self.clock = time(8,0,0)    # tracks the time of day for each truck
        self.cargo = []
        self.location = 0   # coincide with addressID of package or HUB
        self.locationHistory = [()]
    
    def load(self, package):
        self.cargo.append(package)

    def hasRoom(self):
        if len(self.cargo) < MAX_CAPACITY:
            return True
        
        return False
