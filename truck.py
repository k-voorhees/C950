MAX_CAPACITY = 16

class Truck:
    def __init__(self, id):
        self.id = id
        self.odometer = 0
        self.cargo = []
    
    def load(self, package):
        self.cargo.append(package)

    def hasRoom(self):
        if len(self.cargo) < MAX_CAPACITY:
            return True
        
        return False
    
    def availableSpace(self):
        return (MAX_CAPACITY - len(self.cargo))
