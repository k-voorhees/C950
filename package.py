from enum import Enum
import datetime

class Package:
    def __init__(self, id, address, city, state, zip, deadline, weight, note):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.note = note
        ##
        self.addressID = None
        self.status = Status.AT_HUB
        self.deliveryTime = datetime.time(0)
    
    def __str__(self):
        PackageToString = f"Package ID: {self.id}\nAddress ID: {self.addressID}\nAddress: {self.address}\nCity: {self.city}\nState: {self.state}\nZip Code: {self.zip}\nDeadline: {self.deadline}\nWeight: {self.weight}\nDelivery Status: {self.status}\nTime of Delivery: {self.deliveryTime}\n"
        
        return PackageToString
            
class Status(Enum):
    AT_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3
    DELAYED = 4
